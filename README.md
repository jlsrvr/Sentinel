# Sentinel

A mock Trust & Safety case review platform built to demonstrate the core tooling used by content moderation teams — case queues, review interfaces, enforcement workflows, audit trails, and analyst wellbeing features.

Built to demonstrate the core tooling patterns used by content moderation and trust & safety teams.

---

## Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.12, FastAPI, SQLAlchemy 2.0, Alembic |
| Frontend | React 18, TypeScript, Vite, TanStack Query, shadcn/ui |
| Database | PostgreSQL 16 |
| Testing | Pytest, factory-boy, httpx / Vitest |

---

## Prerequisites

- Node v24+
- Docker
- [uv](https://docs.astral.sh/uv/) (Python toolchain)
- pnpm (`corepack enable pnpm`)

---

## Local Setup

**1. Start the database**
```bash
docker compose up -d
```

**2. Backend**
```bash
cd backend
uv sync
cp .env.example .env   # fill in values
uv run alembic upgrade head
uv run uvicorn main:app --reload
```

**3. Frontend**
```bash
cd frontend
pnpm install
pnpm dev
```

API runs on `http://localhost:8000`
Frontend runs on `http://localhost:5173`
Interactive API docs at `http://localhost:8000/docs`

---

## Features

- Case queue with severity-based routing and skill-based assignment ⏳
- Content review interface with decision and audit logging ⏳
- One-click escalation paths and full decision history per case ⏳
- Role-based permissions (analyst, senior reviewer, policy, admin) ⏳
- Reviewer wellbeing: content blurring, exposure tracking, exposure limits ⏳
- Metrics dashboard: queue health, throughput, average handling time ⏳
- Append-only audit trail on every action ⏳
- Reusable API layer designed for new review workflow onboarding ⏳

---

## Development

Tests:
```bash
cd backend && uv run pytest
cd frontend && pnpm test
```

Linting:
```bash
cd backend && uv run ruff check .
cd frontend && pnpm lint
```
