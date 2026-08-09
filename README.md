# UserAPI — DevOps Project

A RESTful User Management API built with **Python / Flask** and **PostgreSQL**, featuring a web dashboard UI. The project demonstrates a complete DevOps lifecycle: automated testing, CI/CD pipeline, Infrastructure as Code, Docker containerization, and Kubernetes orchestration.

---

## Author

| Name | Group |
|------|-------|
| *Your Name Here* | SI03 |

> **AI Usage Notice:** This project was developed with assistance from Claude (Anthropic) for scaffolding code structure, configuration files, and documentation, as per DSTI policy.

---

## What This Project Does

This project builds a **User Management API** — a backend service that lets you create, read, update, and delete users stored in a PostgreSQL database. It comes with a web dashboard so you can interact with it visually in a browser.

The project then wraps this application in every major DevOps tool:

| Tool | What it does in this project |
|------|------------------------------|
| **pytest** | Automatically tests that the code works correctly |
| **GitHub Actions** | Runs tests automatically every time code is pushed |
| **Docker** | Packages the app into a portable container |
| **Docker Compose** | Runs the app + database + pgAdmin together with one command |
| **Vagrant + Ansible** | Creates and configures a virtual machine automatically |
| **Kubernetes** | Runs multiple containers as a scalable cluster |

---

## Work Performed

### Part 1 — Web Application
- Python/Flask REST API with full CRUD for users (Create, Read, Update, Delete)
- PostgreSQL database with SQLAlchemy ORM
- Web UI dashboard — add, edit, delete users with live health status indicator
- Health check endpoint (`GET /health`) that pings the database
- **4 test suites — 51 tests total:** unit, API (functional), configuration, connection

### Part 2 — CI/CD (GitHub Actions)
- `test` job: spins up a real PostgreSQL service container, installs deps, runs all 51 pytest tests
- `lint` job: flake8 code quality check on source code
- `docker-build` job: builds the Docker image (only runs after tests pass)

### Part 3 — IaC (Vagrant + Ansible)
- Vagrantfile: Ubuntu 22.04 VM with port forwarding and synced folder
- Ansible roles: `python` (installs Python + dependencies), `postgresql` (installs + configures DB + creates database), `app` (creates systemd service, starts app, runs health check)
- Ansible health check task confirms the app is live after provisioning

