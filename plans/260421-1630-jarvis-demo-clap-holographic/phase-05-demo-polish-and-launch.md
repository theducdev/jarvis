# Phase 5 — Demo Polish + One-Shot Launch

## Context Links
- Overview: [plan.md](./plan.md)
- Previous: [phase-04](./phase-04-configure-jarvis-voice.md)

## Overview
- **Priority:** Medium
- **Status:** Not started
- **Brief:** Polish boot animation, tạo 1 script bật hết mọi process, dry-run 5 phút demo, fix glitch lớn.

## Implementation Steps

1. **Tune boot sequence**
   - `JarvisScene.tsx`: khi event `wake` → chạy sequence 3 giây:
     - 0.0s: flash trắng nhẹ
     - 0.3s: Arc Reactor pulse + sound effect (có sẵn trong `my-jarvis`)
     - 1.0s: particle sphere spin-up
     - 2.0s: play cached "Good morning, sir. All systems online."
     - 3.0s: ready listen input

2. **Create `app/scripts/launch-demo.ps1`** (PowerShell, Windows-native)
   ```powershell
   # Starts all 3 processes, logs to separate files
   Start-Process powershell -ArgumentList '-NoExit', '-Command', 'cd app\backend; .venv\Scripts\activate; uvicorn main:app --port 8000' -WindowStyle Minimized
   Start-Sleep -Seconds 2
   Start-Process powershell -ArgumentList '-NoExit', '-Command', 'cd app\frontend; npm run dev' -WindowStyle Minimized
   Start-Sleep -Seconds 3
   Start-Process powershell -ArgumentList '-NoExit', '-Command', 'cd app; python clap-wake-listener.py'
   Start-Sleep -Seconds 2
   Start-Process 'http://localhost:5173'
   Write-Host 'Jarvis demo started. Clap twice to wake.'
   ```

3. **Shutdown script `app/scripts/stop-demo.ps1`**
   ```powershell
   Get-Process | Where-Object { $_.MainWindowTitle -match 'uvicorn|vite|clap' } | Stop-Process -Force
   ```
   Hoặc `taskkill /F /IM python.exe /IM node.exe` nếu single-purpose máy.

4. **Create demo script `docs/demo-runbook.md`**
   - Step-by-step cho demo day:
     - Pre-demo: chạy `launch-demo.ps1` 1 phút trước (warm up models)
     - Intro line: "This is Jarvis, a voice assistant inspired by Iron Man."
     - Clap-clap → show boot
     - Ask 3 prepared questions:
       1. "Jarvis, introduce yourself."
       2. "What is the capital of France?"
       3. "Tell me a joke about engineers."
     - Cue camera on Arc Reactor during speaking (waveform)
     - Graceful end: "Goodbye, sir." → shutdown

5. **Dry run 5-minute demo** — log any issues:
   - [ ] No crash
   - [ ] No awkward silence >3s
   - [ ] Clap works first try
   - [ ] Voice clear qua loa laptop (không qua Bluetooth nếu latency cao)

6. **Fallback demo mode**
   - Nếu mic fail → enable button click-to-wake (ẩn mặc định, Ctrl+W toggle)
   - Nếu ElevenLabs fail → pyttsx3 auto kick in (đã setup phase 4)
   - Nếu network fail → pre-canned responses cho 3 câu demo

## Related Code Files
- **Create:**
  - `app/scripts/launch-demo.ps1`
  - `app/scripts/stop-demo.ps1`
  - `docs/demo-runbook.md`
- **Modify:**
  - `app/frontend/src/components/JarvisScene.tsx` (boot sequence tuning)
  - `app/frontend/src/hooks/use-keyboard-shortcuts.ts` (Ctrl+W fallback)

## Todo
- [ ] Boot sequence 3s polished
- [ ] `launch-demo.ps1` bật được 3 process
- [ ] `stop-demo.ps1` tắt sạch
- [ ] `demo-runbook.md` với 3 câu hỏi prepared
- [ ] Dry run 5 phút: 0 crash
- [ ] Fallback click-to-wake hoạt động
- [ ] Pyttsx3 fallback tested

## Success Criteria
- Từ lúc chạy `launch-demo.ps1` → UI sẵn sàng trong <15s
- Demo 5 phút, 3 câu hỏi, không glitch nghiêm trọng
- Nếu 1 component fail → fallback kick in trong <3s

## Risks
- Windows Defender chặn script → user phải unblock; hoặc chạy manual 3 terminal
- Laptop speaker quá nhỏ → chuẩn bị external speaker USB
- Mic noise floor cao ở phòng demo → re-calibrate threshold on-site 1 phút trước

## Next
→ Done. Nếu thành công, scope mở rộng ở plan riêng (persistent memory, hotword thay vì clap, vv)
