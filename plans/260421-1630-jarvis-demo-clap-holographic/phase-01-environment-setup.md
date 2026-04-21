# Phase 1 — Environment Setup + API Keys

## Context Links
- Overview: [plan.md](./plan.md)
- Research: `plans/reports/research-260421-1557-github-jarvis-repos.md`

## Overview
- **Priority:** High (blocker cho các phase sau)
- **Status:** Not started
- **Brief:** Cài đặt runtime, lấy API keys, verify mic hoạt động.

## Requirements
- Python 3.10+ (cho clap-trigger + backend)
- Node.js 18+ (frontend React/Three.js)
- Git
- Windows 10 mic permission enabled
- API keys: Gemini + ElevenLabs

## Implementation Steps

1. **Check runtime versions**
   ```bash
   python --version    # >= 3.10
   node --version      # >= 18
   git --version
   ```
   Nếu thiếu → install qua winget: `winget install Python.Python.3.11` / `OpenJS.NodeJS.LTS`

2. **Lấy Gemini API key**
   - Vào https://aistudio.google.com/app/apikey
   - Create API key → save vào secure note
   - Free tier: 60 req/min đủ cho demo

3. **Lấy ElevenLabs API key**
   - Register tại https://elevenlabs.io
   - Profile → API Keys → generate
   - Free tier: 10,000 chars/month (~20 phút speech)

4. **Tạo `.env` template tại CWD**
   ```
   GEMINI_API_KEY=your_key_here
   ELEVENLABS_API_KEY=your_key_here
   ELEVENLABS_VOICE_ID=            # sẽ fill ở phase 4
   CLAP_THRESHOLD=0.5
   CLAP_COOLDOWN_SEC=2.0
   ```
   **KHÔNG commit `.env`** — thêm vào `.gitignore` ngay.

5. **Test mic bằng Python sounddevice**
   ```bash
   pip install sounddevice numpy
   python -c "import sounddevice as sd; print(sd.query_devices())"
   ```
   Verify có input device → note device index.

## Todo
- [ ] Python 3.10+ installed
- [ ] Node.js 18+ installed
- [ ] Gemini API key acquired
- [ ] ElevenLabs API key acquired
- [ ] `.env` file tạo tại CWD (placeholder values)
- [ ] `.gitignore` có `.env`
- [ ] Mic test pass (sounddevice liệt kê được input device)

## Success Criteria
`python -c "import sounddevice"` chạy không lỗi, `.env` có 2 keys, node+npm available.

## Risks
- Windows mic permission bị tắt → Settings → Privacy → Microphone → enable cho Python/terminal
- PowerShell execution policy block pip → `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`

## Next
→ Phase 2 (clone base repo)
