# Tech Stack - Multimodal AI Agent (MVP-First Approach)

## 🎯 Philosophy
Start lean, scale deliberately. Add complexity only when metrics demand it.

---

## 📦 MVP Stack (Weeks 1-4)

### Frontend
- **Framework:** React 18 + TypeScript + Vite
- **UI Components:** shadcn/ui + Radix UI  
- **Styling:** TailwindCSS
- **State Management:** Zustand
- **Data Fetching:** React Query v5
- **Forms/Validation:** react-hook-form + zod
- **File Upload:** react-dropzone (images only: PNG/JPG)
- **Auth Client:** @clerk/clerk-react
- **Error Tracking:** @sentry/react

### Backend
- **Framework:** FastAPI 0.104+ (Python 3.11)
- **ORM:** SQLAlchemy 2.0 + Alembic
- **Schema Validation:** Pydantic v2
- **Background Tasks:** Celery 5.3 (Redis broker)
- **Config/Secrets:** pydantic-settings + python-dotenv (with abstraction layer)
- **Rate Limiting:** fastapi-limiter (Redis-backed)
- **Logging:** structlog + OpenTelemetry basics
- **Error Tracking:** Sentry SDK
- **File Parsing:** Pillow (image processing only — PDF deferred to Phase 2)

### AI/ML Stack (Open Source Only)
- **Agent Framework:** LangGraph + LangChain
- **Vision Model:** Qwen2.5-VL-7B (`Qwen/Qwen2.5-VL` from HuggingFace)
- **Reasoning Model:** Mistral-7B-Instruct-v0.3 (`mistralai/Mistral-7B-Instruct-v0.3`)
- **Code Generation:** DeepSeek-Coder-7B-v1.5 (`deepseek-ai/deepseek-coder-7b-instruct-v1.5`)
- **Model Serving:** vLLM 0.5+ (production) / Transformers (development)
- **Guardrails:** Pydantic + JSON Schema validation
- **LLM Observability:** Langfuse

### Databases & Storage
- **Primary DB:** PostgreSQL 15+ (pgvector extension available but not used in MVP)
- **Cache/Queue:** Redis 7+
- **Object Storage:** MinIO (S3-compatible, self-hosted)

### Code Execution Sandbox
- **Container Runtime:** Docker 24+ (rootless mode)
- **Isolation:** gVisor (runsc) or nsjail
- **Security:** seccomp profiles + AppArmor
- **Resource Limits:** 
  - CPU: 2 cores
  - Memory: 2GB
  - Timeout: 120 seconds
  - Disk: 100MB tmpfs
- **Network:** Deny all egress by default
- **Filesystem:** Read-only base + tmpfs for /tmp
- **Languages:** Python 3.11 only (JS deferred to Phase 2)

### Code Validation (Critic Agent)
- **Static Linting:** ruff (fast Python linter)
- **Security Scanning:** bandit (security issue detection)
- **Optional:** LLM review prompt before execution

### Observability (Minimal MVP)
- **Errors:** Sentry
- **LLM Traces:** Langfuse
- **Logs:** structlog → stdout → Docker logs
- **Metrics:** FastAPI built-in + custom counters
- **Health Checks:** /healthz, /readyz endpoints

