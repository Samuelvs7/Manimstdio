/* ========================================
   VS Animation Studio — App Logic
   Splash, Themes, Resizable Terminal, WebSocket
   ======================================== */

// ===== State =====
let editor = null;
let isRendering = false;
let currentFilePath = null;
let autoSaveTimer = null;

const DEFAULT_CODE = `from manim import *

class MyScene(Scene):
    def construct(self):
        # Your animation code here
        text = Text("Hello, Manim!", font_size=72)
        self.play(Write(text))
        self.wait(1)

        # Transform into a star
        star = Star(color=YELLOW, fill_opacity=1).scale(2)
        self.play(Transform(text, star))
        self.play(FadeOut(text))
`;

// ===== Splash Screen =====
function initSplash() {
    const splash = document.getElementById('splash-screen');
    const statusEl = splash.querySelector('.splash-status');

    const messages = [
        'Initializing workspace...',
        'Loading animation engine...',
        'Preparing code editor...',
        'Setting up render pipeline...',
        'Almost ready...',
    ];

    let i = 0;
    const interval = setInterval(() => {
        i++;
        if (i < messages.length) {
            statusEl.textContent = messages[i];
        }
    }, 500);

    // Hide splash after animation completes
    setTimeout(() => {
        clearInterval(interval);
        splash.style.opacity = '0';
        splash.style.pointerEvents = 'none';
        setTimeout(() => {
            splash.classList.add('hidden');
        }, 600);
    }, 3000);
}

// ===== Theme System =====
function initTheme() {
    // Load saved theme
    const savedTheme = localStorage.getItem('vs-studio-theme') || 'dark';
    setTheme(savedTheme);

    // Prevent clicks inside dropdown from closing it
    document.getElementById('theme-dropdown').addEventListener('click', (e) => {
        e.stopPropagation();
    });

    // Theme button toggle
    document.getElementById('btn-theme').addEventListener('click', (e) => {
        e.stopPropagation();
        document.getElementById('theme-menu').classList.toggle('open');
    });

    // Theme options
    document.querySelectorAll('.theme-option').forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.stopPropagation();
            const theme = btn.dataset.theme;
            console.log('[Theme] Switching to:', theme);
            setTheme(theme);
            document.getElementById('theme-menu').classList.remove('open');
        });
    });

    // Close theme menu when clicking outside
    document.addEventListener('click', () => {
        document.getElementById('theme-menu').classList.remove('open');
    });
}

function setTheme(theme) {
    console.log('[Theme] Setting data-theme to:', theme);
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('vs-studio-theme', theme);

    // Update active state
    document.querySelectorAll('.theme-option').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.theme === theme);
    });

    // Update Monaco theme
    if (editor) {
        const monacoTheme = theme === 'light' ? 'vs-light-custom' : (theme === 'neon' ? 'neon-dark' : 'manim-dark');
        console.log('[Theme] Setting Monaco theme to:', monacoTheme);
        monaco.editor.setTheme(monacoTheme);
    }
}

// ===== Resizable Terminal =====
function initResizableTerminal() {
    const handle = document.getElementById('resize-handle');
    const consolePanel = document.getElementById('console-panel');
    const appWrapper = document.getElementById('app-wrapper');
    let isResizing = false;
    let startY, startHeight;

    handle.addEventListener('mousedown', (e) => {
        isResizing = true;
        startY = e.clientY;
        startHeight = consolePanel.offsetHeight;
        handle.classList.add('active');
        document.body.style.cursor = 'ns-resize';
        document.body.style.userSelect = 'none';
        e.preventDefault();
    });

    document.addEventListener('mousemove', (e) => {
        if (!isResizing) return;
        const diff = startY - e.clientY;
        const newHeight = Math.max(60, Math.min(600, startHeight + diff));
        consolePanel.style.height = newHeight + 'px';
    });

    document.addEventListener('mouseup', () => {
        if (isResizing) {
            isResizing = false;
            handle.classList.remove('active');
            document.body.style.cursor = '';
            document.body.style.userSelect = '';
        }
    });
}

// ===== Progress Bar =====
function showProgress(active) {
    const bar = document.getElementById('render-progress-bar');
    const fill = document.getElementById('progress-fill');
    if (active) {
        bar.classList.add('active');
        fill.classList.add('animating');
    } else {
        fill.classList.remove('animating');
        fill.style.width = '100%';
        setTimeout(() => {
            bar.classList.remove('active');
            fill.style.width = '0%';
        }, 500);
    }
}

// ===== Initialize Monaco Editor =====
require.config({
    paths: { vs: 'https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.45.0/min/vs' }
});

