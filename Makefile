.PHONY: dev stop logs health test lint clean build setup

# Colors for output
GREEN := \033[0;32m
NC := \033[0m # No Color

#------------------------------------------------------------------------------
# Development
#------------------------------------------------------------------------------

dev: ## Start all services for development
	@echo "$(GREEN)Starting all services...$(NC)"
	docker compose up -d
	@echo "$(GREEN)Services started! Open http://localhost:3000$(NC)"

stop: ## Stop all services
	@echo "$(GREEN)Stopping all services...$(NC)"
	docker compose down

restart: stop dev ## Restart all services

logs: ## View logs from all services
	docker compose logs -f

logs-backend: ## View backend logs only
	docker compose logs -f backend

logs-frontend: ## View frontend logs only
	docker compose logs -f frontend

logs-worker: ## View Celery worker logs
	docker compose logs -f celery-worker

#------------------------------------------------------------------------------
# Health Checks
#------------------------------------------------------------------------------

health: ## Check health of all services
	@echo "$(GREEN)Checking service health...$(NC)"
	@echo "PostgreSQL:"
	@docker compose exec -T postgres pg_isready -U agent_user -d multimodal_agent || echo "Not ready"
	@echo "\nRedis:"
	@docker compose exec -T redis redis-cli ping || echo "Not ready"
	@echo "\nBackend API:"
	@curl -s http://localhost:8000/healthz || echo "Not ready"
	@echo "\nFrontend:"
	@curl -s http://localhost:3000 > /dev/null && echo "OK" || echo "Not ready"

#------------------------------------------------------------------------------
# Testing
#------------------------------------------------------------------------------

test: ## Run all tests
	@echo "$(GREEN)Running backend tests...$(NC)"
	docker compose exec backend pytest -v
	@echo "$(GREEN)Running frontend tests...$(NC)"
	cd frontend && npm test

test-backend: ## Run backend tests only
	docker compose exec backend pytest -v

test-frontend: ## Run frontend tests only
	cd frontend && npm test

test-e2e: ## Run end-to-end tests
	cd tests && pytest e2e/ -v

#------------------------------------------------------------------------------
# Linting & Formatting
#------------------------------------------------------------------------------

lint: ## Run all linters
	@echo "$(GREEN)Linting backend...$(NC)"
	docker compose exec backend ruff check .
	docker compose exec backend mypy .
	@echo "$(GREEN)Linting frontend...$(NC)"
	cd frontend && npm run lint

format: ## Format all code
	@echo "$(GREEN)Formatting backend...$(NC)"
	docker compose exec backend ruff format .
	@echo "$(GREEN)Formatting frontend...$(NC)"
	cd frontend && npm run format

#------------------------------------------------------------------------------
# Database
#------------------------------------------------------------------------------

db-migrate: ## Run database migrations
	docker compose exec backend alembic upgrade head

db-revision: ## Create new migration (usage: make db-revision MSG="add users table")
	docker compose exec backend alembic revision --autogenerate -m "$(MSG)"

db-shell: ## Open PostgreSQL shell
	docker compose exec postgres psql -U agent_user -d multimodal_agent

#------------------------------------------------------------------------------
# Setup & Build
#------------------------------------------------------------------------------

setup: ## Initial project setup
	@echo "$(GREEN)Setting up project...$(NC)"
	cp -n .env.example .env 2>/dev/null || true
	docker compose build
	@echo "$(GREEN)Setup complete! Run 'make dev' to start.$(NC)"

build: ## Build all Docker images
	docker compose build --no-cache

clean: ## Remove all containers, volumes, and build artifacts
	@echo "$(GREEN)Cleaning up...$(NC)"
	docker compose down -v --remove-orphans
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "node_modules" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true

#------------------------------------------------------------------------------
# Help
#------------------------------------------------------------------------------

help: ## Show this help message
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(GREEN)%-15s$(NC) %s\n", $$1, $$2}'

.DEFAULT_GOAL := help
