# PHASE 1: Foundation Infrastructure - Complete Implementation Prompt

## 🎯 Project Introduction

I am building a production-grade **Multimodal AI Agent** system that can:
- Process **images (PNG/JPG only)** and text inputs
- Use open-source AI models (Qwen2.5-VL for vision, Mistral-7B for reasoning, DeepSeek-Coder for code)
- Generate **Python code** and execute it safely in a sandboxed environment
- Validate code with a **Critic Agent** (ruff + bandit) before execution

This is an **MVP-first approach**. We start lean and add complexity only when metrics demand it.

---

## ⚠️ CRITICAL MVP CONSTRAINTS

**READ THIS CAREFULLY — These features are EXCLUDED from MVP:**

| Excluded | Reason |
|----------|--------|
| **PDF Support** | Images only (PNG/JPG). Users can screenshot PDFs. |
| **JS Sandbox** | Python only. Simpler security, covers 95% of use cases. |
| **RAG/Memory** | Session-only context. No vector embeddings. |
| **Web Access** | No external network from sandbox. |
| **Voice Mode** | Text input only. |
| **pgvector** | Not using vectors in MVP. |
| **Neo4j** | Use JSON in Postgres for graphs. |

**DO NOT implement any of the above in Phase 1.**

---

## 📚 Reference: Tech Stack (MVP)

### Frontend
- React 18 + TypeScript + Vite
- shadcn/ui + Radix UI + TailwindCSS
- Zustand (state), React Query (data fetching)
- react-hook-form + zod (forms)
- react-dropzone (image upload only)
- @clerk/clerk-react (auth)
- @sentry/react (errors)

### Backend
- FastAPI 0.104+ (Python 3.11)
- SQLAlchemy 2.0 + Alembic
- Pydantic v2
- Celery 5.3 (Redis broker)
- pydantic-settings + python-dotenv
- Pillow (images only — no pymupdf)
- structlog + Sentry SDK

### AI/ML
- LangGraph + LangChain
- Qwen2.5-VL-7B, Mistral-7B-Instruct, DeepSeek-Coder-v1.5
- vLLM for model serving
- Langfuse for LLM tracing

### Databases & Storage
- PostgreSQL 15+ (metadata only, no pgvector for MVP)
- Redis 7+
- MinIO (S3-compatible)

### Sandbox
- Docker 24+ (rootless)
- gVisor/nsjail isolation
- Python 3.11 only (NO Node.js)
- 2 CPU, 2GB RAM, 120s timeout
- No network egress

### Code Validation (Critic Agent)
- ruff (linting)
- bandit (security scanning)
- Optional: LLM review

---

## 📐 Reference: Architecture (MVP)

```
User Browser (React)
      │
      ▼
Traefik (Reverse Proxy + SSL)
      │
      ▼
FastAPI Backend
├── Auth (Clerk JWT)
├── Job Management
├── File Upload (images only)
└── WebSocket updates
      │
      ├───────────────────┐
      ▼                   ▼
   Redis              PostgreSQL
  (Queue)            (Job metadata)
      │
      ▼
Celery Workers
├── Vision (Qwen2.5-VL)
├── Reasoning (Mistral-7B)  
├── Code Gen (DeepSeek)
└── Critic (ruff + bandit)
      │
      ▼
Sandbox (Python only)
├── gVisor isolation
├── No network
└── Resource limits
      │
      ▼
MinIO (outputs) → Results to User
```

---

## 🎯 PHASE 1 OBJECTIVES

Create the foundation infrastructure:

### 1. Docker Compose
- PostgreSQL 15+ (no pgvector extension needed for MVP)
- Redis 7+
- MinIO
- Traefik (reverse proxy)
- FastAPI service
- Frontend service

### 2. FastAPI Backend Skeleton
Following this structure:
```
backend/
├── app/
│   ├── main.py
│   ├── config.py
│   ├── api/v1/
│   │   ├── auth.py
│   │   ├── jobs.py
│   │   ├── files.py (images only!)
│   │   └── health.py
│   ├── models/
│   ├── schemas/
│   ├── core/
│   ├── services/
│   └── critic/  (placeholder for Phase 4)
├── migrations/
└── tests/
```

**File upload MUST reject non-image files:**
```python
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}
ALLOWED_MIMETYPES = {"image/png", "image/jpeg", "image/gif", "image/webp"}
```

### 3. React Frontend Skeleton
```
frontend/src/
├── pages/
│   ├── HomePage.tsx
│   ├── UploadPage.tsx (images only!)
│   ├── JobsPage.tsx
│   └── ResultsPage.tsx
├── components/
│   └── features/upload/ (image upload component)
├── hooks/
├── lib/
└── store/
```

