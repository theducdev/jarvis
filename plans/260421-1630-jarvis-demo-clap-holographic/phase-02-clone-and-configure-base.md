# Phase 2 — Clone Base Repo + Smoke Test

## Context Links
- Overview: [plan.md](./plan.md)
- Previous: [phase-01](./phase-01-environment-setup.md)

## Overview
- **Priority:** High
- **Status:** Not started
- **Brief:** Clone `harsh-raj00/my-jarvis`, install deps, chạy được demo base trước khi modify.

## Key Insights
- `my-jarvis` stack: React (frontend/) + FastAPI (backend/) + WebSocket
- Dùng Gemini AI (match requirement) + ElevenLabs (match voice requirement)
- Có sẵn VoiceIndicator, WaveformVisualizer, HolographicCore → UI xong
- Chưa có clap detection → phase 3 add

## Implementation Steps

1. **Clone repo vào CWD**
   ```bash
   cd D:/o_E/Desktop/project/jarvis
   git clone https://github.com/harsh-raj00/my-jarvis.git app
   cd app
   ```
   Đặt vào folder `app/` để tách khỏi `plans/` và `docs/`.

2. **Đọc README upstream** để hiểu cấu trúc, env vars, commands.
   - Đặc biệt note: backend port, frontend port, WebSocket endpoint.

3. **Install backend (FastAPI)**
   ```bash
   cd app/backend
   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   ```

4. **Install frontend (React)**
   ```bash
   cd app/frontend
   npm install
   ```

5. **Configure env** — copy API keys từ CWD/.env sang app/backend/.env và app/frontend/.env (theo format upstream yêu cầu).
   ```
   backend/.env:
     GEMINI_API_KEY=...
     ELEVENLABS_API_KEY=...
   ```

6. **Smoke test backend**
   ```bash
   cd app/backend
   uvicorn main:app --reload --port 8000
   ```
   Verify `GET http://localhost:8000/health` (hoặc endpoint có sẵn) → 200 OK.

7. **Smoke test frontend**
   ```bash
   cd app/frontend
   npm run dev
   ```
   Mở browser → thấy Arc Reactor + holographic UI animate.

8. **End-to-end smoke test**
   - Press-to-talk / click mic button
   - Hỏi: "What's the weather?"
   - Verify: Gemini phản hồi + ElevenLabs đọc ra loa

## Related Code Files (read only, upstream)
- `app/backend/main.py` (FastAPI entry)
- `app/backend/websocket_handler.py` (expect WS endpoint)
- `app/frontend/src/components/JarvisScene.tsx` (3D scene)
- `app/frontend/src/components/VoiceIndicator.tsx`

## Todo
- [ ] Clone repo into `app/`
- [ ] Backend venv + deps installed
- [ ] Frontend deps installed
- [ ] `.env` files populated cho cả backend + frontend
- [ ] Backend chạy port 8000 không error
- [ ] Frontend chạy port 3000/5173 không error
- [ ] UI render Arc Reactor + sphere OK
- [ ] Q&A loop hoạt động (voice in → Gemini → voice out)

## Success Criteria
Click mic → hỏi → nghe response. Zero code change ở phase này.

## Risks
- Repo outdated deps → fallback: pin versions từ commit cuối stable; nếu vẫn vỡ, switch sang `Julian-Ivanov/jarvis-voice-assistant` base
- CORS giữa frontend/backend → add middleware `CORSMiddleware` nếu thiếu
- Port conflict → `netstat -ano | findstr :8000`

## Next
→ Phase 3 (integrate clap-trigger)
