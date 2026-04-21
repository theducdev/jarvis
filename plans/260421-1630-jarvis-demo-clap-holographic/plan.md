---
title: Jarvis Demo — Clap-to-Wake + Holographic UI
created: 2026-04-21
status: completed
mode: auto
blockedBy: []
blocks: []
tags: [demo, jarvis, voice-assistant, three.js, elevenlabs, gemini]
---

# Jarvis Demo — Clap-to-Wake + Holographic Neural UI

## Objective
Build a **demo-quality** Iron-Man-style JARVIS:
- Double-clap → wake animation
- Holographic 3D neural UI (Arc Reactor + particle sphere)
- Q&A via Gemini API
- JARVIS-like voice via ElevenLabs

## Strategy
**Fork + merge approach** — avoid writing from scratch:
- **Base**: [harsh-raj00/my-jarvis](https://github.com/harsh-raj00/my-jarvis) → UI + voice + Q&A stack
- **Wake module**: `clap-trigger.py` from [Julian-Ivanov/jarvis-voice-assistant](https://github.com/Julian-Ivanov/jarvis-voice-assistant)
- Bridge clap trigger → frontend via WebSocket (existing in `my-jarvis`)

## Stack
| Layer | Tech |
|-------|------|
| Frontend | React + Three.js + GLSL shaders |
| Backend | FastAPI + WebSocket |
| LLM | Google Gemini API |
| TTS | ElevenLabs (JARVIS voice preset) |
| STT | Web Speech API (client-side) |
| Clap wake | Python + sounddevice + numpy (energy spike detection) |

## Phases

| # | Phase | Status | File |
|---|-------|--------|------|
| 1 | Environment setup + API keys | Completed | [phase-01](./phase-01-environment-setup.md) |
| 2 | Clone base repo + smoke test | Completed | [phase-02](./phase-02-clone-and-configure-base.md) |
| 3 | Integrate clap-trigger wake | Completed | [phase-03](./phase-03-integrate-clap-trigger.md) |
| 4 | Configure JARVIS voice (ElevenLabs) | Completed | [phase-04](./phase-04-configure-jarvis-voice.md) |
| 5 | Demo polish + launch script | Completed | [phase-05](./phase-05-demo-polish-and-launch.md) |

## Implementation Summary

**Phase 3 — Clap wake** (live tested):
- `app/clap-detection/audio_stream_reader.py` — sounddevice wrapper, 16kHz mono, 50ms RMS windows
- `app/clap-detection/double_clap_detector.py` — rising-edge detector, 120–800ms double-clap window, 2s cooldown
- `app/clap-wake-listener.py` — entry script with 3s ambient-noise auto-calibration, POSTs `/api/v1/system/wake`
- `backend/src/api/v1/endpoints/system.py::wake_event` — localhost-only guard, broadcasts `{type:"wake"}` via WS
- `JarvisDashboard.jsx` — WS subscription → wakeFlash overlay + auto-greeting
- Verified: `curl POST /system/wake` → `{"ok":true,"clients":0}` HTTP 200

**Phase 4 — ElevenLabs voice** (live tested):
- `JarvisDashboard.jsx::speak()` rewired from `window.speechSynthesis` → `POST /speech/text-to-speech`
- Backend route returns base64-encoded MP3 (ElevenLabs) or WAV (pyttsx3 fallback)
- Frontend decodes → `new Audio('data:audio/mpeg;base64,...')` → play
- `currentAudioRef` + updated `stopSpeaking()` for mid-speech stop
- Browser-TTS fallback kept for offline resilience
- Verified: `/speech/text-to-speech` returned 25KB MP3 via ElevenLabs engine

**Phase 5 — Launch + runbook**:
- `app/scripts/launch-demo.ps1` — spawns backend + frontend + clap listener, opens browser
- `app/scripts/stop-demo.ps1` — kills by port + command-line match
- `docs/demo-runbook.md` — pre-demo checklist, 3-question script, fallback table

**UX fix during session**: floating command-bar (bottom-center pill) replaced the cramped chat-panel input.

## Key Dependencies
- Python 3.10+, Node.js 18+, git
- API keys: Gemini (free tier OK), ElevenLabs (free tier 10k chars/month)
- Microphone access
- GPU nhẹ để render Three.js 60fps (integrated GPU OK)

## Success Criteria
1. Vỗ tay 2 lần → boot sequence + Arc Reactor sáng lên
2. UI: hologram sphere xoay với particles, waveform khi speaking
3. Hỏi tiếng Anh → Gemini trả lời → ElevenLabs đọc bằng giọng JARVIS
4. Demo chạy được trên 1 máy Windows 10, không crash trong 5 phút demo

## Out of Scope (YAGNI)
- ❌ Multi-user / auth
- ❌ Persistent memory / vector DB
- ❌ Production deployment (chỉ chạy localhost)
- ❌ Test suite đầy đủ — chỉ smoke test
- ❌ Tiếng Việt TTS (English JARVIS voice only)
- ❌ Browser control / smart home plugins (ngoại trừ sẵn có)

## Risks
| Risk | Mitigation |
|------|-----------|
| Repo `my-jarvis` outdated / deps vỡ | Test ngay phase 2, fallback: Julian-Ivanov repo |
| ElevenLabs free tier hết quota giữa demo | Pre-cache TTS cho 10-20 câu phổ biến |
| Clap detection false-positive (tiếng ồn) | Threshold tuning + cooldown 2s |
| Three.js lag trên máy yếu | Giảm particle count 8K → 2K |

## Notes
- Research reports: `plans/reports/research-260421-1557-github-jarvis-repos.md`
- Không tạo git repo mới — clone trực tiếp `my-jarvis` vào CWD