require(['vs/editor/editor.main'], function () {
    // Dark theme
    monaco.editor.defineTheme('manim-dark', {
        base: 'vs-dark', inherit: true,
        rules: [
            { token: 'comment', foreground: '6A737D', fontStyle: 'italic' },
            { token: 'keyword', foreground: 'C586C0' },
            { token: 'string', foreground: 'CE9178' },
            { token: 'number', foreground: 'B5CEA8' },
            { token: 'type', foreground: '4EC9B0' },
            { token: 'function', foreground: 'DCDCAA' },
        ],
        colors: {
            'editor.background': '#12131f',
            'editor.foreground': '#e2e8f0',
            'editorLineNumber.foreground': '#4a4b65',
            'editorLineNumber.activeForeground': '#e2e8f0',
            'editor.selectionBackground': '#264f78',
            'editor.lineHighlightBackground': '#1a1b2e',
            'editorCursor.foreground': '#6366f1',
        }
    });

    // Light theme
    monaco.editor.defineTheme('vs-light-custom', {
        base: 'vs', inherit: true,
        rules: [
            { token: 'comment', foreground: '6a9955', fontStyle: 'italic' },
            { token: 'keyword', foreground: 'af00db' },
            { token: 'string', foreground: 'a31515' },
        ],
        colors: {
            'editor.background': '#ffffff',
            'editor.foreground': '#1a1b2e',
            'editorLineNumber.foreground': '#b0b0c0',
            'editor.lineHighlightBackground': '#f5f6fa',
            'editorCursor.foreground': '#4f46e5',
        }
    });

    // Neon theme
    monaco.editor.defineTheme('neon-dark', {
        base: 'vs-dark', inherit: true,
        rules: [
            { token: 'comment', foreground: '446688', fontStyle: 'italic' },
            { token: 'keyword', foreground: 'bf00ff' },
            { token: 'string', foreground: '00ff88' },
            { token: 'number', foreground: 'ffee00' },
            { token: 'type', foreground: '00f0ff' },
            { token: 'function', foreground: 'ff6600' },
        ],
        colors: {
            'editor.background': '#080815',
            'editor.foreground': '#e0f0ff',
            'editorLineNumber.foreground': '#334466',
            'editorLineNumber.activeForeground': '#00f0ff',
            'editor.selectionBackground': '#1a1a5e',
            'editor.lineHighlightBackground': '#0d0d20',
            'editorCursor.foreground': '#00f0ff',
        }
    });

    const savedCode = localStorage.getItem('manim-studio-code');
    const savedTheme = localStorage.getItem('vs-studio-theme') || 'dark';
    const monacoTheme = savedTheme === 'light' ? 'vs-light-custom' : (savedTheme === 'neon' ? 'neon-dark' : 'manim-dark');

    editor = monaco.editor.create(document.getElementById('monaco-editor'), {
        value: savedCode || DEFAULT_CODE,
        language: 'python',
        theme: monacoTheme,
        fontSize: 14,
        fontFamily: "'JetBrains Mono', 'Consolas', monospace",
        minimap: { enabled: false },
        scrollBeyondLastLine: false,
        lineNumbers: 'on',
        roundedSelection: true,
        padding: { top: 12 },
        automaticLayout: true,
        tabSize: 4,
        wordWrap: 'off',
        suggestOnTriggerCharacters: true,
        quickSuggestions: true,
    });

    editor.onDidChangeModelContent(() => {
        detectScenes();
        showUnsaved(true);
        clearTimeout(autoSaveTimer);
        autoSaveTimer = setTimeout(() => {
            localStorage.setItem('manim-studio-code', editor.getValue());
        }, 1000);
    });

    detectScenes();
});

// ===== Scene Detection =====
async function detectScenes() {
    if (!editor) return;
    const code = editor.getValue();
    try {
        const res = await fetch('/api/scenes', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ code }),
        });
        const data = await res.json();
        const sel = document.getElementById('scene-selector');
        const currentVal = sel.value;
        sel.innerHTML = '';
        if (data.scenes && data.scenes.length > 0) {
            data.scenes.forEach((scene, idx) => {
                const opt = document.createElement('option');
                opt.value = scene;
                opt.textContent = scene;
                if (scene === currentVal || (idx === 0 && !currentVal)) opt.selected = true;
                sel.appendChild(opt);
            });
        } else {
            const opt = document.createElement('option');
            opt.value = '';
            opt.textContent = 'No scenes found';
            sel.appendChild(opt);
        }
    } catch (e) { /* server might not be ready */ }
}

