# Product Requirements Document (PRD)

**Project:** Multimodal AI Agent with Vision + Code Execution (self-hosted)  
**Owner:** Naman  
**Last Updated:** January 2026

---

## 1 — Executive Summary

We will build a self-hosted multimodal AI agent that:

- **Accepts images (PNG/JPG) and text** (PDF support deferred to Phase 2)
- **Uses open-source vision+text and code models** (Qwen2.5-VL, Mistral-7B-Instruct, DeepSeek-Coder-v1.5)
- **Runs ReAct-style agent reasoning** to pick tools and compose steps
- **Generates Python code** and executes it inside an isolated sandbox (gVisor/nsjail) to produce charts, analyses, or data outputs
- **Validates code before execution** using static analysis (ruff, bandit) and optional LLM review (Critic Agent)
- **Stores job metadata in PostgreSQL**, uses Redis for caching/queueing, stores files in MinIO (self-hosted S3)
- **Provides observability, error reporting** and an incident protocol that first notifies the user and recommends safe remediations before any automated action

**Primary outcome:** A reliable, auditable pipeline that turns screenshots into reproducible analyses with safe Python code execution.

---

## 2 — Goals and Success Criteria

### Primary Goals

1. Deliver an MVP that runs end-to-end: **upload image → agent reasoning → code generation → sandbox execution → results returned**
2. Prevent host compromise from user-submitted/generated code
3. Provide explainability: traceable steps in Langfuse
4. Use only open-source LLMs and infra we control

### Success Criteria (MVP)

- `docker compose up` brings the stack up on E2E node with GPU
- Upload image (PNG/JPG) → agent returns a valid analysis PNG/CSV within rated limits
- Sandbox blocks network egress by default and enforces CPU/memory/time limits
- Code is validated with ruff + bandit before execution
- Every agent action is logged and visible in tracing (Langfuse)
- Automated tests (unit + contract + integration) pass in CI
- User receives immediate failure notice on any job failure before any auto remediation

### Non-functional Goals

- Mean time to detect failure (MTTD) < 2 minutes for critical services
- Recovery time objective (RTO) for workers: < 5 minutes for restarts
- Baseline model latency targets: LLM inference < 2s for Mistral 7B, Qwen visual step < 3s (on GPU)

---

## 3 — Scope (MVP vs Phases)

### MVP (Phase 1) — 4-6 weeks

**Included:**
- FastAPI backend + LangGraph ReAct skeleton
- Frontend upload UI (React + TS) for **images only** (PNG/JPG)
- Result visualization (static charts via Recharts or embedded PNG)
- Models: deploy Qwen2.5-VL + Mistral-7B + DeepSeek-Coder locally via vLLM
- Celery workers + gVisor sandbox executor for **Python code only**
- Code validation: ruff (linting) + bandit (security) + optional LLM critic
- PostgreSQL (metadata only), Redis, MinIO
- Basic observability: Langfuse traces and Sentry errors

**Explicitly Excluded from MVP:**
| Feature | Reason | Phase 2 Path |
|---------|--------|--------------|
| PDF Support | Complex parsing (OCR, multi-page) | Add pymupdf + tesseract |
| JS Sandbox | Double the security surface | Add if users request |
| RAG/Memory | Embedding pipelines add weeks | Add when users need cross-session context |
| Web Access | Breaks sandbox security | Add with strict allow-listing |
| Voice Mode | Orthogonal to core | Low priority |
| Interactive UI | Needs JS sandbox | After JS added |
| Neo4j | Overkill for MVP | Add when >5 graph features needed |
| pgvector | No RAG = no vectors needed | Add with RAG |

### Phase 2

- Add PDF support (pymupdf + pytesseract)
- Add Neo4j graph store (when >5 features need it)
- Improve sandbox hardening (seccomp + AppArmor profiles)
- Add RAG with pgvector when cross-session memory needed
- Add Qdrant (when >100k vectors) or Meilisearch (when FTS >250ms)

### Phase 3 (Scale & Polish)

- Auto-scaling model hosts and inference routers
- Full SLO/SLA, backup automation, production-grade IaC
- JS sandbox if users request interactive components
- Security audit, pen test, supply-chain scanning

---

## 4 — Constraints, Non-goals, and Assumptions

### Constraints

- Hosting: E2E Networks (you control hosts)
- Licensing: use permissive/open-source models (no vendor lock-in)
- Sandbox must run without nested virtualization (use gVisor/nsjail)
- No external proprietary LLM APIs

### Non-goals

- Not building a hosted SaaS (self-hosted, not multi-tenant in Phase 1)
- Not supporting real-time multi-user collaboration at MVP
- Not building PDF support in MVP
- Not building JS execution in MVP

### Assumptions

- You have at least one GPU-enabled E2E node available
- You will pin versions and maintain lockfiles
- Images are the primary input format for MVP

---

## 5 — System Components

