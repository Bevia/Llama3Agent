# LlamaAgent — Project Documentation

## Overview

LlamaAgent is a local AI chat interface that runs Meta's **Llama 3** model entirely on your machine via [Ollama](https://ollama.com/). It provides a desktop GUI built with [Kivy](https://kivy.org/) where you can type questions and receive responses from the model — no cloud services, no API keys required.

---

## Architecture

The project uses a **two-process pipeline**: the Kivy GUI and the Ollama inference run in separate OS processes, connected by `subprocess`.

```
User types question in GUI
        │
        ▼
[Kivy UI Process]
  Background thread launches:
    python3 llamaAgent.py "<user_text>"
        │
        ▼
[llamaAgent.py subprocess]
  ollama.chat(model="llama3", messages=[{"role": "user", "content": user_text}])
        │
        ▼
  Prints response to stdout
        │
        ▼
[Kivy UI Process]
  Captures stdout → Clock.schedule_once → updates response TextInput on main thread
```

This design avoids Kivy/Ollama threading conflicts entirely. Each query is a **fresh, single-turn** call — there is no conversation memory or multi-turn context between queries.

---

## Project Structure

```
Llama3Agent/
├── llamaAgent.py              # AI backend — calls Ollama, prints response to stdout
├── kivyFullDesktopAgent.py    # Primary UI — full desktop app with loading spinner
├── kivyDesktopAgent.py        # Intermediate UI — threaded, no spinner
├── kivyTerminalAgent.py       # Prototype UI — output goes to terminal only
├── assets/
│   ├── loader_01.png          # Spinner animation frames (21 total)
│   └── ...loader_21.png
└── README.md                  # Setup and install instructions
```

---

## File Descriptions

### `llamaAgent.py` — AI Backend

The core inference engine. Designed to be called as a subprocess, not directly.

- Reads the user query from `sys.argv[1]`
- Calls `ollama.chat(model="llama3", messages=[{"role": "user", "content": query}])`
- Prints the model response to stdout
- Falls back to a default question (`"I want to know more about private agents"`) if no argument is provided

### `kivyFullDesktopAgent.py` — Primary UI (most complete)

The main application. Adds an animated loading spinner on top of the base UI.

**Layout:**
```
FloatLayout (root)
├── BoxLayout (vertical)
│   ├── TextInput        [user input — 15% height]
│   ├── BoxLayout (horizontal)  [buttons — 15% height]
│   │   ├── Button "Enviar"   (green  — submit query)
│   │   ├── Button "Limpiar"  (red    — clear fields)
│   │   └── Button "Copiar"   (grey   — copy response to clipboard)
│   └── TextInput        [response display, read-only — 70% height]
└── Image                [spinner overlay — 200×200px, centered, shown during inference]
```

**Spinner:** Cycles through `assets/loader_01.png` → `loader_21.png` at 10 fps using `Clock.schedule_once` while waiting for the model response.

**Threading:** Inference runs in a `threading.Thread` so the UI stays responsive. The UI is updated via `Clock.schedule_once` from the background thread (required by Kivy).

### `kivyDesktopAgent.py` — Intermediate UI

Identical to `kivyFullDesktopAgent.py` but without the loading spinner. Uses a `BoxLayout` root instead of `FloatLayout`.

### `kivyTerminalAgent.py` — Prototype UI

Earliest version. Calls `llamaAgent.py` via `subprocess.run()` but does **not** capture output — responses print to the terminal, not the GUI. No threading; UI freezes during inference.

---

## Data Flow — Step by Step

1. User types a question in the top `TextInput` and clicks **Enviar**.
2. A `threading.Thread` is spawned to avoid freezing the UI.
3. The loading spinner starts animating.
4. The thread calls `subprocess.run(["python3", "llamaAgent.py", user_text], capture_output=True)`.
5. `llamaAgent.py` passes the text to Ollama's local `llama3` model.
6. Ollama returns the response; `llamaAgent.py` prints it to stdout.
7. The thread captures stdout and schedules a UI update via `Clock.schedule_once`.
8. The response appears in the read-only `TextInput`; the spinner stops.

---

## Dependencies

| Package | Purpose | Install |
|---|---|---|
| `kivy` | Desktop GUI framework | `pip install kivy` |
| `ollama` | Python SDK for local LLM inference | `pip install ollama` |
| Ollama CLI | Local model runtime | [ollama.com](https://ollama.com) → `ollama pull llama3` |

Standard library: `sys`, `subprocess`, `threading`

**Python version:** 3.12+

---

## Setup

1. Install [Ollama](https://ollama.com/) and pull the model:
   ```bash
   ollama pull llama3
   ```

2. Install Python dependencies:
   ```bash
   pip install kivy ollama
   ```

3. Run the app:
   ```bash
   python3 kivyFullDesktopAgent.py
   ```

---

## Key Design Decisions

| Decision | Reason |
|---|---|
| Separate subprocess for inference | Avoids Kivy/Ollama threading conflicts |
| Background thread in the UI | Keeps the GUI responsive during slow inference |
| `Clock.schedule_once` for UI updates | Kivy requires UI changes on the main thread |
| 21-frame PNG sprite animation | Simple cross-platform loading indicator with no extra dependencies |
| Single-turn queries (no history) | Keeps the backend stateless and simple |

---

## Limitations

- No conversation memory — each query is independent
- Model and settings are hardcoded (no config file)
- No `requirements.txt` — dependencies must be installed manually
- UI labels are in Spanish ("Enviar", "Limpiar", "Copiar")
