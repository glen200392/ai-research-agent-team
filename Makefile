# AI Research Agent Team — Makefile
# Usage: make <target>
.PHONY: setup detect team-a team-b team-c all api api-prod check clean docker-up docker-local docker-api

# ── First-time setup ──────────────────────────────────────────
setup:
	bash setup.sh

# ── Environment detection ─────────────────────────────────────
detect:
	python run.py detect

# ── Run pipelines ─────────────────────────────────────────────
team-a:
	python run.py team-a

team-b:
	python run.py team-b

team-c:
	python run.py team-c

all:
	python run.py all

# Run for a specific month: make team-a MONTH=2026-02
team-a-month:
	python run.py team-a --month $(MONTH)

all-month:
	python run.py all --month $(MONTH)

# Dry-run (validates config, no API calls)
dry-run:
	python run.py team-a --dry-run

# ── API server ────────────────────────────────────────────────
api:
	uvicorn api.server:app --host 0.0.0.0 --port 8080 --reload

api-prod:
	uvicorn api.server:app --host 0.0.0.0 --port 8080 --workers 2

# ── Syntax / import check ─────────────────────────────────────
check:
	python -c "import ast, sys, pathlib; \
	  files = ['core/providers.py','core/env_detector.py', \
	           'frameworks/langgraph/nodes.py', \
	           'frameworks/langgraph/nodes_team_b.py', \
	           'frameworks/langgraph/nodes_team_c.py', \
	           'run.py','api/server.py']; \
	  [ast.parse(pathlib.Path(f).read_text()) or print(f'  OK {f}') for f in files]" \
	  && echo "All files OK"

# ── Docker ────────────────────────────────────────────────────
docker-up:
	docker compose up app

docker-local:
	docker compose --profile local up

docker-api:
	docker compose --profile api up

docker-build:
	docker compose build

docker-pull-model:
	docker compose exec ollama ollama pull llama3.2

# ── Cleanup ───────────────────────────────────────────────────
clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -name "*.pyc" -delete 2>/dev/null || true
	rm -rf tmp/pipeline/*
