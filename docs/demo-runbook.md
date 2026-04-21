# JARVIS Demo Runbook

## Pre-Demo (5 min before)

1. Plug external USB mic + speakers if available (laptop mic OK but noisier)
2. Close music / video apps that hold the audio device
3. Open PowerShell in `D:\o_E\Desktop\project\jarvis` and run:
   ```powershell
   .\app\scripts\launch-demo.ps1
   ```
4. Wait ~15 seconds for all three windows to come up:
   - **Backend**: last line should read `Application startup complete`
   - **Frontend**: `ready in Xxx ms` + `Local: http://localhost:3000/`
   - **Clap listener**: `[READY] Listening. Clap twice to wake JARVIS.`
5. Browser auto-opens `http://localhost:3000`. Click **INITIALIZE** to enter dashboard
6. Verify status pill reads **ONLINE** (top-right)
7. Test-clap twice near the mic → wake flash + "Good evening, Sir. All systems online."

## Demo Script (5 min)

**Intro**: "This is J.A.R.V.I.S., a voice assistant inspired by Iron Man. It wakes with a clap, answers via Gemini, and speaks back with a JARVIS voice from ElevenLabs."

**Cue 1 — Wake**: Clap-clap → UI flashes green, greeting plays
**Cue 2 — Voice Q**: Click mic → *"Introduce yourself"* → JARVIS responds
**Cue 3 — Text Q**: Type *"What is the capital of France?"* in the bottom bar → Enter
**Cue 4 — Personality Q**: *"Tell me a joke about engineers."*

Camera on 3D orb during responses (waveform reacts).

**Graceful end**: Type *"Goodbye, Sir."* → let the reply finish → close windows.

## Fallbacks (if something breaks)

| Symptom | Fallback |
|---------|----------|
| Mic silent / clap doesn't trigger | Use text input at the bottom bar |
| ElevenLabs 401/quota exhausted | Backend auto-switches to pyttsx3 (offline, robotic) — demo continues |
| Backend offline | Status pill red; text input disabled. Run `launch-demo.ps1` again |
| Frontend crashes | Ctrl+R in the browser; dashboard reloads |
| Full reset | `.\app\scripts\stop-demo.ps1` → `.\app\scripts\launch-demo.ps1` |

## Calibration Tips

- If the clap listener triggers on normal speech → re-run it with `--threshold 0.2` (higher)
- If it never triggers even on strong claps → `--threshold 0.06` (lower)
- List mic devices: `python app\clap-wake-listener.py --list-devices`
- Force a specific device: set `CLAP_MIC_DEVICE_INDEX=13` in `.env` before launch

## Known Limitations

- Gemini response latency: 1–3 seconds
- ElevenLabs first call: cold start ~1.5 s; subsequent ~0.6 s
- Clap listener is mono and uses the system default mic; if the browser grabs mic exclusively for speech recognition, claps may be missed during listening mode
