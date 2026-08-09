# Project Evaluation — Rubrics & Validation

This document maps every project requirement to what was built, how to verify it, and what the expected output is.

---

## Part 1 — Web Application (20 points)

### Requirement: Web application with CRUD functionality

| Criterion | What We Built | How to Validate | Expected Output |
|-----------|--------------|-----------------|-----------------|
| Create user | `POST /users` endpoint | Run `docker-compose up` → open http://localhost:3000 → fill form → click Add User | New user row appears in table |
| Read users | `GET /users` and `GET /users/<id>` | Open http://localhost:3000 — table shows all users | List of users displayed |
| Update user | `PUT /users/<id>` endpoint | Click Edit button → change name → Save Changes | Row updates with new value |
| Delete user | `DELETE /users/<id>` endpoint | Click Delete button → confirm | Row disappears from table |
| Health check | `GET /health` endpoint | Open http://localhost:3000/health | `{"status":"ok","database":"healthy"}` |

### Requirement: Storage in database (PostgreSQL)

| Criterion | What We Built | How to Validate | Expected Output |
|-----------|--------------|-----------------|-----------------|
| PostgreSQL database | `userapi_db` via SQLAlchemy | Run `docker-compose up` → open http://localhost:5050 (pgAdmin) | Can browse `users` table |
| Data persists | Docker volume `postgres_data` | Add user → `docker-compose down` → `docker-compose up` → check table | User still there after restart |
| Schema correct | `users` table with 6 columns | pgAdmin → userapi_db → Tables → users → Columns | id, username, email, firstname, lastname, created_at |

### Requirement: Tests (unit, API, configuration, connection)

**Run with:**
```bash
cd userapi
python -m pytest test/ -v
```

| Test File | Type | Tests Count | What It Tests |
|-----------|------|-------------|---------------|
| `test_unit.py` | Unit | 7 | Model validation logic — checks `User.validate()` catches bad input |
| `test_api.py` | API / Functional | 20 | Every HTTP endpoint — create, read, update, delete, error cases |
| `test_config.py` | Configuration | 16 | Config classes load correctly, env vars override defaults |
| `test_connection.py` | Connection | 7 | DB is reachable, table exists, CRUD operations work, constraints enforced |
| **Total** | | **51** | **All pass in 1.5 seconds using SQLite in-memory** |

Expected output:
```
51 passed in 1.5s
```

---

## Part 2 — CI/CD Pipeline (20 points)

### Requirement: Configure CI pipeline with any platform

**Platform used:** GitHub Actions (`.github/workflows/ci.yml`)

| Job | Trigger | What it does | Validation |
|-----|---------|-------------|------------|
| `test` | Every push | Starts PostgreSQL container, runs all 51 tests | Green checkmark in Actions tab |
| `lint` | Every push | Runs flake8 on `src/` and `test/` | No lint errors |
| `docker-build` | After test passes | Builds Docker image | Build succeeds |

**How to validate:**
1. Push code to GitHub
2. Go to repo → **Actions** tab
3. Click the latest workflow run
4. All 3 jobs show green ✓

**Key feature:** The `docker-build` job uses `needs: test` — it only runs if tests pass first. This prevents broken code from being containerized.

---

## Part 3 — Virtual Environment with IaC (20 points)

### Requirement: Configure with Vagrant (1 VM on Linux)

| Criterion | What We Built | Location | Validation |
|-----------|--------------|----------|------------|
| VM with Linux | Ubuntu 22.04 (jammy64) | `iac/Vagrantfile` line 2 | `vagrant up` creates VM in VirtualBox |
| Port forwarding | 3000→3000, 5432→5433 | `iac/Vagrantfile` lines 5-6 | App accessible at http://localhost:3000 |
| Synced folder | `../userapi` → `/home/vagrant/userapi` | `iac/Vagrantfile` line 15 | Code changes on host appear in VM |

### Requirement: Provision with Ansible (language runtime, database, application, health check)

| Ansible Role | Installs / Configures | Location | Validation |
|-------------|----------------------|----------|------------|
| `python` | Python 3, pip, libpq-dev, all requirements | `roles/python/tasks/main.yml` | `python3 --version` inside VM |
| `postgresql` | PostgreSQL 14, creates `userapi_db`, sets password | `roles/postgresql/tasks/main.yml` | `psql -U postgres -c "\l"` inside VM |
| `app` | Installs deps, creates systemd service, starts app | `roles/app/tasks/main.yml` | `systemctl status userapi` → active (running) |
| Health check | `uri` module calls `/health` endpoint | `roles/app/tasks/main.yml` last 2 tasks | Ansible prints `Health check passed: {'status': 'ok'}` |

**How to validate:**
```bash
cd iac
vagrant up                             # provision VM
vagrant ssh                            # connect to VM
systemctl status userapi               # → active (running)
curl http://localhost:3000/health      # → {"status":"ok","database":"healthy"}
exit
```

---

## Part 4 — Docker Image (20 points)

### Requirement: Create a Docker image