// ===== Render via WebSocket =====
function startRender(mode) {
    if (isRendering) {
        logMessage('[STUDIO] ⏳ Another render is already in progress!', 'warning');
        return;
    }

    const code = editor ? editor.getValue() : '';
    const scene = document.getElementById('scene-selector').value;

    if (!scene) {
        logMessage('[STUDIO] ❌ No scene selected. Define a Scene class in your code.', 'error');
        return;
    }

    let quality, fps, format;
    if (mode === 'preview') {
        quality = document.getElementById('preview-quality').value;
        fps = parseInt(document.getElementById('preview-fps').value);
        format = 'mp4';
    } else {
        quality = document.getElementById('render-quality').value;
        fps = parseInt(document.getElementById('render-fps').value);
        format = document.getElementById('render-format').value;
    }

    setRendering(true);
    showPreviewLoading();
    clearConsole();
    showProgress(true);

    logMessage(`[STUDIO] 🔄 Connecting to render server...`, 'info');

    const protocol = location.protocol === 'https:' ? 'wss:' : 'ws:';
    const ws = new WebSocket(`${protocol}//${location.host}/api/render-stream`);

    ws.onopen = () => {
        logMessage('[STUDIO] ✅ Connected! Sending render request...', 'info');
        setConnectionStatus('rendering');
        ws.send(JSON.stringify({ code, scene, quality, fps, format }));
    };

    ws.onmessage = (event) => {
        const data = JSON.parse(event.data);

        if (data.type === 'log') {
            let level = '';
            if (data.message.includes('❌') || data.message.includes('Error') || data.message.includes('error')) level = 'error';
            else if (data.message.includes('✅') || data.message.includes('complete')) level = 'success';
            else if (data.message.includes('[STUDIO]')) level = 'info';
            else if (data.message.includes('WARNING')) level = 'warning';
            logMessage(data.message, level);
        } else if (data.type === 'complete') {
            showProgress(false);
            if (data.success && data.video_url) {
                logMessage(`[STUDIO] ✅ Render successful!`, 'success');
                showPreviewVideo(data.video_url);
            } else {
                logMessage('[STUDIO] ❌ Render failed.', 'error');
                showPreviewPlaceholder();
            }
            if (data.errors && data.errors.length > 0) {
                data.errors.forEach(err => {
                    logMessage(`[ERROR] ${err.description}: ${err.line}`, 'error');
                });
            }
            setRendering(false);
            setConnectionStatus('connected');
        } else if (data.type === 'error') {
            logMessage(`[STUDIO] ❌ ${data.message}`, 'error');
            showPreviewPlaceholder();
            showProgress(false);
            setRendering(false);
            setConnectionStatus('error');
        }
    };

    ws.onerror = () => {
        logMessage('[STUDIO] ❌ WebSocket error. Is the server running?', 'error');
        showPreviewPlaceholder();
        showProgress(false);
        setRendering(false);
        setConnectionStatus('error');
    };

    ws.onclose = () => {
        if (isRendering) { setRendering(false); showProgress(false); }
        setConnectionStatus('connected');
    };
}

// ===== UI Helpers =====
function setRendering(state) {
    isRendering = state;
    document.getElementById('btn-render').disabled = state;
    document.getElementById('btn-preview').disabled = state;
    const statusEl = document.getElementById('render-status');
    statusEl.textContent = state ? 'Rendering...' : 'Ready';
    statusEl.className = state ? 'status-rendering' : 'status-ready';
}

function setConnectionStatus(status) {
    const dot = document.querySelector('#connection-status .dot');
    dot.className = 'dot';
    if (status === 'connected') { dot.classList.add('green'); }
    else if (status === 'rendering') { dot.classList.add('orange'); }
    else if (status === 'error') { dot.classList.add('red'); }
}

function showPreviewLoading() {
    document.getElementById('preview-placeholder').style.display = 'none';
    document.getElementById('preview-loading').style.display = 'block';
    document.getElementById('preview-video').style.display = 'none';
}

function showPreviewPlaceholder() {
    document.getElementById('preview-placeholder').style.display = 'block';
    document.getElementById('preview-loading').style.display = 'none';
    document.getElementById('preview-video').style.display = 'none';
}

function showPreviewVideo(url) {
    document.getElementById('preview-placeholder').style.display = 'none';
    document.getElementById('preview-loading').style.display = 'none';
    const video = document.getElementById('preview-video');
    video.src = url + '?t=' + Date.now();
    video.style.display = 'block';
    video.load();
    video.play().catch(() => {});
}

function showUnsaved(show) {
    document.getElementById('unsaved-indicator').style.display = show ? 'inline' : 'none';
}