### DevOps & CI/CD
- **Local Dev:** docker-compose
- **CI:** GitHub Actions (test, lint, security scan)
- **Registry:** GitHub Container Registry (GHCR)
- **Deployment:** docker-compose on E2E Networks GPU node
- **Reverse Proxy:** Traefik (with Let's Encrypt)
- **Security Scanning:** Trivy for containers

---

## � Explicitly Excluded from MVP

| Feature | Excluded Component | Reason | Phase 2 Path |
|---------|-------------------|--------|--------------|
| PDF Support | pymupdf, pytesseract | Complex parsing pipeline | Add when core is stable |
| JS Sandbox | Node.js 18, npm packages | Double the security surface | Add if users request |
| RAG/Memory | sentence-transformers, pgvector | Embedding pipelines add complexity | Add when users need it |
| Web Access | Tavily, SerpAPI | Breaks sandbox security | Add with strict allow-listing |
| Voice Mode | Whisper, Coqui TTS | Orthogonal to core | Low priority |
| Interactive UI | Dynamic React rendering | Needs JS sandbox | After JS sandbox added |

---

## �📊 Phase 2 Additions (Trigger-Based)

### Service Addition Triggers

| Component | MVP Solution | Scale To | When to Upgrade |
|-----------|-------------|----------|-----------------|
| **Vector DB** | Not used (skip for MVP) | pgvector → Qdrant | When RAG is needed |
| **Text Search** | PostgreSQL FTS | Meilisearch | FTS >250ms OR need faceted search |
| **Graph Store** | JSON in Postgres | Neo4j | >5 graph features OR audit requirements |
| **Monitoring** | Basic logs | Prometheus + Grafana | >2 nodes OR need SLO tracking |
| **Tracing** | Langfuse | + OpenTelemetry Tempo | Distributed tracing needed |
| **Secrets** | .env files | Vault/Doppler | Team >1 OR compliance requirement |
| **Orchestration** | docker-compose | Kubernetes | >5 services OR multi-node required |
| **Model Router** | Single vLLM | Ray Serve/Triton | >3 models OR A/B testing |

---

## 🏗️ Adapter Pattern Architecture

All external services use adapter patterns for seamless migration:

```python
# Example: Storage Adapter
class StorageAdapter(ABC):
    async def upload(self, file_path: str, content: bytes): ...
    async def download(self, file_path: str) -> bytes: ...

# MVP: MinIO
class MinIOAdapter(StorageAdapter): ...

# Future: Cloudflare R2 when needed
class R2Adapter(StorageAdapter): ...
```

Similar adapters for:
- Secrets Management (env → Vault)
- Object Storage (MinIO → R2)
- Search (Postgres FTS → Meilisearch)

---

## 🔒 Security Requirements

### Non-Negotiable Security Measures
- Sandboxed code execution with gVisor/nsjail
- No network egress from sandbox
- Input validation on all file uploads (images only: PNG, JPG, JPEG, GIF, WEBP)
- Static code analysis before execution (ruff + bandit)
- Secrets abstraction (never hardcoded)
- PII redaction in logs (Presidio patterns)
- Container scanning in CI (Trivy)
- Rate limiting per user/IP
- HTTPS only (Traefik + Let's Encrypt)

---

## 💰 Cost Breakdown

### MVP Monthly Costs
- **E2E GPU Node:** ~$250 (1x A100 40GB or similar)
- **Storage:** ~$20 (included in node)
- **Monitoring:** $0 (self-hosted basics)
- **Auth:** $0-25 (Clerk free tier)
- **Total:** ~$270-300/month

### Per-Job Economics
- Target: <$0.10 per job
- GPU inference: ~$0.05
- Storage/compute: ~$0.02
- Margin: ~$0.03

---

## 🚀 Implementation Priorities

### Week 1: Foundation
1. PostgreSQL setup (no pgvector for MVP)
2. Redis for queuing
3. MinIO for object storage
4. FastAPI skeleton with auth
5. Basic upload UI (images only)

### Week 2: AI Integration
1. Deploy models with vLLM
2. LangGraph ReAct agent
3. Tool implementations (VisionTool, CodeTool)
4. Basic adapter patterns

### Week 3: Execution & Safety
1. Docker sandbox configuration
2. gVisor/nsjail setup
3. Resource limits
4. Code validation (ruff + bandit)
5. Critic agent (optional LLM review)

### Week 4: Polish & Deploy
1. Error handling
2. Langfuse integration
3. E2E testing
4. Production deployment

---

## ✅ Definition of Done (MVP)

- [ ] `docker-compose up` brings entire stack online
- [ ] Upload image (PNG/JPG) → receive analysis/code output
- [ ] Sandbox prevents network access and enforces limits
- [ ] All errors logged to Sentry
- [ ] LLM traces visible in Langfuse
- [ ] Health checks passing
- [ ] E2E test suite green
- [ ] Security scan (Trivy) passing
- [ ] Documentation complete

---

## 📈 Scaling Readiness

Despite the MVP focus, the architecture is ready to scale:
- Adapter patterns prevent vendor lock-in
- Clear metrics trigger service additions
- Skeleton infrastructure ready to enable
- No architectural decisions block future growth

The key: **Ship fast, but ship smart.**

---

## 📝 Why We Made These Decisions

### Excluded Features Rationale

| Feature | Why Excluded |
|---------|-------------|
| **PDF Support** | Complex parsing (OCR, multi-page, tables) is a project within a project |
| **JS Sandbox** | Two runtimes = double security configs, double dependencies |
| **RAG/Memory** | Embedding pipelines, chunking, retrieval tuning adds weeks |
| **Web Access** | Breaks our "no network egress" security guarantee |
| **Voice Mode** | Cool but doesn't help the core image→analysis→code loop |

### Kept Features Rationale

| Feature | Why Kept |
|---------|----------|
| **Local LLMs** | User has GPU on E2E Networks — this is the differentiator |
| **Critic Agent** | Low-effort, high-value — catches bugs before sandbox runs |

### Philosophy

> Start with the simplest thing that works end-to-end. Every excluded feature has a clear Phase 2 path when users need it.