# Multimodal AI Agent

[![CI](https://github.com/namm9an/multimodal-agent-vision-code/actions/workflows/ci.yml/badge.svg)](https://github.com/namm9an/multimodal-agent-vision-code/actions/workflows/ci.yml)

A self-hosted multimodal AI agent that processes images and generates Python code for analysis.

## Features

- 📸 **Image Analysis** - Upload PNG/JPG images for AI processing
- 🤖 **AI-Powered** - Uses Qwen2.5-VL, Llama-3.1-8B, and DeepSeek-Coder
- 🐍 **Python Code Generation** - Generates and executes Python safely
- 🔒 **Secure Sandbox** - Isolated code execution with resource limits
- 🔐 **Authentication** - Clerk-powered login (Google, GitHub, Email)
- ⚡ **Redis Caching** - Optimized performance with intelligent caching
- 📊 **Error Tracking** - Sentry integration for production monitoring

## Tech Stack

- **Backend:** FastAPI, Celery, PostgreSQL, Redis, LangGraph
- **Frontend:** React, TypeScript, Vite, TailwindCSS
- **AI:** Qwen2.5-VL, Llama-3.1-8B, DeepSeek-Coder (E2E Networks)
- **Auth:** Clerk
- **CI/CD:** GitHub Actions

## Quick Start

### Prerequisites

- Docker & Docker Compose
- Node.js 20+
- Python 3.11+

### Setup

```bash
# Clone the repository
git clone https://github.com/namm9an/multimodal-agent-vision-code.git
cd multimodal-agent-vision-code

# Copy environment file
cp .env.example .env
# Edit .env with your credentials (API keys, Clerk, etc.)

# Start all services
docker compose up -d

# Open in browser
open http://localhost:3000
```

### Development Commands

```bash
docker compose up -d      # Start all services
docker compose down       # Stop all services
docker compose logs -f    # View logs
make health               # Check service health
make test                 # Run tests
make lint                 # Run linters
```

## Project Structure

```
├── backend/              # FastAPI application
│   ├── app/
│   │   ├── adapters/     # LLM client adapters
│   │   ├── agents/       # LangGraph agent + tools
│   │   ├── api/          # REST endpoints
│   │   ├── core/         # Cache, DB, logging
│   │   ├── critic/       # Code validation
│   │   └── workers/      # Celery tasks
│   └── Dockerfile
├── frontend/             # React application
│   ├── src/
│   │   ├── components/   # UI components
│   │   └── pages/        # Page components
│   └── Dockerfile
├── sandbox/              # Code execution sandbox
│   ├── Dockerfile
│   └── seccomp-profile.json
└── docker-compose.yml
```

## Environment Variables

See `.env.example` for all required variables including:
- `E2E_API_TOKEN` - E2E Networks API token
- `CLERK_*` - Clerk authentication keys
- `DATABASE_URL` - PostgreSQL connection
- `REDIS_URL` - Redis connection

## API Documentation

When running locally, API docs available at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## License

Private - All rights reserved.