**Upload component MUST:**
- Accept only: PNG, JPG, JPEG, GIF, WEBP
- Reject PDFs with clear error message
- Show preview of uploaded image

### 4. Configuration
- `.env.example` with all required variables
- pydantic-settings for config management
- Clerk auth setup

### 5. Development Utilities
- Makefile with: `dev`, `test`, `build`, `health-check`
- setup.sh for initial setup
- README with instructions

---

## 📄 Expected Deliverables

After completing Phase 1, you should have:

1. **docker-compose.yml** - All services defined with:
   - Pinned versions
   - Health checks
   - Volume mounts
   - Environment variables

2. **Backend files:**
   - `backend/app/main.py` - FastAPI entry point
   - `backend/app/config.py` - Settings with pydantic-settings
   - `backend/app/api/v1/*.py` - API endpoints
   - `backend/app/models/*.py` - SQLAlchemy models
   - `backend/app/schemas/*.py` - Pydantic schemas
   - `backend/app/core/*.py` - Auth, DB, logging
   - `backend/requirements.txt` - Pinned dependencies

3. **Frontend files:**
   - `frontend/src/App.tsx` - Main app
   - `frontend/src/pages/*.tsx` - Page components
   - `frontend/src/components/*` - Reusable components
   - `frontend/package.json` - Dependencies

4. **Configuration:**
   - `.env.example`
   - `Makefile`
   - `README.md`

5. **PHASE_1_COMPLETED.md** documenting:
   - All services and ports
   - How to verify setup
   - API endpoints created
   - Environment variables
   - Known issues/TODOs

---

## ✅ Success Criteria

- [ ] `docker compose up` brings all services online
- [ ] Health check endpoints return 200
- [ ] Can upload PNG/JPG images via API
- [ ] Uploading PDF returns 400 error with clear message
- [ ] Clerk authentication works
- [ ] Database migrations run successfully
- [ ] Frontend loads and shows upload form
- [ ] MinIO stores uploaded files

---

## 🚫 DO NOT

- ❌ Add PDF parsing (pymupdf, tesseract)
- ❌ Add Node.js to sandbox
- ❌ Add RAG/vector search (pgvector, embeddings)
- ❌ Add web access features
- ❌ Add voice input/output
- ❌ Implement the full agent pipeline (Phase 2-4)
- ❌ Implement sandbox execution (Phase 4)

---

## 📝 Additional Notes

### File Validation Code Example

```python
# backend/app/services/file_service.py
from fastapi import UploadFile, HTTPException
import magic  # python-magic for MIME detection

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}
ALLOWED_MIMETYPES = {"image/png", "image/jpeg", "image/gif", "image/webp"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

def validate_image_upload(file: UploadFile) -> None:
    """Validate that uploaded file is an allowed image type."""
    
    # Check extension
    ext = file.filename.split(".")[-1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Allowed: {', '.join(ALLOWED_EXTENSIONS)}. "
                   f"PDF support coming in Phase 2."
        )
    
    # Check MIME type
    content = file.file.read(1024)
    file.file.seek(0)
    mime_type = magic.from_buffer(content, mime=True)
    
    if mime_type not in ALLOWED_MIMETYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file content. Only images are supported."
        )
```

### Frontend Upload Validation

```typescript
// frontend/src/components/features/upload/ImageUpload.tsx
const ACCEPTED_TYPES = {
  'image/png': ['.png'],
  'image/jpeg': ['.jpg', '.jpeg'],
  'image/gif': ['.gif'],
  'image/webp': ['.webp'],
};

// In react-dropzone
const { getRootProps, getInputProps } = useDropzone({
  accept: ACCEPTED_TYPES,
  onDropRejected: (rejectedFiles) => {
    toast.error("Only images are supported. PDF support coming soon!");
  },
});
```

---

## 🚀 Start Implementation

Please implement Phase 1 following all the above specifications. Focus on:

1. Working docker-compose setup
2. Clean FastAPI backend with image-only upload
3. Basic React frontend with image upload
4. Proper error messages when PDFs are rejected
5. Health checks and configuration

When complete, create `PHASE_1_COMPLETED.md` with full documentation.

---

## 📝 Why These Decisions

### Why Images Only?
PDF parsing (OCR, multi-page, tables) is complex. Users can screenshot PDFs for now. Proper PDF support in Phase 2.

### Why Python Only?
Two runtimes = double the security surface. Python covers 95% of data analysis. JS can be added later.

### Why No RAG?
Embedding pipelines are complex. Session-only context is sufficient for MVP. Each job is self-contained.

### Why Critic Agent?
Low-effort, high-value. Catches bugs before sandbox runs. Implemented in Phase 4.

### Philosophy
> "Ship fast, but ship smart." Start with the simplest thing that works end-to-end.