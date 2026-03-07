.PHONY: dev test lint format typecheck docker-up docker-down docs clean install

# --- Development ---
install:
	pip install -e ".[dev]"

dev:
	PYTHONPATH=src uvicorn agentguard.main:app --reload --host 0.0.0.0 --port 8000

# --- Quality ---
test:
	PYTHONPATH=src pytest tests/ -v --cov=src/agentguard --cov-report=term-missing

lint:
	ruff check src/ tests/

format:
	ruff format src/ tests/

typecheck:
	mypy src/agentguard/

# --- Docker ---
docker-up:
	docker compose up --build -d

docker-down:
	docker compose down

# --- Documentation ---
docs:
	mkdocs serve

docs-build:
	mkdocs build

# --- Cleanup ---
clean:
	rm -rf __pycache__ .pytest_cache .mypy_cache .ruff_cache htmlcov .coverage dist build site
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
