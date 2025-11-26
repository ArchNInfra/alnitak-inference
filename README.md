# Alphard — Minimal Inference Service

Alphard is the inference star of the Constellation System — a lightweight, reproducible ML inference service designed for containerized deployment on AWS ECS Fargate.

This repository implements the **minimal ML loop **:
- Train a simple ML model
- Serve predictions via FastAPI
- Export Prometheus metrics
- Package into a deterministic Docker image
- Integrate with Thuban (ECS/Fargate baseline)

---

## Overview

Alphard provides:

- A reproducible training pipeline (`ml/train.py`)
- A minimal FastAPI inference server (`service/app.py`)
- Health check endpoint for ALB (`/health`)
- Prometheus metrics (`/metrics`)
- Dockerized runtime
- Deterministic dependency pinning

This service is intentionally minimal to ensure stability and ease of deployment across environments.

---

## Architecture

```
                +-----------------------------+
                |        Alphard API          |
                |  FastAPI + Uvicorn          |
                +--------------+--------------+
                               |
                     Load Model on Startup
                               |
                     ml/models/model-latest.pkl
                               ^
                               |
                     +---------+---------+
                     |   ml/train.py     |
                     |  Train → Export   |
                     +-------------------+
```

---

## Quick Start

### 1. Train the model

```
python -m ml.train
```

This produces:

```
ml/models/model-latest.pkl
```

### 2. Run the API locally

```
uvicorn service.app:app --reload
```

---

## Endpoints

| Endpoint       | Description                                 |
|----------------|---------------------------------------------|
| `/health`      | Service ready, model loaded                 |
| `/predict`     | Run inference                               |
| `/metrics`     | Prometheus metrics (counters & gauges)      |

### Examples

**Health**

```
curl http://localhost:8000/health
```

**Predict**

```
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"features":[0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0]}'
```

**Metrics**

```
curl http://localhost:8000/metrics
```

---

## Docker

### Build

```
docker build -t alphard-inference:local .
```

### Run

```
docker run -p 8000:8000 alphard-inference:local
```

---

## Deployment (via Thuban-infra)

Thuban provisions:
- ECS Cluster
- Task Definition
- ALB + Listener + Target Group
- IAM Task Roles
- CloudWatch Logs
- ECR Repository

Alphard only needs to provide a container image and respond to:
- `/health`
- port `8000`

---

## Repository Structure

```
alphard-inference/
├── ml/
│   ├── train.py
│   └── models/
│       └── model-latest.pkl        (ignored by Git)
├── service/
│   └── app.py
├── tests/
│   └── __init__.py
├── Dockerfile
├── requirements.txt
└── README.md
```

---

## Status

### v0.2 — Completed
- Error handling for model load failure
- Prometheus metrics
- ECS-ready health check
- Stable Docker build

### v0.1 — Initial
- Minimal training + inference loop

