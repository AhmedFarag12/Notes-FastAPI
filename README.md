# FastAPI DevOps Lab

A small production-style Notes REST API built with FastAPI, made to be practiced on with DevOps tools: Docker, CI/CD, Kubernetes, monitoring.

## What it does

- CRUD for notes (`/notes`) backed by SQLAlchemy (SQLite locally, PostgreSQL via `DATABASE_URL`)
- `GET /health` health check for load balancers, Kubernetes probes, and uptime monitors
- `GET /metrics` Prometheus metrics (requests, latency) via prometheus-fastapi-instrumentator
- Interactive API docs at `/docs`
- Automated tests with pytest
- Multi-stage Dockerfile and docker-compose with PostgreSQL

## Stack

Python 3.12, FastAPI, SQLAlchemy 2, Uvicorn, PostgreSQL (compose), pytest.

## Run locally

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
uvicorn app.main:app --reload
```

Open http://localhost:8000/docs

## Run tests

```bash
pytest -v
```

## Run with Docker

```bash
docker build -t notes-api .
docker run -p 8000:8000 notes-api
```

Or the full stack (API + PostgreSQL):

```bash
docker compose up --build
```

## API

| Method | Path | Description |
| ------ | ---- | ----------- |
| GET | /health | Health check |
| GET | /metrics | Prometheus metrics |
| GET | /notes | List notes |
| POST | /notes | Create a note `{ "title": "...", "content": "..." }` |
| GET | /notes/{id} | Get one note |
| PATCH | /notes/{id} | Update a note |
| DELETE | /notes/{id} | Delete a note |

## Configuration

| Variable | Default | Description |
| -------- | ------- | ----------- |
| DATABASE_URL | sqlite:///./notes.db | SQLAlchemy connection string |

## Suggested DevOps practice roadmap

1. Containerize: build and push the image to Docker Hub.
2. CI: add a pipeline (Jenkins or GitHub Actions) that runs `pytest`, then builds and pushes the image on every push to main.
3. Deploy: run it on a VPS with docker-compose, or write Kubernetes manifests (Deployment, Service, liveness/readiness probes against `/health`).
4. Monitoring: add Prometheus scraping `/metrics` and a Grafana dashboard for request rate and latency.
5. IaC: provision the server or cluster with Terraform and configure it with Ansible.
