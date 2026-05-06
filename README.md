# DevOps Challenge — Application

A Dockerised Flask REST API deployed to AWS EC2 via GitHub Actions.

---

## Table of Contents

- [Application Overview](#application-overview)
- [Repository Structure](#repository-structure)
- [Running Locally](#running-locally)
- [Docker](#docker)
- [CI/CD Pipeline](#cicd-pipeline)
- [GitHub Secrets](#github-secrets)

---

## Application Overview

A minimal Flask REST API with two endpoints:

| Endpoint | Method | Response |
|---|---|---|
| `/` | GET | `{ "message": "DevOps Challenge App is running", "status": "ok" }` |
| `/health` | GET | `{ "status": "healthy", "environment": "<APP_ENV>" }` |

**Stack**
- Python 3.12
- Flask 3.1.3
- Runs on port `5000`
- Containerised with Docker using `python:3.12-slim`

---

## Repository Structure

```
devops-challenge-app/
├── app.py                  # Flask application
├── conftest.py             # Pytest configuration
├── test_app.py             # Application tests
├── requirements.txt        # Python dependencies
├── Dockerfile              # Container definition
└── .github/
    └── workflows/
        └── application.yml # Test, build, and deploy pipeline
```

---

## Running Locally

**Install dependencies and start the server**

```bash
pip install -r requirements.txt
python app.py
```

Visit `http://localhost:5000` and `http://localhost:5000/health` to verify the app is running.

**Run tests**

```bash
pytest test_app.py -v
```

---

## Docker

**Build and run the image locally**

```bash
docker build -t devops-challenge-app .
docker run -p 5000:5000 devops-challenge-app
```

**Image is published to Docker Hub as:**

```
yourname/devops-challenge-app:latest
yourname/devops-challenge-app:<git-sha>
```

The pipeline tags every build with both `latest` and the commit SHA so previous versions can be identified and rolled back to if needed.

---

## CI/CD Pipeline

**Trigger:** push to `main`

```
Push to main
      |
      v
  [build job]
   |- Build Docker image
   +- Cache image for subsequent jobs
      |
      v
  [test job]
   |- Load built image
   +- Run pytest inside the container
      |
      v
  [push job]
   |- Log in to Docker Hub
   +- Push image (latest + git-sha tags)
      |
      v
  [deploy job]  <- requires "production" environment
   |- Read EC2_PUBLIC_IP from repository secrets
   +- SSH into EC2 -> pull image -> stop old container -> run new container
```

The `production` environment can be configured in **Settings > Environments** to require a reviewer before the deploy job runs.

Building before testing means the test job runs against the actual Docker image that will be deployed, not just the raw source code. The image is only pushed to Docker Hub if tests pass. The deploy job then connects to the EC2 instance over SSH, pulls the verified image, stops the currently running container, and starts a new one in its place.

---

## GitHub Secrets

Navigate to **Settings > Secrets and variables > Actions** in this repository and add:

| Secret | Description |
|---|---|
| `EC2_PUBLIC_IP` | Public IP of the EC2 instance — copy from Terraform output after infrastructure is deployed |
| `EC2_SSH_PRIVATE_KEY` | Full contents of your `.pem` private key file |
| `DOCKERHUB_USERNAME` | Docker Hub username |
| `DOCKERHUB_TOKEN` | Docker Hub access token (not your password) |

> The EC2 instance is provisioned separately via the infrastructure repository. `EC2_PUBLIC_IP` must be updated here whenever the infrastructure is redeployed and a new IP is assigned.
