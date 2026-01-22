# 🎯 Step-by-Step Implementation Plan

## Overview

This is a granular, step-by-step plan organized by phases. Each step is small enough to complete without errors cascading into later steps.

---

## Pre-Phase: LLM Infrastructure Setup

Before building the application, we need working LLM endpoints.

### Step 0.1: LLM Node Deployment
- [ ] Launch Qwen2.5-VL node on E2E Networks
- [ ] Launch Mistral-7B node on E2E Networks  
- [ ] Launch DeepSeek-Coder node on E2E Networks
- [ ] Document API endpoints for each model
- [ ] Test each endpoint with a simple API call

### Step 0.2: Credentials Setup
- [ ] Create `.env.example` with placeholder values
- [ ] Create `.env` (gitignored) with real credentials
- [ ] Add `.env` to `.gitignore`
- [ ] Verify credentials work with test script

**Deliverable:** Working LLM endpoints we can call from our application

---

## Phase 1: Foundation Infrastructure (Days 1-3)

### Step 1.1: Project Skeleton
- [ ] Create project directory structure
- [ ] Initialize git repository
- [ ] Create `.gitignore` with proper exclusions
- [ ] Create `README.md` with setup instructions
- [ ] Create `Makefile` with common commands

### Step 1.2: Environment Configuration
- [ ] Create `.env.example` with all variables
- [ ] Create `backend/.env.example`
- [ ] Create `frontend/.env.example`
- [ ] Set up pydantic-settings config class

### Step 1.3: Docker Compose - Databases
- [ ] Add PostgreSQL service (no pgvector for MVP)
- [ ] Add Redis service
- [ ] Add health checks for both
- [ ] Test: `docker compose up postgres redis`
- [ ] Verify connections work

### Step 1.4: Docker Compose - Storage
- [ ] Add MinIO service
- [ ] Configure default bucket
- [ ] Test: MinIO console accessible
- [ ] Verify file upload/download works

### Step 1.5: Docker Compose - Networking
- [ ] Add Traefik service
- [ ] Configure routing rules
- [ ] Set up SSL (dev certs initially)
- [ ] Test: Traefik dashboard accessible

### Step 1.6: FastAPI Backend Skeleton
- [ ] Create `backend/Dockerfile`
- [ ] Create `backend/requirements.txt`
- [ ] Create `backend/app/main.py`
- [ ] Create `backend/app/config.py`
- [ ] Add health check endpoints (`/healthz`, `/readyz`)
- [ ] Test: API responds to health checks

### Step 1.7: Database Models
- [ ] Create SQLAlchemy base
- [ ] Create User model
- [ ] Create Job model  
- [ ] Create File model
- [ ] Set up Alembic migrations
- [ ] Run initial migration

### Step 1.8: API Endpoints - Files
- [ ] Create file upload endpoint
- [ ] Implement image-only validation (reject PDFs!)
- [ ] Store files in MinIO
- [ ] Create file metadata in Postgres
- [ ] Test: Upload PNG succeeds, PDF rejected

### Step 1.9: API Endpoints - Jobs
- [ ] Create job creation endpoint
- [ ] Create job status endpoint
- [ ] Create job results endpoint
- [ ] Test: Can create and query jobs

### Step 1.10: Authentication (Clerk)
- [ ] Set up Clerk project
- [ ] Add Clerk credentials to `.env`
- [ ] Implement JWT verification middleware
- [ ] Protect API endpoints
- [ ] Test: Authenticated requests work

### Step 1.11: React Frontend Skeleton
- [ ] Create Vite + React + TypeScript project
- [ ] Install shadcn/ui
- [ ] Set up TailwindCSS
- [ ] Create basic routing
- [ ] Create layout components

### Step 1.12: Frontend - Auth
- [ ] Install @clerk/clerk-react
- [ ] Create login/signup pages
- [ ] Add auth provider
- [ ] Test: Can log in

### Step 1.13: Frontend - Upload
- [ ] Create image upload component
- [ ] Add drag-and-drop (react-dropzone)
- [ ] Implement file type validation (images only!)
- [ ] Show upload preview
- [ ] Connect to backend API
- [ ] Test: Can upload images from UI

### Step 1.14: Frontend - Jobs
- [ ] Create jobs list page
- [ ] Create job detail page
- [ ] Add polling for job status
- [ ] Test: Can see job status updates

### Step 1.15: Phase 1 Integration Test
- [ ] Full flow: Login → Upload image → See job created
- [ ] Verify all services healthy
- [ ] Document any issues in WORK_LOG.md

**Phase 1 Deliverable:** Working web app where you can upload images and see jobs created

---

## Phase 2: LLM Integration (Days 4-6)

### Step 2.1: Model Client Setup
- [ ] Create model client base class
- [ ] Create Qwen client (vision)
- [ ] Create Mistral client (reasoning)
- [ ] Create DeepSeek client (code gen)
- [ ] Add to config with endpoints from `.env`

