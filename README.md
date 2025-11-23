# Alphard – Inference Service

**Alphard** is the inference star of the Constellation System — a solitary, high-pressure gateway just like the star Alphard (“the solitary one”) in Hydra.  
It provides a resilient, containerized inference API capable of running behind AWS ECS Fargate.

---

## Overview

Alphard exposes a minimal, production-ready inference API that serves model predictions and integrates cleanly with the Mira MLOps pipeline.

The design emphasizes:

- **Reproducibility** (immutable Docker images, Git SHA tags)
- **Stability under load** (ECS + ALB health checks)
- **Structured logging** (logfmt or JSON logs for CloudWatch)
- **Separation of concerns** (model is loaded from S3 or artifact registry)

---

## Scope

### Core Features
- FastAPI-based REST inference endpoint  
- Config-driven model loading  
- Structured JSON logs (compatible with CloudWatch Insights)  
- Health probe endpoints (`/live`, `/ready`)

### Deployment Targets
- **AWS ECS Fargate** (primary)
- AWS ALB with rolling deployments
- ECR container registry
- GitHub Actions CI for:
  - lint → build → push → deploy (optional)

---

## Stack

**Language & Framework**
- Python
- FastAPI
- Uvicorn

**AWS Services**
- ECS Fargate (service runtime)
- ALB (load balancing + health checks)
- ECR (container images)
- CloudWatch Logs (observability)
- S3 (model artifact retrieval, optional)

**Tooling**
- Docker (multi-stage build)
- GitHub Actions (CI)

---

## Structure

(To be completed after v0.2)

Suggested layout:

alphard-inference/
app/
main.py
inference.py
models/
configs/
docker/
infra/
tests/
scripts/
docs/


---

## Health Endpoints

The service exposes:

- `/live` – process is alive  
- `/ready` – model loaded & API ready  
- `/predict` – inference endpoint  

These enable ALB to safely orchestrate rolling deployments without dropping traffic.

---

## Status

### 0.2 — Upcoming
- Add FastAPI app structure  
- Add Docker multi-stage build  
- Add GitHub Actions CI pipeline  
- Add ECS task/service Terraform module  

### 0.1 — Repository initialized
- Renamed to Alphard and linked to the Constellation system
