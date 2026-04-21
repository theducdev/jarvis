# Phase 4 — Configure JARVIS-like Voice (ElevenLabs)

## Context Links
- Overview: [plan.md](./plan.md)
- Previous: [phase-03](./phase-03-integrate-clap-trigger.md)

## Overview
- **Priority:** Medium-High (quan trọng cho demo feel)
- **Status:** Not started
- **Brief:** Chọn voice JARVIS từ ElevenLabs Voice Library (hoặc clone), config backend dùng voice ID đó, pre-cache 10 câu thường dùng để tránh hết quota.

## Key Insights
- ElevenLabs có sẵn community voices "JARVIS-like" (British male, formal, deep)
- Voice cloning từ sample Paul Bettany cần Starter plan ($5/month) — tránh nếu free tier đủ
- Pre-cache greeting lines → tiết kiệm quota + latency thấp hơn

## Requirements
- Voice phải: British accent, formal, calm, slightly robotic edge
- Latency đọc first word <800ms
- Quota-aware — monitor + fallback TTS nếu quota cạn

## Implementation Steps

1. **Explore ElevenLabs Voice Library**
   - Login → Voices → Voice Library
   - Search "JARVIS" hoặc "British butler"
   - Preview → chọn 1 voice → Add to My Voices
   - Copy Voice ID (format `21m00Tcm4TlvDq8ikWAM`)

2. **Update `.env`**
   ```
   ELEVENLABS_VOICE_ID=<paste_id>
   ELEVENLABS_MODEL=eleven_turbo_v2_5   # nhanh nhất, chất lượng đủ
   ELEVENLABS_STABILITY=0.5
   ELEVENLABS_SIMILARITY=0.75
   ```

3. **Verify upstream backend gọi đúng voice ID**
   - Grep code: `grep -rn ELEVENLABS_VOICE_ID app/backend`
   - Nếu hardcoded → replace bằng `os.getenv("ELEVENLABS_VOICE_ID")`

4. **Create pre-cache script `app/scripts/pregenerate-greetings.py`** (~70 lines)
   - Input: list 10 câu trong `app/assets/cached-phrases.txt`:
     ```
     Good morning, sir.
     All systems online.
     How may I assist you today?
     Working on it, sir.
     Task complete.
     Shutting down.
     I'm afraid I don't understand.
     Let me check that for you.
     Right away, sir.
     Welcome back.
     ```
   - Call ElevenLabs `/v1/text-to-speech/{voice_id}` → save mp3 vào `app/assets/voice-cache/`
   - Backend TTS route: check cache trước khi call API

5. **Modify backend TTS handler**
   - Pseudocode:
     ```python
     def speak(text):
         cache_key = hash(text.strip().lower())
         if cache_file := cache_lookup(cache_key):
             return stream_file(cache_file)
         return stream_elevenlabs(text)
     ```

6. **Add quota monitor**
   - ElevenLabs API: `GET /v1/user` → returns `character_count`, `character_limit`
   - Warn if <500 chars left → log WARNING + fallback `pyttsx3` (offline robotic Windows voice)

7. **Test**
   - Nói "Good morning" → expect cached response, latency <200ms
   - Nói câu mới → ElevenLabs, latency <1200ms
   - Verify voice sound đúng JARVIS feel

## Related Code Files
- **Create:**
  - `app/scripts/pregenerate-greetings.py`
  - `app/assets/cached-phrases.txt`
  - `app/assets/voice-cache/.gitkeep`
- **Modify:**
  - `app/backend/tts_service.py` (hoặc file tương đương của upstream)
  - `app/backend/.env`

## Todo
- [ ] Chọn voice từ ElevenLabs Library, copy ID
- [ ] `.env` update với voice ID + model
- [ ] Backend đọc env var (không hardcode)
- [ ] 10 cached phrases generated mp3
- [ ] Cache lookup logic trong TTS handler
- [ ] Quota monitor endpoint `/admin/quota`
- [ ] Pyttsx3 fallback hoạt động khi quota=0
- [ ] Demo test: sound giống JARVIS

## Success Criteria
Hỏi "Good morning" → nghe voice JARVIS <200ms (cached); câu ngẫu nhiên <1200ms.

## Risks
- Voice chọn sai "vibe" — giải pháp: A/B test 3 voices với team trước khi lock
- Quota cạn giữa demo → pyttsx3 fallback đảm bảo demo không chết
- ElevenLabs rate limit (Free: 2 concurrent) → throttle 1 request at a time

## Security
- API key chỉ trong backend `.env`, không expose frontend
- Cached mp3 an toàn commit (không PII)

## Next
→ Phase 5 (demo polish + launch)
