.install: ## Install dependencies
	cd backend && pip install -r requirements.txt
	cd ../frontend && npm install
	cd ../mobile && npm install

.dev: ## Run development servers
	docker-compose up -d

.test: ## Run tests
	cd backend && pytest --cov=src tests/ -v

.lint: ## Run linters
	cd backend && flake8 src tests
	cd backend && mypy src
	cd backend && bandit -r src

.format: ## Format code
	cd backend && black src tests
	cd backend && isort src tests

.clean: ## Clean up
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	cd backend && rm -rf .pytest_cache
	cd backend && rm -rf htmlcov

.docker-build: ## Build Docker images
	docker-compose build

.docker-up: ## Start Docker containers
	docker-compose up -d

.docker-down: ## Stop Docker containers
	docker-compose down

.docker-logs: ## View Docker logs
	docker-compose logs -f backend

.migrate: ## Run database migrations
	docker-compose exec backend alembic upgrade head

.init-db: ## Initialize database
	docker-compose exec backend python init_db.py

.deploy: ## Deploy application
	@echo "Starting deployment..."
	docker-compose -f docker-compose.prod.yml build
	docker-compose -f docker-compose.prod.yml up -d
	docker-compose -f docker-compose.prod.yml exec backend python init_db.py
	@echo "Deployment completed!"

.help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^\.[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sed 's/^\.//g' | awk 'BEGIN {FS = ":.*?## "}; {printf "  make %-15s %s\n", $$1, $$2}'

.DEFAULT_GOAL := help
