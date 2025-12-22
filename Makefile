.PHONY: install dev-backend dev-frontend dev test lint build

install:
	cd backend && pip install -e ".[dev]"
	cd frontend && npm install

dev-backend:
	cd backend && uvicorn reviewbot.main:app --reload --host 0.0.0.0 --port 8000

dev-frontend:
	cd frontend && npm run dev

dev:
	@echo "Open two terminals and run:"
	@echo "  Terminal 1: make dev-backend"
	@echo "  Terminal 2: make dev-frontend"

test:
	cd backend && pytest -v
	cd frontend && npm run test

lint:
	cd backend && ruff check src/
	cd frontend && npm run lint

build:
	cd frontend && npm run build