### Step 2.2: Model Health Checks
- [ ] Add model health check endpoints
- [ ] Verify each model responds
- [ ] Add to Docker health checks

### Step 2.3: Simple Model Test UI
- [ ] Create debug page for model testing
- [ ] Test vision model with sample image
- [ ] Test reasoning model with sample prompt
- [ ] Test code model with sample request

### Step 2.4: Celery Setup
- [ ] Create Celery app configuration
- [ ] Add Celery worker to docker-compose
- [ ] Create basic test task
- [ ] Verify task execution works

### Step 2.5: Agent Pipeline - Vision Tool
- [ ] Create VisionTool class
- [ ] Implement image analysis with Qwen
- [ ] Test with sample images

### Step 2.6: Agent Pipeline - CodeGen Tool
- [ ] Create CodeGenTool class
- [ ] Implement Python code generation with DeepSeek
- [ ] Test with sample prompts

### Step 2.7: Agent Pipeline - ReAct Agent
- [ ] Set up LangGraph
- [ ] Create ReAct agent skeleton
- [ ] Wire up Mistral for reasoning
- [ ] Connect Vision and CodeGen tools
- [ ] Test simple agent flow

### Step 2.8: Job Processing Task
- [ ] Create Celery task for job processing
- [ ] Connect to agent pipeline
- [ ] Update job status in Postgres
- [ ] Test: Job processes and updates status

### Step 2.9: Phase 2 Integration Test
- [ ] Upload image → Agent processes → Code generated
- [ ] Verify job status updates correctly
- [ ] Document any issues in WORK_LOG.md

**Phase 2 Deliverable:** Upload image → AI analyzes and generates Python code (not executed yet)

---

## Phase 3: Critic Agent + Sandbox (Days 7-10)

### Step 3.1: Critic Agent - Linter
- [ ] Create critic module structure
- [ ] Implement ruff integration
- [ ] Test with valid and invalid code

### Step 3.2: Critic Agent - Security
- [ ] Implement bandit integration
- [ ] Test with safe and unsafe code samples

### Step 3.3: Critic Agent - Orchestrator
- [ ] Create validation pipeline
- [ ] Combine ruff + bandit checks
- [ ] Return structured validation result
- [ ] Integrate into agent pipeline

### Step 3.4: Sandbox - Base Image
- [ ] Create sandbox Dockerfile
- [ ] Install Python 3.11 + common packages
- [ ] Lock down filesystem
- [ ] Test container builds

### Step 3.5: Sandbox - Security Profiles
- [ ] Create seccomp profile
- [ ] Create gVisor/nsjail config
- [ ] Set resource limits (2 CPU, 2GB, 120s)
- [ ] Disable network egress

### Step 3.6: Sandbox - Execution Service
- [ ] Create sandbox execution service
- [ ] Implement code runner script
- [ ] Capture stdout/stderr
- [ ] Handle timeouts gracefully
- [ ] Return execution results

### Step 3.7: Sandbox Integration
- [ ] Connect sandbox to agent pipeline
- [ ] Store outputs in MinIO
- [ ] Update job with results
- [ ] Test full flow

### Step 3.8: Result Display
- [ ] Frontend: Display generated charts/outputs
- [ ] Frontend: Show execution logs
- [ ] Frontend: Show validation status

### Step 3.9: Phase 3 Integration Test
- [ ] Full flow: Image → Analysis → Code → Validate → Execute → Results
- [ ] Test with code that should fail validation
- [ ] Test with code that times out
- [ ] Document any issues in WORK_LOG.md

**Phase 3 Deliverable:** Complete working pipeline with safe code execution

---

## Phase 4: Observability + Polish (Days 11-12)

### Step 4.1: Error Tracking
- [ ] Set up Sentry project
- [ ] Add Sentry to backend
- [ ] Add Sentry to frontend
- [ ] Test error capture

### Step 4.2: LLM Tracing
- [ ] Set up Langfuse
- [ ] Instrument model calls
- [ ] Verify traces appear

### Step 4.3: User Notifications
- [ ] Implement job failure notifications
- [ ] Show remediation options
- [ ] Test failure flows

### Step 4.4: Error Handling
- [ ] Implement error recovery strategies
- [ ] Add retry logic where appropriate
- [ ] Test graceful degradation

### Step 4.5: Final Testing
- [ ] Run full E2E tests
- [ ] Fix any remaining issues
- [ ] Update documentation

**Phase 4 Deliverable:** Production-ready MVP with observability

---

## Checklist Summary

| Phase | Steps | Focus |
|-------|-------|-------|
| Pre-Phase | 0.1 - 0.2 | LLM nodes + credentials |
| Phase 1 | 1.1 - 1.15 | Foundation: Docker, API, Frontend |
| Phase 2 | 2.1 - 2.9 | LLM integration + Agent |
| Phase 3 | 3.1 - 3.9 | Critic + Sandbox |
| Phase 4 | 4.1 - 4.5 | Observability + Polish |

---

## Secrets Management Rules

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
