# Research Report: GitHub Repositories liên quan đến "Jarvis"

**Date:** 2026-04-21 15:57 (Asia/Bangkok)
**Scope:** Tìm các repo GitHub phổ biến liên quan đến Jarvis AI assistant
**Searches:** 4 WebSearch queries (GitHub topic + voice + Microsoft + LLM agent)

---

## Executive Summary

Hệ sinh thái "Jarvis" trên GitHub chia làm **3 nhóm chính**:
1. **Research-grade (Microsoft JARVIS / HuggingGPT)** — academic LLM-orchestration, kết nối LLM với HuggingFace models.
2. **Personal AI voice assistants** — Python-based, wake-word + STT + LLM + TTS (hầu hết single-dev projects).
3. **Modern agentic Jarvis (2025-2026)** — offline/private, MCP-enabled, RAG + tool-calling, chạy local.

Repo đáng chú ý nhất: `microsoft/JARVIS` (authoritative), `isair/jarvis` (modern private assistant), `Likhithsai2580/JARVIS` (feature-rich 2026).

---

## Top Repositories

### Tier 1 — Flagship / Research

| Repo | Mô tả | Stack |
|------|-------|-------|
| [microsoft/JARVIS](https://github.com/microsoft/JARVIS) | HuggingGPT — LLM controller + HuggingFace expert models. Paper: arxiv 2303.17580. Task planning → model selection → execution → response. | Python, HF Hub, ChatGPT |
| [Cofshine/JARVIS-HuggingGPT](https://github.com/Cofshine/JARVIS-HuggingGPT) | Fork/mirror của Microsoft JARVIS | Python |

### Tier 2 — Modern Private / Agentic Assistants (2025-2026)

| Repo | Điểm nổi bật |
|------|--------------|
| [isair/jarvis](https://github.com/isair/jarvis) | **100% private offline** voice assistant. Memory, location/time awareness, Chrome control, nutrition tracking. Hỗ trợ unlimited MCPs không bị context rot. |
| [llm-guy/jarvis](https://github.com/llm-guy/jarvis) | Wake-word + Qwen local LLM via Ollama + LangChain + TTS. Tool-calling. |
| [rajeshl8/agentjarvis](https://github.com/rajeshl8/agentjarvis) | Autonomous agent — NVIDIA NIM + RAG, Gmail/Calendar analysis, deploy AWS EKS. |
| [gamkers/Project_Jarvis](https://github.com/gamkers/Project_Jarvis) | Voice + text UI, Gemini/Groq Llama3, vector search, task/reminder mgmt. |
| [Likhithsai2580/JARVIS](https://github.com/Likhithsai2580/JARVIS) | Versatile AI assistant, voice + web scraping + ML, 128+ stars, updated March 2026. |

### Tier 3 — Classic Python Voice Assistants

| Repo | Mô tả |
|------|-------|
| [AlexandreSajus/JARVIS](https://github.com/AlexandreSajus/JARVIS) | Voice→Deepgram STT→GPT-3→ElevenLabs TTS, web UI. |
| [saasscaleup/openai-jarvis](https://github.com/saasscaleup/openai-jarvis) | OpenAI Whisper + GPT-3.5-turbo. |
| [Gladiator07/JARVIS](https://github.com/Gladiator07/JARVIS) | Python GUI, OpenWeatherMap + Wolframalpha + Google Calendar. |
| [BolisettySujith/J.A.R.V.I.S](https://github.com/BolisettySujith/J.A.R.V.I.S) | PC control, URL/app opener. |
| [kishanrajput23/Jarvis-Desktop-Voice-Assistant](https://github.com/kishanrajput23/Jarvis-Desktop-Voice-Assistant) | Desktop system-level commands, async. |
| [vannu07/jarvis](https://github.com/vannu07/jarvis) | Python + OpenCV face recognition, Hacktoberfest 2025. |
| [AnubhavChaturvedi-GitHub/jarvis-ai-assistant](https://github.com/AnubhavChaturvedi-GitHub/jarvis-ai-assistant) | Voice + NLP task automation. |
| [atharva-shinde7/JARVIS-AI](https://github.com/atharva-shinde7/JARVIS-AI) | Groq LLM + Cohere, PC control + image gen. |
| [zeeshan020dev/Jarvis-AI-For-Windows-2026](https://github.com/zeeshan020dev/Jarvis-AI-For-Windows-2026) | Windows, Google Gemini API, system automation. |

### Tier 4 — Adjacent / Topic Hubs

- [GitHub Topic: jarvis](https://github.com/topics/jarvis)
- [GitHub Topic: jarvis-ai](https://github.com/topics/jarvis-ai)
- [GitHub Topic: jarvis-assistant](https://github.com/topics/jarvis-assistant)
- [open-jarvis/OpenJarvis](https://github.com/open-jarvis/OpenJarvis) — on-device AI, liên quan Stanford Hazy Research / Scaling Intelligence Lab.

---

## Comparative Analysis

| Tiêu chí | microsoft/JARVIS | isair/jarvis | llm-guy/jarvis | AlexandreSajus/JARVIS |
|----------|------------------|--------------|----------------|----------------------|
| Privacy | Cloud (HF + OpenAI) | **100% local** | Local (Ollama) | Cloud APIs |
| Stack | Python, HF Hub | Python, MCP | Python, LangChain, Ollama | Python, Deepgram/OpenAI/ElevenLabs |
| Agent capability | Multi-model orchestration | Tool-calling via MCP | Tool-calling | Basic voice loop |
| Offline | ❌ | ✅ | ✅ | ❌ |
| Maturity | Research-grade | Production-ish | Hobby | Demo/tutorial |

---

## Recommendations

- Học orchestration / multi-model agents → **microsoft/JARVIS**
- Build private offline assistant có MCP → **isair/jarvis**
- Nghịch local LLM + wake word quick-start → **llm-guy/jarvis**
- Inspire UX / feature set cho dự án cá nhân → **Likhithsai2580/JARVIS**, **gamkers/Project_Jarvis**

---

## Unresolved Questions

1. Dự án `jarvis` tại CWD (`D:\o_E\Desktop\project\jarvis`) là repo mới khởi tạo hay fork từ repo nào? Muốn ref repo cụ thể để inspire?
2. Mục tiêu: voice assistant full, hay LLM-orchestration kiểu HuggingGPT, hay agent-with-tools?
3. Yêu cầu privacy — cần 100% offline local, hay cloud API là OK?
4. Ngôn ngữ/stack ưu tiên (Python / Node / Go)?
