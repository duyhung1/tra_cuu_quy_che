PY ?= backend/.venv/bin/python
BASE_URL ?= http://localhost:8000

.PHONY: help venv dev down seed lint test test-unit eval eval-score fixtures

help:
	@echo "make venv      - create backend virtualenv (Python 3.12) and install deps"
	@echo "make dev       - start the full local stack (postgres, s3, tei, api, worker, web)"
	@echo "make seed      - upload the 3 sample PDFs to the running stack"
	@echo "make lint      - ruff + mypy (backend), eslint + tsc (frontend)"
	@echo "make test      - unit + integration tests (needs Docker for Testcontainers)"
	@echo "make eval      - run the golden set against BASE_URL ($(BASE_URL))"

venv:
	cd backend && python3.12 -m venv .venv && .venv/bin/pip install -U pip && .venv/bin/pip install -e ".[dev]"

dev:
	docker compose up --build -d
	@echo "Web: http://localhost:5173  API: http://localhost:8000/api/v1/docs"

down:
	docker compose down

fixtures:
	cd backend && .venv/bin/python tests/fixtures/make_pdfs.py

seed: fixtures
	curl -sf -X POST $(BASE_URL)/api/v1/documents \
	  $(foreach f,$(wildcard backend/tests/fixtures/pdfs/sample/*.pdf),-F "files=@$(f)") | python3 -m json.tool

lint:
	cd backend && .venv/bin/ruff check app tests && .venv/bin/mypy app
	cd frontend && npx eslint src && npx tsc --noEmit

test:
	cd backend && .venv/bin/pytest
	cd frontend && npx vitest run

test-unit:
	cd backend && .venv/bin/pytest tests/unit

eval:
	cd backend && .venv/bin/python tests/eval/run_eval.py --base-url $(BASE_URL)

eval-score:
	cd backend && .venv/bin/python tests/eval/score.py
