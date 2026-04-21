# JARVIS — Clap-Wake Holographic Voice Assistant

Iron Man-style JARVIS demo:

- **Clap twice** → UI boots with a green flash + greeting
- **Holographic 3D neural UI** (Three.js: Arc Reactor, particle sphere, waveform)
- **Q&A** via Google Gemini
- **JARVIS-like voice** via ElevenLabs (pyttsx3 + browser-TTS fallback chain)

## Stack

| Layer | Tech |
|-------|------|
| Frontend | React 18, Vite, Three.js, GLSL |
| Backend | FastAPI, WebSocket, SQLite |
| LLM | Google Gemini (`gemini-3-flash-preview`) |
| TTS | ElevenLabs → pyttsx3 → browser TTS |
| STT | Web Speech API (client-side) |
| Clap wake | Python + sounddevice + numpy (RMS + double-clap detection) |

## Quick Start (Windows)

1. Copy `.env.example` → `.env`, fill in `GEMINI_API_KEY` and `ELEVENLABS_API_KEY`
2. Install:
   ```powershell
   # Backend
   cd app\backend
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   pip install sounddevice numpy requests

   # Frontend
   cd ..\frontend
   npm install
   ```
3. Run everything with one script:
   ```powershell
   .\app\scripts\launch-demo.ps1
   ```
4. Browser opens `http://localhost:3000` → click **INITIALIZE** → clap twice to wake

Stop: `.\app\scripts\stop-demo.ps1`

## Layout

```
jarvis/
├── app/
│   ├── backend/              # FastAPI + Gemini + ElevenLabs
│   ├── frontend/             # React + Three.js dashboard
│   ├── clap-detection/       # audio_stream_reader + double_clap_detector
│   ├── clap-wake-listener.py # entry-point: POSTs /system/wake on clap-clap
│   └── scripts/              # launch-demo.ps1, stop-demo.ps1
├── docs/demo-runbook.md      # pre-demo checklist, script, fallbacks
└── plans/                    # implementation plan + phase files
```

## Credits

- Base UI cloned from [harsh-raj00/my-jarvis](https://github.com/harsh-raj00/my-jarvis)
- Clap detection inspired by [Julian-Ivanov/jarvis-voice-assistant](https://github.com/Julian-Ivanov/jarvis-voice-assistant)

## License

MIT (demo project — not production-ready)