// ===== Console =====
function logMessage(message, level = '') {
    const output = document.getElementById('console-output');
    const line = document.createElement('div');
    line.className = `log-line ${level}`;
    line.textContent = message;
    output.appendChild(line);
    output.scrollTop = output.scrollHeight;
}

function clearConsole() {
    document.getElementById('console-output').innerHTML = '';
}

// ===== File Operations =====
async function newFile() {
    if (editor) {
        editor.setValue(DEFAULT_CODE);
        currentFilePath = null;
        showUnsaved(false);
        logMessage('[STUDIO] 📄 New file created.', 'info');
    }
}

async function openFile() {
    try {
        if ('showOpenFilePicker' in window) {
            const [fileHandle] = await window.showOpenFilePicker({
                types: [{ description: 'Python Files', accept: { 'text/x-python': ['.py'] } }],
            });
            const file = await fileHandle.getFile();
            editor.setValue(await file.text());
            currentFilePath = file.name;
            showUnsaved(false);
            logMessage(`[STUDIO] 📂 Opened: ${file.name}`, 'info');
        } else {
            const input = document.createElement('input');
            input.type = 'file'; input.accept = '.py';
            input.onchange = async (e) => {
                const file = e.target.files[0];
                if (file) {
                    editor.setValue(await file.text());
                    currentFilePath = file.name;
                    showUnsaved(false);
                    logMessage(`[STUDIO] 📂 Opened: ${file.name}`, 'info');
                }
            };
            input.click();
        }
    } catch (e) {
        if (e.name !== 'AbortError') logMessage(`[STUDIO] ❌ ${e.message}`, 'error');
    }
}

async function saveFile() {
    try {
        if ('showSaveFilePicker' in window) {
            const handle = await window.showSaveFilePicker({
                suggestedName: currentFilePath || 'scene.py',
                types: [{ description: 'Python Files', accept: { 'text/x-python': ['.py'] } }],
            });
            const writable = await handle.createWritable();
            await writable.write(editor.getValue());
            await writable.close();
            currentFilePath = handle.name;
            showUnsaved(false);
            logMessage(`[STUDIO] 💾 Saved: ${handle.name}`, 'success');
        } else {
            const blob = new Blob([editor.getValue()], { type: 'text/x-python' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url; a.download = currentFilePath || 'scene.py';
            a.click(); URL.revokeObjectURL(url);
            showUnsaved(false);
            logMessage(`[STUDIO] 💾 Downloaded: ${a.download}`, 'success');
        }
    } catch (e) {
        if (e.name !== 'AbortError') logMessage(`[STUDIO] ❌ ${e.message}`, 'error');
    }
}

// ===== Event Listeners =====
document.addEventListener('DOMContentLoaded', () => {
    // Init systems
    initSplash();
    initTheme();
    initResizableTerminal();

    // Buttons
    document.getElementById('btn-new').addEventListener('click', newFile);
    document.getElementById('btn-open').addEventListener('click', openFile);
    document.getElementById('btn-save').addEventListener('click', saveFile);
    document.getElementById('btn-render').addEventListener('click', () => startRender('render'));
    document.getElementById('btn-preview').addEventListener('click', () => startRender('preview'));
    document.getElementById('btn-clear-console').addEventListener('click', clearConsole);
    document.getElementById('btn-copy-logs').addEventListener('click', () => {
        navigator.clipboard.writeText(document.getElementById('console-output').innerText)
            .then(() => logMessage('[STUDIO] 📋 Logs copied!', 'info'));
    });

    // Font size
    document.getElementById('font-size-selector').addEventListener('change', (e) => {
        if (editor) editor.updateOptions({ fontSize: parseInt(e.target.value) });
    });

    // Keyboard shortcuts
    document.addEventListener('keydown', (e) => {
        if (e.ctrlKey && e.key === 's') { e.preventDefault(); saveFile(); }
        if (e.ctrlKey && e.key === 'o') { e.preventDefault(); openFile(); }
        if (e.ctrlKey && e.key === 'n') { e.preventDefault(); newFile(); }
        if (e.ctrlKey && !e.shiftKey && e.key === 'Enter') { e.preventDefault(); startRender('preview'); }
        if (e.ctrlKey && e.shiftKey && e.key === 'Enter') { e.preventDefault(); startRender('render'); }
    });

    // Welcome
    logMessage('[STUDIO] 🚀 VS Animation Studio ready.', 'info');
    logMessage('[STUDIO] ⌨️  Shortcuts: Ctrl+Enter = Preview | Ctrl+Shift+Enter = Render | Ctrl+S = Save', 'info');
});
