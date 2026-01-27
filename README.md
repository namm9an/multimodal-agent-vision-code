# Multimodal AI Agent

A self-hosted multimodal AI agent that processes images and generates Python code for analysis.

## Features

- 📸 **Image Analysis** - Upload PNG/JPG images for AI processing
- 🤖 **AI-Powered** - Uses Qwen2.5-VL, Mistral-7B, and DeepSeek-Coder
- 🐍 **Python Code Generation** - Generates and executes Python safely
- 🔒 **Secure Sandbox** - Isolated code execution with resource limits
- 🔐 **Authentication** - Clerk-powered login (Google, GitHub, Email)

## Tech Stack

- **Backend:** FastAPI, Celery, PostgreSQL, Redis
- **Frontend:** React, TypeScript, Vite, TailwindCSS
- **AI:** LangGraph, vLLM (E2E Networks)
- **Auth:** Clerk

## Quick Start

### Prerequisites

- Docker & Docker Compose
- Node.js 18+
- Python 3.11+

### Setup

```bash
# Clone and enter directory
cd multimodal-agent

# Copy environment file
cp .env.example .env
# Edit .env with your credentials

# Start all services
make dev

# Open in browser
open http://localhost:3000
```

### Development Commands

```bash
make dev          # Start all services
make stop         # Stop all services
make logs         # View logs
make health       # Check service health
make test         # Run tests
make lint         # Run linters
make clean        # Remove containers and volumes
```

## Project Structure

```
multimodal-agent/
├── backend/          # FastAPI application
├── frontend/         # React application
├── sandbox/          # Code execution sandbox
├── models/           # LLM configurations
├── scripts/          # Utility scripts
└── docker-compose.yml
```

## Environment Variables

See `.env.example` for all required variables.

## Documentation

- [PRD](../prd.md) - Product Requirements
- [Tech Stack](../techstack.md) - Technology Choices
- [Architecture](../architecturediagram.md) - System Design
- [Implementation Guide](../IMPLEMENTATION_GUIDE.md) - Build Steps

## License

Private - All rights reserved.
