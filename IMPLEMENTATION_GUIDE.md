# 🚀 Implementation Guide

## Strategy: Incremental Building with Documentation

### Why Phases?
- **Context Management:** AI agents have limited memory — granular steps prevent context loss
- **Testability:** Verify each phase works before proceeding
- **Rollback Safety:** Easy to revert if something breaks
- **Clear Progress:** Know exactly what's done and what's next
- **Iteration Safety:** Modular design allows rework without destroying core architecture

---

## 🎯 MVP Scope Reminder

Before implementing, remember our MVP decisions:

| Feature | Status |
|---------|--------|
| **Input** | Images only (PNG/JPG) — no PDF |
| **Execution** | Python only — no JS sandbox |
| **Memory** | Session-only — no RAG/vectors |
| **Validation** | Critic agent (ruff + bandit) |
| **LLMs** | Self-hosted via E2E Networks (Qwen, Mistral, DeepSeek v1.5) |

---

## 🔐 Secrets Management Rules

1. **Never commit secrets to git**
2. All credentials go in `.env` files
3. `.env` files are in `.gitignore`
4. Use `.env.example` for documentation
5. Use pydantic-settings for type-safe config

```bash
# .gitignore must include:
.env
.env.local
.env.*.local
*.pem
*.key
```

---

## Pre-Phase: LLM Infrastructure Setup

Before building the application, we need working LLM endpoints.

### Step 0.1: LLM Node Deployment
- [x] Launch Qwen2.5-VL node on E2E Networks
- [x] Launch Mistral-7B node on E2E Networks
- [x] Launch DeepSeek-Coder node on E2E Networks
- [x] Document API endpoints (see `LLM_CONFIG.md`)
- [ ] Test each endpoint with a simple API call

### Step 0.2: Credentials Setup
- [ ] Create `.env.example` with placeholder values
- [ ] Create `.env` (gitignored) with real credentials
- [ ] Add `.env` to `.gitignore`
- [ ] Verify credentials work with test script

**Deliverable:** Working LLM endpoints we can call from our application

---

## Phase 1: Foundation Infrastructure (Days 1-3)

**Goal:** Basic infrastructure and project skeleton

**Success Criteria:** Run `docker compose up` → Login → Upload PNG → See job created

### Deliverables
- docker-compose.yml with PostgreSQL, Redis, MinIO, Traefik
- FastAPI backend skeleton with health checks
- React frontend with basic routing and Clerk auth
- Image upload (PNG/JPG only) — reject PDFs
- Environment variables and configuration

### Granular Steps

**1.1 Project Skeleton**
- [ ] Initialize git repository
- [ ] Create `.gitignore` with proper exclusions
- [ ] Create `README.md` with setup instructions
- [ ] Create `Makefile` with common commands

**1.2 Environment Configuration**
- [ ] Create `.env.example` with all variables
- [ ] Create `backend/.env.example`
- [ ] Create `frontend/.env.example`
- [ ] Set up pydantic-settings config class

**1.3 Docker Compose - Databases**
- [ ] Add PostgreSQL service (no pgvector for MVP)
- [ ] Add Redis service
- [ ] Add health checks for both
- [ ] Test: `docker compose up postgres redis`

**1.4 Docker Compose - Storage**
- [ ] Add MinIO service
- [ ] Configure default bucket
- [ ] Test: MinIO console accessible

**1.5 Docker Compose - Networking**
- [ ] Add Traefik service
- [ ] Configure routing rules
- [ ] Set up SSL (dev certs initially)

**1.6 FastAPI Backend**
- [ ] Create `backend/Dockerfile`
- [ ] Create `backend/requirements.txt`
- [ ] Create `backend/app/main.py`
- [ ] Create `backend/app/config.py`
- [ ] Add health check endpoints (`/healthz`, `/readyz`)

**1.7 Database Models**
- [ ] Create SQLAlchemy base
- [ ] Create User, Job, File models
- [ ] Set up Alembic migrations
- [ ] Run initial migration

**1.8 API - File Upload**
- [ ] Create file upload endpoint
- [ ] Implement image-only validation (reject PDFs!)
- [ ] Store files in MinIO
- [ ] Test: Upload PNG succeeds, PDF rejected

**1.9 API - Jobs**
- [ ] Create job creation endpoint
- [ ] Create job status endpoint
- [ ] Create job results endpoint

**1.10 Authentication (Clerk)**
- [ ] Set up Clerk project
- [ ] Implement JWT verification middleware
- [ ] Protect API endpoints

**1.11 React Frontend**
- [ ] Create Vite + React + TypeScript project
- [ ] Install shadcn/ui + TailwindCSS
- [ ] Create basic routing
- [ ] Install @clerk/clerk-react
- [ ] Create login/signup pages

**1.12 Frontend - Upload**
- [ ] Create image upload component (react-dropzone)
- [ ] Implement file type validation (images only!)
- [ ] Show upload preview
- [ ] Connect to backend API

**1.13 Frontend - Jobs**
- [ ] Create jobs list page
- [ ] Create job detail page
- [ ] Add polling for job status

**1.14 Phase 1 Integration Test**
- [ ] Full flow: Login → Upload image → See job created
- [ ] Verify all services healthy
- [ ] Document any issues in `WORK_LOG.md`

---

## Phase 2: LLM Integration (Days 4-6)

**Goal:** Connect to E2E Networks LLM endpoints and create agent skeleton

