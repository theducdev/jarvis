# Phase 3 — Integrate Clap-Trigger Wake Module

## Context Links
- Overview: [plan.md](./plan.md)
- Previous: [phase-02](./phase-02-clone-and-configure-base.md)

## Overview
- **Priority:** High (feature chính của demo)
- **Status:** Not started
- **Brief:** Port `clap-trigger.py` từ `Julian-Ivanov/jarvis-voice-assistant`, chạy song song backend, emit event "wake" qua WebSocket → frontend play boot sequence.

## Key Insights
- Clap = **energy spike ngắn** (<100ms, amplitude > threshold)
- Double-clap = 2 spikes cách nhau 200ms–800ms
- Dùng `sounddevice` stream 16kHz mono, windowed RMS
- Fire event qua HTTP POST tới backend (đơn giản hơn WS producer từ Python)

## Requirements
- Python module độc lập, chạy background process
- Không block mic khi Web Speech API đang listen
  - → Chạy trên device khác hoặc dùng `loopback` / release device khi user hỏi
  - **Simpler:** dùng cùng device, pause clap listener khi Gemini đang response

## Architecture
```
┌────────────────────────┐         ┌──────────────────┐
│ clap-wake-listener.py  │ POST    │  FastAPI backend │
│  sounddevice stream    │────────▶│  /wake endpoint  │
│  RMS + double-clap     │         └────────┬─────────┘
└────────────────────────┘                  │ WS broadcast
                                            ▼
                                   ┌────────────────────┐
                                   │ React frontend     │
                                   │ play boot sequence │
                                   └────────────────────┘
```

## Related Code Files
- **Create:**
  - `app/clap-wake-listener.py` (entry point)
  - `app/clap-detection/double-clap-detector.py` (logic)
  - `app/clap-detection/audio-stream-reader.py` (sounddevice wrapper)
- **Modify:**
  - `app/backend/main.py` — add `POST /wake` route
  - `app/backend/websocket_handler.py` — broadcast `{"event": "wake"}`
  - `app/frontend/src/components/JarvisScene.tsx` — listen event "wake" → trigger boot animation
- **Reference:** Julian-Ivanov upstream `clap-trigger.py`

## Implementation Steps

1. **Fetch upstream clap-trigger.py**
   ```bash
   curl -o /tmp/clap-trigger-upstream.py \
     https://raw.githubusercontent.com/Julian-Ivanov/jarvis-voice-assistant/main/clap-trigger.py
   ```
   Đọc + hiểu logic.

2. **Create `app/clap-detection/audio-stream-reader.py`** (~60 lines)
   - Wrap `sounddevice.InputStream` ở 16kHz mono
   - Yield window RMS mỗi 50ms
   - Expose `close()` để release device

3. **Create `app/clap-detection/double-clap-detector.py`** (~80 lines)
   - Input: stream of RMS values
   - Detect spike: `rms > threshold` với prev_rms thấp (rising edge)
   - Buffer last spike timestamp
   - Emit `double_clap` event khi 2 spikes trong window 200-800ms
   - Cooldown 2s sau mỗi trigger

4. **Create `app/clap-wake-listener.py`** (~50 lines)
   - Main loop: compose reader + detector
   - Khi double-clap → `requests.post("http://localhost:8000/wake")`
   - Graceful shutdown trên Ctrl+C

5. **Modify backend `main.py`**
   ```python
   from fastapi import FastAPI
   @app.post("/wake")
   async def wake_event():
       await ws_broadcast({"event": "wake", "ts": time.time()})
       return {"ok": True}
   ```

6. **Modify frontend `JarvisScene.tsx`**
   - Subscribe WebSocket message `event === "wake"`
   - Trigger state `setBooting(true)` → play Arc Reactor power-up animation + pulse

7. **Smoke test**
   - Start backend (terminal 1)
   - Start frontend (terminal 2)
   - Start `python app/clap-wake-listener.py` (terminal 3)
   - Clap-clap → UI bật boot sequence

## Todo
- [ ] Fetch + read upstream clap-trigger.py
- [ ] `audio-stream-reader.py` created
- [ ] `double-clap-detector.py` created + unit test với fake RMS stream
- [ ] `clap-wake-listener.py` glue script
- [ ] Backend `/wake` endpoint + WS broadcast
- [ ] Frontend listens `event: wake` → plays boot animation
- [ ] E2E: clap-clap → UI bật sáng

## Success Criteria
- Double-clap từ 1m → UI boot sequence trong <500ms
- Single clap → không trigger
- Nói/tiếng ồn nhẹ → không trigger (threshold đúng)
- Cooldown 2s hoạt động (không trigger lặp liên tục)

## Risks
- **Threshold calibration** — mỗi mic khác nhau. Solution: log RMS 10s lúc start, user clap 3 lần → auto-calibrate threshold = mean(clap_rms) * 0.7
- **Mic device conflict** với Web Speech API — nếu browser chiếm mic exclusive, clap listener fail. Fallback: clap listener dùng device index khác, hoặc tạm pause khi đang hỏi
- **Windows audio driver latency** — WASAPI mode để giảm latency nếu cần

## Security
- `/wake` endpoint: chỉ bind `127.0.0.1`, không expose external
- Không log audio data

## Next
→ Phase 4 (JARVIS voice configuration)
