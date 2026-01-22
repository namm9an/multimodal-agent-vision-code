# 📁 Project Folder Structure

## Complete Project Layout (MVP)

```
multimodal-agent/
│
├── 📄 README.md                      # Project overview and setup instructions
├── 📄 .env.example                   # Template for environment variables
├── 📄 .gitignore                     # Git ignore patterns
├── 📄 docker-compose.yml             # Main orchestration file
├── 📄 docker-compose.override.yml    # Local development overrides
├── 📄 docker-compose.prod.yml        # Production overrides
├── 📄 Makefile                       # Common commands and shortcuts
│
├── 📁 docs/                          # Documentation
│   ├── 📄 prd.md                     # Product Requirements Document
│   ├── 📄 techstack.md               # Technology Stack
│   ├── 📄 architecturediagram.md     # System Architecture
│   ├── 📄 folder_structure.md        # This file
│   ├── 📄 runbook.md                 # Operational runbook
│   ├── 📄 api_spec.yaml              # OpenAPI specification
│   └── 📄 testing_strategy.md        # Test plan and strategies
│
├── 📁 backend/                       # FastAPI Backend
│   ├── 📄 Dockerfile                 # Backend container definition
│   ├── 📄 requirements.txt           # Python dependencies (pinned)
│   ├── 📄 requirements-dev.txt       # Development dependencies
│   ├── 📄 pyproject.toml             # Python project configuration
│   ├── 📄 alembic.ini                # Database migration config
│   ├── 📄 .env.example               # Backend-specific env template
│   │
│   ├── 📁 app/                      # Main application
│   │   ├── 📄 __init__.py
│   │   ├── 📄 main.py               # FastAPI app entry point
│   │   ├── 📄 config.py             # Configuration with pydantic-settings
│   │   │
│   │   ├── 📁 api/                  # API endpoints
│   │   │   ├── 📄 __init__.py
│   │   │   ├── 📁 v1/               # API version 1
│   │   │   │   ├── 📄 __init__.py
│   │   │   │   ├── 📄 auth.py      # Authentication endpoints
│   │   │   │   ├── 📄 jobs.py      # Job management endpoints
│   │   │   │   ├── 📄 files.py     # File upload/download (images only)
│   │   │   │   └── 📄 health.py    # Health check endpoints
│   │   │   └── 📄 dependencies.py   # Shared dependencies
│   │   │
│   │   ├── 📁 models/               # Database models
│   │   │   ├── 📄 __init__.py
│   │   │   ├── 📄 base.py          # SQLAlchemy base
│   │   │   ├── 📄 user.py          # User model
│   │   │   ├── 📄 job.py           # Job model
│   │   │   └── 📄 file.py          # File metadata model
│   │   │
│   │   ├── 📁 schemas/              # Pydantic schemas
│   │   │   ├── 📄 __init__.py
│   │   │   ├── 📄 user.py          # User schemas
│   │   │   ├── 📄 job.py           # Job schemas
│   │   │   ├── 📄 file.py          # File schemas
│   │   │   └── 📄 common.py        # Shared schemas
│   │   │
│   │   ├── 📁 core/                 # Core functionality
│   │   │   ├── 📄 __init__.py
│   │   │   ├── 📄 auth.py          # JWT verification
│   │   │   ├── 📄 database.py      # Database connection
│   │   │   ├── 📄 exceptions.py    # Custom exceptions
│   │   │   ├── 📄 logging.py       # Logging configuration
│   │   │   └── 📄 security.py      # Security utilities
│   │   │
│   │   ├── 📁 services/             # Business logic
│   │   │   ├── 📄 __init__.py
│   │   │   ├── 📄 job_service.py   # Job management
│   │   │   ├── 📄 file_service.py  # File operations (images only)
│   │   │   └── 📄 user_service.py  # User operations
│   │   │
│   │   ├── 📁 agents/               # LangGraph agents
│   │   │   ├── 📄 __init__.py
│   │   │   ├── 📄 base.py          # Base agent class
│   │   │   ├── 📄 react_agent.py   # ReAct implementation
│   │   │   ├── 📁 tools/           # Agent tools
│   │   │   │   ├── 📄 __init__.py
│   │   │   │   ├── 📄 vision.py    # Vision analysis tool (images only)
│   │   │   │   ├── 📄 code_gen.py  # Code generation tool (Python only)
│   │   │   │   └── 📄 execute.py   # Code execution tool
│   │   │   └── 📁 prompts/         # Prompt templates
│   │   │       ├── 📄 __init__.py
│   │   │       ├── 📄 system.py    # System prompts
│   │   │       └── 📄 tools.py     # Tool descriptions
│   │   │
│   │   ├── 📁 critic/               # Code validation (Critic Agent)
│   │   │   ├── 📄 __init__.py
│   │   │   ├── 📄 linter.py        # ruff integration
│   │   │   ├── 📄 security.py      # bandit integration
│   │   │   ├── 📄 llm_review.py    # Optional LLM code review
│   │   │   └── 📄 validator.py     # Main validation orchestrator
│   │   │
│   │   ├── 📁 adapters/             # Adapter pattern implementations
│   │   │   ├── 📄 __init__.py
│   │   │   ├── 📄 base.py          # Abstract base classes
│   │   │   ├── 📄 secrets.py       # Secrets management (env → Vault)
│   │   │   ├── 📄 storage.py       # Object storage adapters (MinIO)
│   │   │   └── 📄 search.py        # Search adapters (Postgres FTS)
│   │   │
│   │   └── 📁 workers/              # Celery workers
│   │       ├── 📄 __init__.py
│   │       ├── 📄 celery_app.py    # Celery configuration
│   │       ├── 📄 tasks.py         # Task definitions
│   │       └── 📄 sandbox.py       # Sandbox execution (Python only)
│   │
│   ├── 📁 migrations/               # Alembic migrations
│   │   ├── 📄 env.py
│   │   ├── 📄 script.py.mako
│   │   └── 📁 versions/
│   │       └── 📄 001_initial.py
│   │
│   └── 📁 tests/                    # Backend tests
│       ├── 📄 __init__.py
│       ├── 📄 conftest.py          # Pytest fixtures
│       ├── 📁 unit/                # Unit tests
│       ├── 📁 integration/         # Integration tests
│       └── 📁 e2e/                 # End-to-end tests
│
├── 📁 frontend/                     # React Frontend
│   ├── 📄 Dockerfile                # Frontend container
│   ├── 📄 package.json              # Node dependencies
│   ├── 📄 package-lock.json         # Locked dependencies
│   ├── 📄 tsconfig.json             # TypeScript config
│   ├── 📄 vite.config.ts            # Vite configuration
│   ├── 📄 .env.example              # Frontend env template
│   ├── 📄 index.html                # HTML entry point
│   │
│   ├── 📁 public/                   # Static assets
│   │   └── 📄 favicon.ico
│   │
│   ├── 📁 src/                      # Source code
│   │   ├── 📄 main.tsx              # React entry point
│   │   ├── 📄 App.tsx               # Main App component
│   │   ├── 📄 vite-env.d.ts        # Vite types
│   │   │
│   │   ├── 📁 components/           # Reusable components
│   │   │   ├── 📁 ui/              # shadcn/ui components
│   │   │   ├── 📁 common/          # Shared components
│   │   │   └── 📁 features/        # Feature-specific
│   │   │       └── 📁 upload/      # Image upload components
│   │   │
│   │   ├── 📁 pages/               # Page components
│   │   │   ├── 📄 HomePage.tsx
│   │   │   ├── 📄 UploadPage.tsx   # Image upload only
│   │   │   ├── 📄 JobsPage.tsx
│   │   │   └── 📄 ResultsPage.tsx  # Static chart display
│   │   │
│   │   ├── 📁 hooks/               # Custom hooks
│   │   │   ├── 📄 useAuth.ts
│   │   │   ├── 📄 useJobs.ts
│   │   │   └── 📄 useWebSocket.ts
│   │   │
│   │   ├── 📁 lib/                 # Utilities
│   │   │   ├── 📄 api.ts          # API client
│   │   │   ├── 📄 utils.ts        # Helper functions
│   │   │   └── 📄 constants.ts    # Constants
│   │   │
│   │   ├── 📁 store/               # Zustand stores
│   │   │   ├── 📄 authStore.ts
│   │   │   └── 📄 jobStore.ts
│   │   │
│   │   └── 📁 styles/              # Global styles
│   │       └── 📄 globals.css
│   │
│   └── 📁 tests/                   # Frontend tests
│       ├── 📁 unit/
│       └── 📁 e2e/
│
├── 📁 models/                      # ML Models
│   ├── 📄 download_models.sh       # Download script
│   ├── 📄 model_config.yaml        # Model configurations
│   │
│   ├── 📁 vllm/                    # vLLM serving configs
│   │   ├── 📄 Dockerfile           # vLLM container
│   │   ├── 📄 requirements.txt     # vLLM dependencies
│   │   ├── 📄 server.py           # vLLM server script
│   │   └── 📄 config.yaml         # Serving configuration
│   │
│   └── 📁 weights/                 # Model weights (gitignored)
│       ├── 📁 qwen2.5-vl/
│       ├── 📁 mistral-7b/
│       └── 📁 deepseek-coder/
│
├── 📁 sandbox/                     # Code Execution Sandbox (Python only)
│   ├── 📄 Dockerfile.sandbox       # Sandbox container
│   ├── 📄 requirements.txt         # Python packages for sandbox
│   │
│   ├── 📁 profiles/               # Security profiles
│   │   ├── 📄 seccomp.json       # Seccomp profile
│   │   ├── 📄 apparmor.profile   # AppArmor profile
│   │   └── 📄 gvisor_config.yaml # gVisor configuration
│   │
│   └── 📁 scripts/                # Sandbox scripts
│       ├── 📄 runner.py           # Python code runner
│       ├── 📄 validator.py        # Code validation (calls critic)
│       └── 📄 resource_monitor.py # Resource monitoring
│
├── 📁 infra/                       # Infrastructure (Phase 2)
│   ├── 📄 README.md               # When to enable these
│   │
│   ├── 📁 terraform/              # IaC (disabled for MVP)
│   │   ├── 📄 main.tf.disabled
│   │   ├── 📄 variables.tf.disabled
│   │   └── 📄 outputs.tf.disabled
│   │
│   ├── 📁 k8s/                    # Kubernetes (Phase 2)
│   │   ├── 📄 namespace.yaml.disabled
│   │   ├── 📄 deployments.yaml.disabled
│   │   └── 📄 services.yaml.disabled
│   │
│   └── 📁 helm/                   # Helm charts (Phase 2)
│       └── 📁 multimodal-agent/
│
├── 📁 scripts/                     # Utility scripts
│   ├── 📄 setup.sh                # Initial setup script
│   ├── 📄 dev.sh                  # Start development environment
│   ├── 📄 test.sh                 # Run all tests
│   ├── 📄 build.sh                # Build all containers
│   ├── 📄 deploy.sh               # Deploy to production
│   ├── 📄 backup.sh               # Backup databases
│   └── 📄 health_check.sh         # Check service health
│
├── 📁 tests/                       # End-to-end tests
│   ├── 📄 requirements.txt         # Test dependencies
│   ├── 📄 conftest.py             # Shared fixtures
│   │
│   ├── 📁 fixtures/               # Test data
│   │   ├── 📁 images/            # Test images (PNG/JPG only)
│   │   └── 📁 expected/          # Expected outputs
│   │
│   └── 📁 e2e/                    # E2E test suites
│       ├── 📄 test_upload.py      # Image upload tests
│       ├── 📄 test_processing.py
│       ├── 📄 test_sandbox.py     # Python sandbox tests
│       ├── 📄 test_critic.py      # Code validation tests
│       └── 📄 test_full_flow.py
│
├── 📁 .github/                     # GitHub configuration
│   ├── 📁 workflows/              # GitHub Actions
│   │   ├── 📄 ci.yml             # Continuous Integration
│   │   ├── 📄 cd.yml             # Continuous Deployment
│   │   ├── 📄 security.yml       # Security scanning
│   │   └── 📄 codeql.yml         # Code quality analysis
│   │
│   ├── 📁 ISSUE_TEMPLATE/         # Issue templates
│   └── 📄 pull_request_template.md # PR template
│
└── 📁 monitoring/                  # Monitoring configs
    ├── 📄 docker-compose.monitoring.yml # Monitoring stack
    │
    ├── 📁 prometheus/              # Prometheus (Phase 2)
    │   └── 📄 prometheus.yml.disabled
    │
    ├── 📁 grafana/                 # Grafana (Phase 2)
    │   └── 📁 dashboards/
    │
    └── 📁 alerts/                  # Alert rules
        └── 📄 rules.yml
```

