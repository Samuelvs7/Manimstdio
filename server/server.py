"""Manim Animation Studio — FastAPI server."""

import json
import os
import shutil
import sys
from pathlib import Path

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

# Support both `python server/server.py` and `uvicorn server.server:app`
try:
    from server.render_engine import detect_scenes, render_scene
except ImportError:
    from render_engine import detect_scenes, render_scene

# Paths
PROJECT_DIR = str(Path(__file__).resolve().parent.parent)

# Cross-platform manim executable detection (Windows local dev or Linux Docker)
_win_exe = Path(PROJECT_DIR) / ".venv" / "Scripts" / "manim.exe"
_unix_exe = Path(PROJECT_DIR) / ".venv" / "bin" / "manim"
MANIM_EXE = (
    str(_win_exe) if _win_exe.exists()
    else str(_unix_exe) if _unix_exe.exists()
    else shutil.which("manim") or "manim"
)
STATIC_DIR = str(Path(PROJECT_DIR) / "static")
MEDIA_DIR = str(Path(PROJECT_DIR) / "media")

app = FastAPI(title="Manim Animation Studio")

# Serve static files
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


# ---------- Models ----------

class ScenesRequest(BaseModel):
    code: str


class FileRequest(BaseModel):
    path: str
    content: str | None = None


# ---------- Routes ----------

@app.get("/")
async def index():
    """Serve the main IDE page."""
    return FileResponse(Path(STATIC_DIR) / "index.html")


@app.post("/api/scenes")
async def get_scenes(req: ScenesRequest):
    """Detect Scene subclasses from code."""
    scenes = detect_scenes(req.code)
    return JSONResponse({"scenes": scenes})


@app.get("/api/video/{filepath:path}")
async def serve_video(filepath: str):
    """Serve a rendered video file."""
    video_path = Path(MEDIA_DIR) / filepath
    if video_path.exists():
        media_type = "video/mp4" if str(video_path).endswith(".mp4") else "image/gif"
        return FileResponse(str(video_path), media_type=media_type)
    return JSONResponse({"error": "Video not found"}, status_code=404)


@app.post("/api/save")
async def save_file(req: FileRequest):
    """Save code to a .py file."""
    try:
        path = Path(req.path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(req.content, encoding="utf-8")
        return JSONResponse({"success": True, "path": str(path)})
    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)}, status_code=500)


@app.post("/api/open")
async def open_file(req: FileRequest):
    """Read a .py file."""
    try:
        path = Path(req.path)
        if not path.exists():
            return JSONResponse({"success": False, "error": "File not found"}, status_code=404)
        content = path.read_text(encoding="utf-8")
        return JSONResponse({"success": True, "content": content, "path": str(path)})
    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)}, status_code=500)


# ---------- WebSocket Render Stream ----------

@app.websocket("/api/render-stream")
async def render_stream(ws: WebSocket):
    """WebSocket endpoint for real-time render streaming."""
    await ws.accept()

    try:
        # Receive render config
        data = await ws.receive_text()
        config = json.loads(data)

        code = config.get("code", "")
        scene = config.get("scene", "")
        quality = config.get("quality", "l")
        fps = config.get("fps", 15)
        output_format = config.get("format", "mp4")

        if not code or not scene:
            await ws.send_json({"type": "error", "message": "Code and scene name are required"})
            await ws.close()
            return

        # Log callback sends each line to the client
        async def send_log(line: str):
            try:
                await ws.send_json({"type": "log", "message": line})
            except Exception:
                pass

        await send_log(f"[STUDIO] Starting render of '{scene}'...")

        result = await render_scene(
            code=code,
            scene_name=scene,
            quality=quality,
            fps=fps,
            output_format=output_format,
            manim_exe=MANIM_EXE,
            project_dir=PROJECT_DIR,
            log_callback=send_log,
        )

        # Send final result
        video_url = None
        if result["success"] and result["video_path"]:
            # Convert absolute path to relative URL
            rel_path = Path(result["video_path"]).relative_to(Path(MEDIA_DIR))
            video_url = f"/api/video/{rel_path.as_posix()}"

        await ws.send_json({
            "type": "complete",
            "success": result["success"],
            "video_url": video_url,
            "errors": result.get("errors", []),
        })

    except WebSocketDisconnect:
        pass
    except Exception as e:
        try:
            await ws.send_json({"type": "error", "message": str(e)})
        except Exception:
            pass
    finally:
        try:
            await ws.close()
        except Exception:
            pass


if __name__ == "__main__":
    import uvicorn

    # Add server directory to path for imports
    sys.path.insert(0, str(Path(__file__).parent))
    port = int(os.environ.get("PORT", 8000))
    print(f"Manim Studio starting...")
    print(f"  Project dir: {PROJECT_DIR}")
    print(f"  Manim exe:   {MANIM_EXE}")
    print(f"  Static dir:  {STATIC_DIR}")
    print(f"  Open http://localhost:{port} in your browser")
    uvicorn.run("server:app", host="0.0.0.0", port=port, reload=False)