| Component | Purpose | Failure Handling |
|-----------|---------|------------------|
| **Frontend (React+TS)** | Upload UI, job viewer, trace visualizer | Show user-facing message, mark job failed |
| **API (FastAPI)** | Orchestrates flows, enforces auth/RBAC | Return 503, notify user |
| **Agent Layer (LangGraph)** | ReAct decisioning and tool router | Halt execution, present failing plan to user |
| **Vision LLM (Qwen2.5-VL)** | Image understanding and captioning | Notify user, suggest re-upload |
| **Reasoning LLM (Mistral 7B)** | Plan generation and tool orchestration | Reduce chain depth, require human approval |
| **Code LLM (DeepSeek-Coder)** | Python code generation | Deny auto-exec, present code for review |
| **Critic Agent** | Static analysis + optional LLM review | Block execution if issues found |
| **Sandbox (gVisor/nsjail)** | Safe Python execution | Notify user, collect logs |
| **PostgreSQL** | Job metadata and user data | Alert, set read-only mode |
| **Redis** | Cache and queue broker | Restore from snapshot |
| **MinIO** | Object storage for files | Fallback to local SSD |
| **Langfuse** | LLM call traces | Notify ops, fallback to file logging |
| **Sentry** | Error collection | Queue errors for later |

---

## 6 — End-to-End Flow

```
1. User uploads image via frontend → File posted to FastAPI via Traefik

2. FastAPI stores raw file to MinIO and creates job metadata in Postgres

3. FastAPI enqueues job in Celery (Redis broker)

4. Worker pulls job, loads file from MinIO, runs Vision LLM (Qwen) for analysis

5. Vision output + context sent to Mistral (reasoning). LangGraph composes a ReAct plan

6. If plan includes code generation, call DeepSeek-Coder for Python code

7. Critic Agent validates code:
   - ruff (linting)
   - bandit (security)
   - Optional: LLM review

8. If validation passes, submit to sandbox worker. Sandbox executes with:
   - 2 CPU cores, 2GB RAM, 120s timeout
   - No network egress
   - Read-only filesystem + tmpfs

9. Worker writes outputs (charts, CSVs) to MinIO and metadata to Postgres

10. FastAPI updates job state. Frontend polls results.

11. Traces available in Langfuse, errors in Sentry
```

---

## 7 — Incident Protocol

**This is critical and non-negotiable** because the system executes generated code.

### Principle

Every failure affecting user experience or security triggers:

1. **Immediate user-visible notification**
   - UI: job marked FAILED with short explanation
   - Provide reason and link to diagnostics

2. **Do not attempt automated remediation** that could change user data without consent

3. **Provide recommended remediation options:**
   - Why it failed (best-effort diagnosis)
   - Safe next steps (e.g., "retry", "download code and inspect", "request review")
   - Operator action (restart worker, increase memory)
   - Optional auto-retry with user consent

4. **Incident log required** for all failures:
   - Job ID, user ID, timestamps
   - Tool outputs, model outputs, sandbox logs
   - Trace ID and ReAct plan snapshot

---

## 8 — Security & Compliance

- Sandbox default denies network egress
- Code validated with ruff + bandit before execution
- Input validation: images only (PNG, JPG, JPEG, GIF, WEBP)
- Secrets: stored in environment variables, migrate to Vault when team >1
- PII redaction in logs using Presidio patterns
- Container scanning (Trivy + Syft) in CI
- Role-based access via Clerk

---

## 9 — Observability & SLOs

### Tracing
- Langfuse stores LLM call steps and tool outputs (redacted)

### Suggested SLOs
- Job success rate >= 95% for normal inputs
- Median job latency < 10s for simple tasks; P95 < 60s
- Sandbox security alerts: 0 critical incidents

### Alerts
- Worker queue length > threshold
- Model GPU memory > 90% for > 2 min
- Postgres connections near max
- Repeated FAILED job ratio > 5% in 10 minutes

---

## 10 — Acceptance Criteria (MVP)

- [ ] `docker compose up` boots the stack on E2E dev host with GPU
- [ ] Upload a sample chart (PNG) → Agent produces summary + Python plot stored in MinIO
- [ ] Sandbox enforces no network egress and kills runtime > timeout
- [ ] Code is validated with ruff + bandit before execution
- [ ] Langfuse shows trace for the job with tool steps
- [ ] CI pipeline blocks PR merges if tests fail or image scan fails
- [ ] User receives immediate failure notice before any auto remediation

---

## 11 — Build Roadmap

| Week | Focus |
|------|-------|
| **0** | Pin versions, docker-compose baseline, .env.example |
| **1-2** | FastAPI skeleton, auth, health checks, frontend upload (images only), Postgres + Redis + MinIO |
| **3** | Deploy Qwen + Mistral + DeepSeek via vLLM, LangGraph ReAct agent, VisionTool + CodeTool |
| **4** | gVisor sandbox, code validation (ruff + bandit), critic agent |
| **5** | Langfuse + Sentry integration, job traces |
| **6** | CI pipeline, E2E testing, production deployment |

---

## 12 — Why We Made These Decisions

### Why Exclude PDF Support?

PDF parsing involves multi-page handling, scanned vs native PDFs, OCR quality issues, and table extraction. It's a project within a project. Users can screenshot PDFs for MVP — proper support comes in Phase 2.

### Why Python Only (No JS)?

Two runtimes = two sets of security policies, two dependency systems, double the attack surface. Python handles 95% of data analysis use cases. JS can be added in Phase 2 if users need interactive web components.

### Why No RAG/Memory?

RAG requires embedding models, vector databases, chunking logic, and retrieval tuning — each is a sub-project. For MVP, each conversation is self-contained. Job metadata is stored for history, but no semantic search.

### Why Add Critic Agent?

Low-effort, high-value. Running `ruff` and `bandit` on generated code before execution catches bugs and security issues, reducing sandbox failures. Optional LLM review adds another layer.

### Philosophy

> "Ship fast, but ship smart."
> 
> Start with the simplest thing that works end-to-end. Every excluded feature has a clear Phase 2 path when real users need it.