### Part 4 — Docker
- Dockerfile using `python:3.11-slim` base image
- Image pushed to Docker Hub: **[kousiksc/userapi](https://hub.docker.com/r/kousiksc/userapi)**
- `.dockerignore` excludes all dev/test artifacts

### Part 5 — Kubernetes (Minikube)
- PersistentVolume + PersistentVolumeClaim for PostgreSQL data persistence
- Deployments: `postgres` (1 replica) + `userapi` (2 replicas with load balancing)
- Services: `postgres-service` (ClusterIP — internal) + `userapi-service` (NodePort — external access)
- Liveness and readiness probes on the API container

### Bonus
- **Docker Compose** — single command starts app + PostgreSQL + pgAdmin 4
- **pgAdmin 4** — visual database management UI (runs at `http://localhost:5050`)
- **Web UI Dashboard** — browser-based frontend for the API

---

## Project Structure

```
.
├── .github/
│   └── workflows/
│       └── ci.yml                  # GitHub Actions CI pipeline
├── userapi/
│   ├── src/
│   │   ├── __init__.py             # Flask app factory
│   │   ├── app.py                  # Entry point
│   │   ├── config.py               # Config classes (Default / Test / Production)
│   │   ├── models.py               # User SQLAlchemy model
│   │   ├── routes.py               # All REST endpoints + UI route
│   │   └── templates/
│   │       └── index.html          # Web dashboard UI
│   ├── test/
│   │   ├── conftest.py             # pytest fixtures (SQLite in-memory)
│   │   ├── test_unit.py            # Unit tests — model validation logic
│   │   ├── test_api.py             # API tests — full HTTP request/response
│   │   ├── test_config.py          # Configuration loading tests
│   │   └── test_connection.py      # Database connection & schema tests
│   ├── conf/
│   │   └── database.ini            # DB config reference file
│   ├── .env                        # Local environment variables (not committed)
│   ├── Dockerfile
│   ├── .dockerignore
│   ├── requirements.txt
│   ├── setup.py
│   └── pytest.ini
├── iac/
│   ├── Vagrantfile
│   └── playbooks/
│       ├── inventory.ini
│       ├── setup.yml
│       └── roles/
│           ├── python/tasks/main.yml
│           ├── postgresql/tasks/main.yml
│           └── app/tasks/main.yml
├── k8s/
│   ├── persistent-volume.yaml
│   ├── persistent-volume-claim.yaml
│   ├── deployment.yaml
│   └── service.yaml
├── screenshots/
├── docker-compose.yaml
├── setup.py
├── .gitignore
└── README.md
```

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Web UI dashboard |
| GET | `/api` | API info (JSON) |
| GET | `/health` | Health check — pings the database |
| POST | `/users` | Create a new user |
| GET | `/users` | List all users |
| GET | `/users/<id>` | Get a single user by ID |
| PUT | `/users/<id>` | Update a user |
| DELETE | `/users/<id>` | Delete a user |

---

## Screenshots

| Screenshot | Description |
|-----------|-------------|
| ![Dashboard](screenshots/dashboard.png) | Web UI dashboard with users |
| ![Tests](screenshots/tests.png) | 51 pytest tests passing |
| ![pgAdmin](screenshots/pgadmin.png) | pgAdmin showing users table |
| ![CI Pipeline](screenshots/ci_pipeline.png) | GitHub Actions green CI run |
| ![Docker Hub](screenshots/dockerhub.png) | Docker Hub image page |
| ![Vagrant](screenshots/vagrant_provision.png) | Ansible provisioning output |
| ![K8s Pods](screenshots/k8s_pods.png) | kubectl get pods output |

---

## Prerequisites — Install These First

### 1. Docker Desktop
Runs containers. Required for Docker Compose and Minikube (Docker driver).

Download: https://www.docker.com/products/docker-desktop/

```bash
docker --version        # verify
docker-compose --version
```

### 2. VirtualBox
Hypervisor that runs the Vagrant virtual machine.

Download: https://www.virtualbox.org/wiki/Downloads

```bash
VBoxManage --version    # verify
```

### 3. Vagrant
Tool that creates and manages virtual machines using a simple config file (Vagrantfile).

Download: https://developer.hashicorp.com/vagrant/downloads
→ Choose **Windows AMD64** → install the `.msi` → **restart your terminal**

```bash
vagrant --version       # verify
```

### 4. Minikube
Runs a local Kubernetes cluster inside Docker.

Download: https://minikube.sigs.k8s.io/docs/start/
→ The installer places it at `C:\Program Files\Kubernetes\Minikube\`
→ Add that path to your Windows **System Environment Variables → PATH**
→ Restart terminal after adding to PATH

```bash
minikube version        # verify
```

### 5. kubectl
Command-line tool to control Kubernetes clusters.

Download: https://kubernetes.io/docs/tasks/tools/install-kubectl-windows/

```bash
kubectl version --client   # verify
```

### 6. Python 3.11+
Download: https://www.python.org/downloads/

```bash
python --version        # verify
```

---

## Step 1 — Configure Environment

```bash
# Clone the repository
git clone https://github.com/kousiksc/devops-project.git
cd devops-project
```

Create the file `userapi/.env` with the following content:

```
DB_HOST=localhost
DB_PORT=5432
DB_NAME=userapi_db
DB_USER=postgres
DB_PASSWORD=postgres
SECRET_KEY=my-super-secret-key
```

> This file is for local development only. It is in `.gitignore` and never committed.

---

## Step 2 — Run Tests

Tests use SQLite in-memory — **no PostgreSQL installation needed**.

```bash
cd userapi

# Install dependencies
pip install -r requirements.txt

# Install the package in editable mode (makes imports work)
pip install -e ..

# Run all 51 tests with verbose output
python -m pytest test/ -v

# Run individual suites
python -m pytest test/test_unit.py -v        # tests model validation logic
python -m pytest test/test_api.py -v         # tests every HTTP endpoint
python -m pytest test/test_config.py -v      # tests config loading from env vars
python -m pytest test/test_connection.py -v  # tests DB schema and CRUD operations
```

Expected result: **51 passed**

---

## Step 3 — Docker Compose (Recommended way to run the full stack)

**What Docker Compose does:** reads `docker-compose.yaml` and starts all 3 services (app, PostgreSQL, pgAdmin) together as a group with one command. Each service runs in its own container.

```bash
# From the project root — builds image and starts all containers
cd E:\PROJECT2
docker-compose up --build
```

Wait until you see:
```
userapi_app  | Listening at: http://0.0.0.0:3000
```

### Services and their URLs:

| Service | URL | Login |
|---------|-----|-------|
| **Web App Dashboard** | http://localhost:3000 | — |
| **Health Check** | http://localhost:3000/health | — |
| **pgAdmin 4** | http://localhost:5050 | `admin@admin.com` / `admin` |
| **PostgreSQL** | localhost:5432 | `postgres` / `postgres` |

> **pgAdmin only runs with Docker Compose** — it is not available in Vagrant or Kubernetes.

### Connect pgAdmin to the database:
1. Open http://localhost:5050 → login with `admin@admin.com` / `admin`
2. Right-click **Servers** → **Register** → **Server**
3. **General tab** → Name: `UserAPI`
4. **Connection tab** → Host: `postgres`, Port: `5432`, Username: `postgres`, Password: `postgres`
5. Click **Save**
6. Browse to: `userapi_db` → Schemas → public → Tables → `users` → right-click → **View/Edit Data → All Rows**

### Use the Web Dashboard:
- Go to http://localhost:3000
- Fill in the form and click **+ Add User** → user appears in table instantly
- Click **Edit** → a modal opens, change fields, click **Save Changes**
- Click **Delete** → confirmation prompt, then removed from table and database
- Green dot in header = database connection is healthy

### Stop:
```bash
docker-compose down        # stops and removes containers (data is preserved in volumes)
docker-compose down -v     # stops and also deletes the database volume (fresh start)
```

---

## Step 4 — Docker Image (Build & Push to Docker Hub)

**What Docker does:** packages the app and all its dependencies into a single portable image that runs the same everywhere.

```bash
cd userapi

# Build the image and tag it with your Docker Hub username
docker build -t kousiksc/userapi:latest .

# Login to Docker Hub
docker login

# Push the image to Docker Hub (makes it publicly available)
docker push kousiksc/userapi:latest
```

**Docker Hub image:** https://hub.docker.com/r/kousiksc/userapi

---

## Step 5 — Vagrant + Ansible (Infrastructure as Code)

**What Vagrant is:** a tool that creates and configures virtual machines automatically from a text file (Vagrantfile). Instead of manually setting up a server, you describe what you want and Vagrant builds it.

**What Ansible is:** a tool that configures software on a server automatically. It reads "playbooks" (YAML files) that describe what to install and run — no manual SSH commands needed.

> Run `docker-compose down` first to free port 3000.

```bash
cd iac

# Creates Ubuntu VM in VirtualBox + runs Ansible to install everything
vagrant up
```

**What `vagrant up` does step by step:**
1. Downloads Ubuntu 22.04 box (~500 MB, first time only)
2. Creates a virtual machine in VirtualBox
3. Installs Ansible inside the VM
4. Runs the Ansible playbook which:
   - Installs Python 3, pip, and all dependencies
   - Installs PostgreSQL and creates the `userapi_db` database
   - Creates a systemd service for the app
   - Starts the app and runs a health check

**Total time:** ~15–25 minutes on first run.

After it finishes, the app is at:
- http://localhost:3000 (port forwarded from VM)

### Verify the app inside the VM:
```bash
vagrant ssh                           # connect to the VM via SSH

# Inside the VM:
systemctl status userapi              # check service status — should show "active (running)"
curl http://localhost:3000/health     # should return {"status":"ok","database":"healthy"}
curl http://localhost:3000/users      # should return [] (empty list)
exit                                  # exit the VM
```

### Other Vagrant commands:
```bash
vagrant status      # show current VM state (running / poweroff / not created)
vagrant halt        # gracefully shut down the VM (preserves all data)
vagrant reload      # restart the VM — use this after changing Vagrantfile
vagrant provision   # re-run Ansible without rebooting (use after fixing playbooks)
vagrant ssh         # open SSH shell inside the VM
vagrant destroy     # completely delete the VM (frees disk space)
```

### If `vagrant up` fails mid-way:
```bash
vagrant provision   # re-runs Ansible on the already-booted VM — much faster than vagrant up
```

---

## Step 6 — Kubernetes (Minikube)

**What Kubernetes is:** a system that manages containerized applications across multiple machines (or simulated machines). It automatically restarts crashed containers, balances traffic between replicas, and manages storage.

**What Minikube is:** a tool that runs a single-node Kubernetes cluster on your local machine for development/testing.

> Make sure Docker Desktop is running. Run `vagrant halt` first if Vagrant VM is up.

### Start the cluster:
```bash
# Start a local Kubernetes cluster using Docker as the driver (no VT-X required)
minikube start --driver=docker --no-vtx-check

# Verify the cluster is fully running
minikube status
# Expected:
# host: Running
# kubelet: Running
# apiserver: Running      ← all 3 must show Running
# kubeconfig: Configured
```

### Deploy the application:
```bash
# Create storage for PostgreSQL data
kubectl apply -f k8s/persistent-volume.yaml --validate=false
# Creates a PersistentVolume — a piece of storage on the node

kubectl apply -f k8s/persistent-volume-claim.yaml --validate=false
# Creates a PersistentVolumeClaim — reserves that storage for PostgreSQL

kubectl apply -f k8s/deployment.yaml --validate=false
# Creates 2 Deployments: postgres (1 replica) and userapi (2 replicas)

kubectl apply -f k8s/service.yaml --validate=false
# Creates 2 Services:
#   postgres-service (ClusterIP)  — internal access only, used by the app
#   userapi-service  (NodePort)   — external access on port 30080
```

### Check everything is running:
```bash
kubectl get pods --request-timeout=60s
# Wait until all STATUS = Running (takes 1-3 minutes)
# NAME                         READY   STATUS    RESTARTS   AGE
# postgres-xxx-xxx             1/1     Running   0          2m
# userapi-xxx-xxx              1/1     Running   0          2m
# userapi-xxx-xxx              1/1     Running   0          2m

kubectl get services
# NAME               TYPE        CLUSTER-IP     PORT(S)
# postgres-service   ClusterIP   10.x.x.x       5432/TCP
# userapi-service    NodePort    10.x.x.x       80:30080/TCP

kubectl get pv,pvc
# Shows PersistentVolume and PersistentVolumeClaim both BOUND
```

### Access the app:
```bash
# Get the URL (keep this terminal open — tunnel stays alive while open)
minikube service userapi-service --url
# Prints something like: http://127.0.0.1:54422
# Open that URL in your browser
```

### Useful debug commands:
```bash
kubectl logs -l app=userapi              # view app container logs
kubectl describe pod <pod-name>          # detailed info about a pod
kubectl get events --sort-by=.metadata.creationTimestamp   # see what happened
```

### Cleanup:
```bash
kubectl delete -f k8s/      # remove all deployments, services, PV, PVC
minikube stop               # stop the cluster (preserves state)
minikube delete             # completely delete the cluster
```

### Troubleshooting Minikube:

**Problem: `apiserver: Stopped` in minikube status**
```bash
minikube stop
minikube start --driver=docker --no-vtx-check
```

**Problem: `kubectl get pods` times out**
```bash
kubectl get pods --request-timeout=60s
```

**Problem: TLS handshake timeout on kubectl apply**
```bash
# Add --validate=false to skip client-side schema validation
kubectl apply -f k8s/deployment.yaml --validate=false
```

**Problem: minikube not recognized as a command**
- Add `C:\Program Files\Kubernetes\Minikube` to Windows PATH
- Open: System Properties → Advanced → Environment Variables → System Variables → Path → New

**Problem: Docker Desktop unable to start**
- Open Task Manager → end all `Docker Desktop`, `com.docker.backend`, `com.docker.proxy` processes
- Relaunch Docker Desktop from Start menu

**Problem: Port already in use**
- Run `docker-compose down` to free ports 3000 and 5432
- Run `vagrant halt` to free port 3000

---

## CI/CD — GitHub Actions

Every push to `main` or `develop` automatically triggers the pipeline.

**Jobs:**

| Job | What it does |
|-----|-------------|
| `test` | Starts a real PostgreSQL container, installs Python deps, runs all 51 pytest tests |
| `lint` | Runs flake8 to check code style and catch syntax errors |
| `docker-build` | Builds the Docker image to verify it builds cleanly (only after tests pass) |

View CI runs: https://github.com/kousiksc/devops-project/actions

---

## Links

| Resource | URL |
|----------|-----|
| GitHub Repository | https://github.com/kousiksc/devops-project |
| Docker Hub Image | https://hub.docker.com/r/kousiksc/userapi |
| GitHub Actions CI | https://github.com/kousiksc/devops-project/actions |
| Vagrant Downloads | https://developer.hashicorp.com/vagrant/downloads |
| VirtualBox Downloads | https://www.virtualbox.org/wiki/Downloads |
| Minikube Docs | https://minikube.sigs.k8s.io/docs/start/ |
