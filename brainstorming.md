# 🧠 Feature Brainstorming: Multimodal AI Agent

This document tracks feature decisions for the MVP — what we're including, excluding, and why.

---

## ✅ Final Decisions

| Feature | Status | Decision |
| :--- | :--- | :--- |
| **Local LLMs** | ✅ Keep | We have abundant GPU on E2E Networks |
| **PDF Support** | ❌ Exclude | Images only for MVP (PNG/JPG) |
| **JS Sandbox** | ❌ Exclude | Python only — simpler, covers 95% of use cases |
| **RAG/Memory** | ❌ Exclude | Session-only context (store job metadata in Postgres) |
| **Web Access** | ❌ Exclude | No external API calls from sandbox |
| **Voice Mode** | ❌ Exclude | Text input only |
| **Critic Agent** | ✅ Keep | Lightweight linting (ruff/bandit) + LLM review before execution |
| **Interactive UI** | ❌ Exclude | Static charts (PNG) only |
| **IDE Integration** | ❌ Exclude | Web UI only, no VS Code extension |

---

## 📉 Excluded Features (Deferred to Phase 2+)

### 1. PDF Support
- **Original Plan:** Support Images AND PDFs
- **MVP Decision:** ❌ **Images only (PNG/JPG)**
- **Reason:** PDF parsing is complex (multi-page, OCR quality, tables). Users can screenshot PDFs for now.
- **Phase 2:** Add PyMuPDF + Tesseract pipeline when core is stable.

### 2. Multi-Language Sandbox (JS)
- **Original Plan:** Python AND JavaScript execution
- **MVP Decision:** ❌ **Python only**
- **Reason:** One runtime = simpler security, fewer dependencies. Python handles 95% of data analysis.
- **Phase 2:** Consider JS if users request interactive web components.

### 3. Vector Memory (RAG)
- **Original Plan:** Store embeddings in pgvector for semantic search
- **MVP Decision:** ❌ **Session-only memory**
- **Reason:** RAG adds embedding pipelines, chunking, retrieval tuning. Each conversation is self-contained.
- **Keeping:** Job history stored in Postgres (metadata only, not embeddings).
- **Phase 2:** Add RAG when users need cross-session context.

### 4. Controlled Web Access
- **Original Plan:** Allow agent to search web for real-time data
- **MVP Decision:** ❌ **No external network access**
- **Reason:** Breaks sandbox security model. Would need careful allow-listing.
- **Phase 2:** Consider Tavily/SerpAPI integration with strict controls.

### 5. Voice Interface
- **Original Plan:** Whisper (STT) + Coqui (TTS)
- **MVP Decision:** ❌ **Text only**
- **Reason:** Orthogonal to core value prop. Adds latency and dependencies.
- **Phase 2:** Cool feature but low priority.

### 6. Interactive UI Generation
- **Original Plan:** Generate React/Recharts components that render in chat
- **MVP Decision:** ❌ **Static PNG charts only**
- **Reason:** Requires JS sandbox (excluded) and dynamic frontend rendering.
- **Phase 2:** Consider when JS sandbox is added.

### 7. IDE Integration (VS Code Extension)
- **Original Plan:** VS Code extension to access local project files
- **MVP Decision:** ❌ **Web UI only**
- **Reason:** VS Code extensions are a separate product. Stay focused.
- **Phase 2+:** Potential future expansion.

---

## ✅ Features We're Keeping

### 1. Local LLMs (Self-Hosted)
- **Status:** ✅ **Keeping**
- **Models:** Qwen2.5-VL, Mistral-7B, DeepSeek-Coder via vLLM
- **Reason:** User has abundant GPU on E2E Networks. Self-hosting = privacy + control.

### 2. Critic Agent (Code Review Before Execution)
- **Status:** ✅ **Keeping (Lightweight)**
- **Implementation:**
  - Static analysis: `ruff` (linting) + `bandit` (security)
  - Optional: LLM review prompt before sandbox execution
- **Reason:** Low-effort, high-value. Catches bugs before sandbox runs, reduces failures.

---

## 🎯 MVP Scope Summary

```
INPUT:  PNG/JPG images + text prompts
         ↓
VISION: Qwen2.5-VL extracts content
         ↓
REASON: Mistral-7B plans steps
         ↓
CODE:   DeepSeek-Coder generates Python
         ↓
CRITIC: ruff + bandit + optional LLM review
         ↓
SANDBOX: Python execution (2 CPU, 2GB RAM, 120s, no network)
         ↓
OUTPUT: Static charts (PNG), CSVs, text analysis
```

---

## 📝 Why We Made These Decisions

### The Goal: Ship Without Roadblocks

We made these exclusions to **reduce complexity and avoid over-engineering** the MVP. Each excluded feature was evaluated on:

1. **Roadblock Risk:** Does this add significant complexity that could block progress?
2. **Value vs. Effort:** Is the benefit worth the implementation cost for v1?
3. **Core to Mission:** Is this essential for "image → analysis → code → results"?

### Summary of Rationale

| Exclusion | Primary Reason |
|-----------|----------------|
| PDF Support | Complex parsing pipeline (OCR, multi-page, tables) |
| JS Sandbox | Double the security surface, double the dependencies |
| RAG Memory | Embedding pipelines are a project within a project |
| Web Access | Breaks "no network egress" sandbox security rule |
| Voice Mode | Cool but orthogonal — doesn't help core loop |
| Interactive UI | Needs JS sandbox which we excluded |
| IDE Extension | Separate product, not core focus |

### What We Keep

| Feature | Why Keep It |
|---------|-------------|
| Local LLMs | User has GPU + it's the differentiator (privacy, control) |
| Critic Agent | Low-effort, high-value safety improvement |

### The Philosophy

> **"Ship fast, but ship smart."**
> 
> Start with the simplest thing that works end-to-end. Add complexity only when real users need it and metrics demand it. Every excluded feature has a clear Phase 2 path.
