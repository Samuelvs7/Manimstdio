"""Manim render engine — handles subprocess execution, render locking, and error parsing."""

import asyncio
import os
import re
import time
from pathlib import Path

# Global render lock
_render_lock = asyncio.Lock()


def detect_scenes(code: str) -> list[str]:
    """Parse Python code and return a list of Scene subclass names."""
    pattern = r"class\s+(\w+)\s*\(.*Scene.*\)"
    return re.findall(pattern, code)


def parse_errors(log_line: str) -> dict | None:
    """Detect common Manim/LaTeX errors in a log line."""
    error_patterns = [
        (r"LaTeX Error", "latex", "LaTeX compilation error"),
        (r"FileNotFoundError", "file", "Missing file or dependency"),
        (r"SyntaxError", "syntax", "Python syntax error"),
        (r"ModuleNotFoundError", "module", "Missing Python module"),
        (r"NameError", "name", "Undefined variable or name"),
        (r"TypeError", "type", "Type mismatch error"),
        (r"cannot find the file", "latex", "LaTeX compiler not found"),
    ]
    for pattern, error_type, description in error_patterns:
        if re.search(pattern, log_line, re.IGNORECASE):
            return {"type": error_type, "description": description, "line": log_line.strip()}
    return None


async def render_scene(
    code: str,
    scene_name: str,
    quality: str = "l",
    fps: int = 15,
    output_format: str = "mp4",
    manim_exe: str = "",
    project_dir: str = "",
    log_callback=None,
):
    """
    Render a Manim scene.

    Args:
        code: Python source code
        scene_name: Name of the Scene class to render
        quality: 'l' (480p), 'm' (720p), 'h' (1080p)
        fps: Frames per second
        output_format: 'mp4' or 'gif'
        manim_exe: Path to manim executable
        log_callback: Async callable(str) for streaming logs
    Returns:
        dict with 'success', 'video_path', 'errors'
    """
    if _render_lock.locked():
        return {"success": False, "video_path": None, "errors": [{"type": "busy", "description": "Another render is in progress. Please wait.", "line": ""}]}

    async with _render_lock:
        # Create temp directory
        temp_dir = Path(project_dir) / "temp"
        temp_dir.mkdir(exist_ok=True)

        # Write code to a uniquely named temp file
        timestamp = int(time.time() * 1000)
        temp_file = temp_dir / f"render_{timestamp}.py"
        temp_file.write_text(code, encoding="utf-8")

        # Build manim command
        quality_flag = f"-q{quality}"
        cmd = [
            manim_exe,
            quality_flag,
            f"--fps={fps}",
            f"--format={output_format}",
            "--disable_caching",
            str(temp_file),
            scene_name,
        ]

        if log_callback:
            await log_callback(f"[STUDIO] Rendering {scene_name} at quality={quality}, fps={fps}, format={output_format}")
            await log_callback(f"[STUDIO] Command: {' '.join(cmd)}")

        errors = []
        all_output = []

        try:
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.STDOUT,
                cwd=project_dir,
            )

            # Stream output line by line
            while True:
                line = await asyncio.wait_for(process.stdout.readline(), timeout=120)
                if not line:
                    break
                decoded = line.decode("utf-8", errors="replace").rstrip()
                all_output.append(decoded)

                # Check for errors
                error = parse_errors(decoded)
                if error:
                    errors.append(error)

                if log_callback:
                    await log_callback(decoded)

            await asyncio.wait_for(process.wait(), timeout=10)

            if log_callback:
                await log_callback(f"[STUDIO] Manim exited with code {process.returncode}")

        except asyncio.TimeoutError:
            process.kill()
            errors.append({"type": "timeout", "description": "Render timed out (120s limit)", "line": ""})
            if log_callback:
                await log_callback("[STUDIO] ❌ Render timed out!")
            return {"success": False, "video_path": None, "errors": errors}
        except Exception as e:
            errors.append({"type": "exception", "description": str(e), "line": ""})
            if log_callback:
                await log_callback(f"[STUDIO] ❌ Error: {e}")
            return {"success": False, "video_path": None, "errors": errors}

        # Find the output video
        video_path = find_output_video(project_dir, scene_name, output_format)

        if video_path and process.returncode == 0:
            if log_callback:
                await log_callback(f"[STUDIO] ✅ Render complete: {video_path}")
            return {"success": True, "video_path": video_path, "errors": errors}
        else:
            if log_callback:
                await log_callback("[STUDIO] ❌ Render failed. Check errors above.")
            return {"success": False, "video_path": None, "errors": errors}


def find_output_video(project_dir: str, scene_name: str, fmt: str = "mp4") -> str | None:
    """Search the media directory for the most recently rendered video matching the scene name."""
    media_dir = Path(project_dir) / "media" / "videos"
    if not media_dir.exists():
        return None

    # Find all matching files recursively
    matches = list(media_dir.rglob(f"{scene_name}.{fmt}"))
    if not matches:
        return None

    # Return the most recently modified one
    latest = max(matches, key=lambda p: p.stat().st_mtime)
    return str(latest)
