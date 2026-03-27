# Manim Animation Studio

A professional web-based IDE for writing, rendering, and previewing Manim animations.

## Features
- **Monaco Code Editor** with Python syntax highlighting
- **Live Preview** — rendered videos display in-browser
- **Real-time Logs** — WebSocket streaming of render output
- **Scene Auto-Detection** — select from multiple scenes in your code
- **Render Controls** — choose quality (480p/720p/1080p), FPS, and format (MP4/GIF)
- **File Operations** — New, Open, Save with keyboard shortcuts
- **Error Parsing** — LaTeX, syntax, and dependency errors highlighted

## Quick Start

1. **Install dependencies** (first time only):
```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e .
.\.venv\Scripts\python.exe -m pip install fastapi uvicorn websockets python-multipart
```

2. **Launch the Studio**:
```powershell
.\.venv\Scripts\python.exe server/server.py
```

3. **Open in browser**: [http://localhost:8000](http://localhost:8000)

## Keyboard Shortcuts
| Shortcut | Action |
|---|---|
| `Ctrl + Enter` | Quick Preview |
| `Ctrl + Shift + Enter` | Final Render |
| `Ctrl + S` | Save File |
| `Ctrl + O` | Open File |
| `Ctrl + N` | New File |
