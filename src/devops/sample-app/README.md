# Notes App — DevOps Lab Starter

A tiny Flask "notes" web app that carries through the entire
[DevOps Lab](https://albanna-tutorials.com/devops/) course — from a single
container to a monitored, auto-deployed app on a real cloud cluster.

This repo is the **capstone starter**: every file maps to a module so you can
follow along (or compare your own work against it).

---

## What's inside

| Path | Module | Purpose |
|------|--------|---------|
| `app.py`, `requirements.txt` | — | The Flask notes app (`/`, `/add`, `/health`, `/metrics`) |
| `Dockerfile`, `.dockerignore` | 6 | Containerize the app |
| `docker-compose.yml`, `prometheus.yml` | 7 & 11 | Full local stack: app + db + monitoring |
| `tests/test_app.py` | 9 | Tests the CI pipeline runs |
| `k8s/` | 8 | Kubernetes manifests (Secret, db, web) |
| `terraform/main.tf` | 10 | Provision the app with the Docker provider |
| `ansible/` | 10 | Configure a host idempotently |
| `grafana/dashboard.json` | 11 | Golden-signals dashboard to import |
| `.github/workflows/ci.yml` | 9 & 12 | Test → build → publish (deploy is commented) |

The app picks its storage automatically: **in-memory** when run alone, or
**PostgreSQL** when `DATABASE_URL` is set — so every stage below just works.

---

## Quick start by module

### Module 6 — Docker (single container)
```bash
docker build -t notes-app:1.0 .
docker run -d -p 8080:5000 --name notes notes-app:1.0
# open http://localhost:8080   (storage: in-memory)
```

### Module 7 & 11 — Compose (app + db + monitoring)
```bash
docker compose up --build
# app:        http://localhost:8080   (storage: postgres, persists)
# prometheus: http://localhost:9090
# grafana:    http://localhost:3000   (admin / admin)
```
In Grafana, add a Prometheus data source at `http://prometheus:9090`, then
import `grafana/dashboard.json`.

### Module 8 — Kubernetes (Minikube)
```bash
minikube start
docker build -t notes-app:1.0 .
minikube image load notes-app:1.0
kubectl apply -f k8s/
minikube service web
```

### Module 9 — CI/CD
Push to GitHub. The workflow in `.github/workflows/ci.yml` runs `pytest`, then
builds and publishes the image to GHCR on every push to `main`.

### Module 10 — Infrastructure as Code
```bash
# Terraform (needs the notes-app:1.0 image built first)
cd terraform && terraform init && terraform plan && terraform apply

# Ansible (run twice to see idempotency)
cd ../ansible && ansible-playbook playbook.yml
```

### Module 13 — Real cloud
Deploy `k8s/` to a cloud cluster (k3s on a free-tier VM), add a `KUBECONFIG`
GitHub secret, and uncomment the `deploy` job in the workflow for full
auto-deploy. See the [Module 13 guide](https://albanna-tutorials.com/devops/13_cloud.html).

---

## Architecture

```
Developer ──git push──▶ GitHub ──▶ Actions (test ▶ build ▶ push ▶ deploy)
                                              │
                                              ▼
                          Kubernetes:  web (x2) ──▶ db (Postgres)
                                          │
                                   Prometheus ──▶ Grafana
```

## Prerequisites
Docker, and (per module) kubectl + Minikube, Terraform, Ansible, a GitHub
account. All free. Nothing here costs money until the optional cloud bonus.

## Security notes
The passwords in this repo (`secret`) are **demo values**. Never commit real
secrets — use GitHub Secrets, Kubernetes Secrets, or a `.env` file (already
in `.gitignore`).