| Criterion | What We Built | Location | Validation |
|-----------|--------------|----------|------------|
| Dockerfile | `python:3.11-slim` base, installs deps, copies code | `userapi/Dockerfile` | `docker build` succeeds |
| .dockerignore | Excludes `__pycache__`, `.env`, `.git`, test files | `userapi/.dockerignore` | Image size is minimal |
| Correct structure | Files copied to `./userapi/` subdir for correct imports | `Dockerfile` line 8 | App starts without ImportError |
| Gunicorn server | Production WSGI server with `--preload` | `Dockerfile` last line | App serves requests correctly |

### Requirement: Push image to Docker Hub

**Image:** `kousiksc/userapi:latest`
**URL:** https://hub.docker.com/r/kousiksc/userapi

```bash
# How to build and push:
cd userapi
docker build -t kousiksc/userapi:latest .
docker login
docker push kousiksc/userapi:latest
```

**How to validate:**
```bash
# Pull and run from Docker Hub (proves it works independently)
docker run -e DB_HOST=localhost -p 3000:3000 kousiksc/userapi:latest
```

---

## Part 5 — Kubernetes (20 points)

### Requirement: Install Kubernetes cluster using Minikube

```bash
minikube start --driver=docker --no-vtx-check
minikube status
# host: Running / kubelet: Running / apiserver: Running
```

### Requirement: Create Kubernetes Manifest YAML files

| Manifest | File | What it creates | Validation |
|----------|------|----------------|------------|
| PersistentVolume | `k8s/persistent-volume.yaml` | 1Gi storage on node at `/mnt/data/postgres` | `kubectl get pv` → STATUS: Bound |
| PersistentVolumeClaim | `k8s/persistent-volume-claim.yaml` | Reserves the PV for PostgreSQL | `kubectl get pvc` → STATUS: Bound |
| Deployments | `k8s/deployment.yaml` | `postgres` (1 pod) + `userapi` (2 pods) | `kubectl get pods` → 3 Running |
| Services | `k8s/service.yaml` | ClusterIP for postgres, NodePort for app | `kubectl get services` → 2 services |

**How to validate full Kubernetes deployment:**
```bash
minikube start --driver=docker --no-vtx-check

kubectl apply -f k8s/persistent-volume.yaml --validate=false
kubectl apply -f k8s/persistent-volume-claim.yaml --validate=false
kubectl apply -f k8s/deployment.yaml --validate=false
kubectl apply -f k8s/service.yaml --validate=false

kubectl get pods --request-timeout=60s
# Wait until all 3 pods show Running

kubectl get services
kubectl get pv,pvc

minikube service userapi-service --url
# Open the printed URL in browser → UserAPI dashboard appears
```

---

## Bonus — Docker Compose (extra points)

### Requirement: docker-compose.yml that starts the application

| Service | Image | Port | Purpose |
|---------|-------|------|---------|
| `postgres` | postgres:16 | 5432 | Database with health check |
| `pgadmin` | dpage/pgadmin4 | 5050 | Visual DB management UI |
| `app` | built from Dockerfile | 3000 | Flask API + Web UI |

```bash
docker-compose up --build      # start everything
# App:     http://localhost:3000
# pgAdmin: http://localhost:5050  (admin@admin.com / admin)
docker-compose down            # stop everything
```

---

## Summary Checklist

| Requirement | Status | Evidence |
|-------------|--------|----------|
| Web app with CRUD | ✅ | Flask routes in `src/routes.py`, Web UI in `src/templates/index.html` |
| PostgreSQL storage | ✅ | SQLAlchemy model in `src/models.py`, `userapi_db` database |
| Unit tests | ✅ | `test/test_unit.py` — 7 tests |
| API tests | ✅ | `test/test_api.py` — 20 tests |
| Config tests | ✅ | `test/test_config.py` — 16 tests |
| Connection tests | ✅ | `test/test_connection.py` — 7 tests |
| Health check endpoint | ✅ | `GET /health` returns DB status |
| CI pipeline | ✅ | `.github/workflows/ci.yml` — GitHub Actions |
| Vagrant VM | ✅ | `iac/Vagrantfile` — Ubuntu 22.04 |
| Ansible provisioning | ✅ | 3 roles: python, postgresql, app |
| Ansible health check | ✅ | `uri` task in app role |
| Dockerfile | ✅ | `userapi/Dockerfile` |
| Docker Hub push | ✅ | `kousiksc/userapi:latest` |
| .dockerignore | ✅ | `userapi/.dockerignore` |
| Minikube cluster | ✅ | `minikube start --driver=docker` |
| PV + PVC | ✅ | `k8s/persistent-volume.yaml` + `k8s/persistent-volume-claim.yaml` |
| Deployments | ✅ | `k8s/deployment.yaml` — postgres + userapi |
| Services | ✅ | `k8s/service.yaml` — ClusterIP + NodePort |
| Docker Compose (bonus) | ✅ | `docker-compose.yaml` — app + postgres + pgAdmin |
| Web UI (bonus) | ✅ | `src/templates/index.html` |