---

## Key Directories Explained

### `/backend/app/critic/` (NEW)
Code validation before sandbox execution:
- `linter.py`: Integrates ruff for Python linting
- `security.py`: Integrates bandit for security scanning
- `llm_review.py`: Optional LLM-based code review
- `validator.py`: Orchestrates the validation pipeline

### `/backend/app/agents/`
LangGraph-based agent implementation:
- `react_agent.py`: Main ReAct loop
- `tools/vision.py`: Image analysis (PNG/JPG only)
- `tools/code_gen.py`: Python code generation
- `tools/execute.py`: Sandbox execution trigger

### `/sandbox/`
Isolated Python code execution environment:
- Security profiles for containment
- Resource monitoring and limits
- Python 3.11 runtime only (no Node.js)

---

## Removed from MVP

The following folders/files are **NOT included** in MVP:

| Removed | Why |
|---------|-----|
| `sandbox/package.json` | No JS sandbox |
| `tests/fixtures/pdfs/` | No PDF support |
| `backend/app/agents/tools/search.py` | No RAG |
| `backend/app/adapters/vector_store.py` | No vector search |

---

## Environment Variables Structure

### `.env` (Root)
```bash
# General
ENVIRONMENT=development
DEBUG=true

# Database
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
POSTGRES_DB=multimodal_agent
POSTGRES_USER=agent_user
POSTGRES_PASSWORD=secure_password

# Redis
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_PASSWORD=redis_password

# MinIO
MINIO_ENDPOINT=minio:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin
MINIO_BUCKET=agent-files

# Auth
CLERK_SECRET_KEY=sk_test_xxx
CLERK_PUBLISHABLE_KEY=pk_test_xxx

# Models
VLLM_HOST=vllm
VLLM_PORT=8000
MODEL_PATH=/models/weights

# Observability
SENTRY_DSN=https://xxx@sentry.io/xxx
LANGFUSE_PUBLIC_KEY=pk_xxx
LANGFUSE_SECRET_KEY=sk_xxx

# Critic Agent
CRITIC_ENABLE_LLM_REVIEW=false  # Optional LLM review
```

---

## Why This Structure?

### Why `/backend/app/critic/`?
Centralizes code validation logic. Catches bugs and security issues before sandbox execution. Easy to extend with more checks.

### Why No `/sandbox/package.json`?
No JS sandbox in MVP. Python covers 95% of use cases. Reduces security surface.

### Why No `tests/fixtures/pdfs/`?
No PDF support in MVP. Users can screenshot PDFs. Proper support in Phase 2.

### Philosophy
> Keep the structure simple. Every folder serves a clear purpose. Excluded features have clear Phase 2 paths.