**Success Criteria:** Upload image → Agent processes → Code generated (not executed)

### Deliverables
- Model client classes connecting to E2E endpoints
- Model health checks
- Celery for background job processing
- LangGraph ReAct agent with VisionTool and CodeGenTool
- Job status tracking in UI

### Granular Steps

**2.1 Model Clients**
- [ ] Create model client base class
- [ ] Create Qwen client (vision)
- [ ] Create Mistral client (reasoning)
- [ ] Create DeepSeek client (code gen)
- [ ] Add endpoints from `.env`

**2.2 Model Health Checks**
- [ ] Add `/health/models` endpoint
- [ ] Verify each model responds

**2.3 Model Test UI**
- [ ] Create debug page for model testing
- [ ] Test each model with sample input

**2.4 Celery Setup**
- [ ] Create Celery app configuration
- [ ] Add Celery worker to docker-compose
- [ ] Verify task execution works

**2.5 Agent Pipeline**
- [ ] Create VisionTool class (image analysis)
- [ ] Create CodeGenTool class (Python generation)
- [ ] Set up LangGraph ReAct agent
- [ ] Wire up Mistral for reasoning
- [ ] Connect tools to agent

**2.6 Job Processing**
- [ ] Create Celery task for job processing
- [ ] Connect to agent pipeline
- [ ] Update job status in Postgres
- [ ] Test end-to-end flow

---

## Phase 3: Critic Agent + Sandbox (Days 7-10)

**Goal:** Code validation and secure execution

**Success Criteria:** Image → Analysis → Code → Validate → Execute → Results

### Deliverables
- Critic agent with ruff + bandit
- Docker sandbox with gVisor
- Resource limits (2 CPU, 2GB, 120s, no network)
- Result storage in MinIO
- Results display in UI

### Granular Steps

**3.1 Critic - Linter**
- [ ] Create critic module structure
- [ ] Implement ruff integration
- [ ] Test with valid and invalid code

**3.2 Critic - Security**
- [ ] Implement bandit integration
- [ ] Test with safe and unsafe code

**3.3 Critic - Orchestrator**
- [ ] Combine ruff + bandit into validation pipeline
- [ ] Integrate into agent pipeline

**3.4 Sandbox - Base**
- [ ] Create sandbox Dockerfile
- [ ] Install Python 3.11 + common packages
- [ ] Lock down filesystem

**3.5 Sandbox - Security**
- [ ] Create seccomp profile
- [ ] Configure gVisor/nsjail
- [ ] Set resource limits
- [ ] Disable network egress

**3.6 Sandbox - Execution**
- [ ] Create code runner script
- [ ] Capture stdout/stderr
- [ ] Handle timeouts gracefully

**3.7 Integration**
- [ ] Connect sandbox to agent pipeline
- [ ] Store outputs in MinIO
- [ ] Update job with results

**3.8 Frontend - Results**
- [ ] Display generated charts/outputs
- [ ] Show execution logs
- [ ] Show validation status

---

## Phase 4: Observability + Polish (Days 11-12)

**Goal:** Production-ready monitoring and error recovery

**Success Criteria:** All errors tracked, LLM calls traced, graceful failures

### Deliverables
- Sentry for error tracking
- Langfuse for LLM monitoring
- User notification system
- Error recovery with retry logic
- E2E test suite
- CI/CD pipeline

### Granular Steps

**4.1 Error Tracking**
- [ ] Set up Sentry project
- [ ] Add Sentry to backend + frontend
- [ ] Test error capture

**4.2 LLM Tracing**
- [ ] Set up Langfuse
- [ ] Instrument model calls
- [ ] Verify traces appear

**4.3 Error Handling**
- [ ] Implement error recovery strategies
- [ ] Add retry logic where appropriate
- [ ] Implement user notifications for failures

**4.4 Testing**
- [ ] Write unit tests (>80% coverage)
- [ ] Write integration tests
- [ ] Write E2E tests
- [ ] Set up CI pipeline

**4.5 Deployment**
- [ ] Create production docker-compose
- [ ] Deploy to E2E Networks
- [ ] Verify production health

---

## 📋 Phase Completion Template

After each phase, document in `WORK_LOG.md`:

```markdown
## [Date] - Phase X Completed

**Completed Objectives:**
- [x] Objective 1
- [x] Objective 2

**Files Created:**
- `path/to/file.py` - Description

**Services Running:**
- PostgreSQL on port 5432
- FastAPI on port 8000

**How to Test:**
```bash
make health-check
```

**Known Issues:**
- Issue 1...

**Next Phase Prerequisites:**
- ...
```

---

## 💡 Pro Tips

1. **Always mention MVP constraints** — No PDF, Python only, no RAG
2. **Test between phases** — Don't proceed if previous phase is broken
3. **Keep phases small** — 2-3 days of work maximum
4. **Document immediately** — Update `WORK_LOG.md` after each step
5. **Version control** — Commit after each successful phase
6. **Context retention** — Use checkboxes to track where you left off

---

## 📝 Why This Approach

### Why Granular Steps?
Each step is small enough to complete without errors cascading. If something breaks, you know exactly which step failed.

### Why Critic Agent?
Code validation (ruff + bandit) before sandbox execution catches bugs early. Low-effort, high-value.

### Why Explicit PDF/JS Exclusions?
Prevents accidentally implementing excluded features. Clear constraints = focused implementation.

### Philosophy
> Ship the simplest thing that works end-to-end. Add complexity only when users need it.