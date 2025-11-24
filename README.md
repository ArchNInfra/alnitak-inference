# Alphard – Minimal Inference Service

Alphard is the inference star of the Constellation System — a lightweight, reproducible inference API designed to run on AWS ECS Fargate later in the pipeline.

This version implements the **minimal ML loop **:

- Train a simple ML model  
- Serve predictions via FastAPI  
- Package everything into a Docker image  

It forms the foundation for deployment in later stages (Day 5: ECS/Fargate).

---

## Overview

This repository provides:

- A reproducible ML training script (`ml/train.py`)
- A FastAPI-based inference service (`service/app.py`)
- A minimal Prometheus metrics endpoint
- A Docker runtime environment
- A clean, dependency-pinned Python environment

This version intentionally keeps everything small and deterministic.

---

## Scope

Alphard (v0.1 – minimal version) delivers:

- Minimal ML training pipeline
- FastAPI inference API
- Basic metrics endpoint
- Dockerized runtime environment
- Ready for AWS ECS Fargate deployment in v0.2

---

## Quick Start

### 1. Train the model locally

```
python -m ml.train
```

Produces:

```
ml/models/model-latest.pkl
```

### 2. Run the API locally

```
uvicorn service.app:app --reload
```

### 3. Test

#### Health Check

```
curl http://localhost:8000/health
```

#### Prediction

```
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"features":[0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0]}'
```

#### Metrics

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

## Endpoints

| Endpoint       | Description                        |
|----------------|------------------------------------|
| `/health`      | Service is alive and operational   |
| `/predict`     | Perform inference using the model  |
| `/metrics`     | Prometheus-compatible metrics      |

---

## Structure

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

### v0.2 — Upcoming
- ECS Fargate deployment  
- Structured logs  
- Rolling deploy readiness endpoints  
- GitHub Actions CI  

### v0.1 — Minimal Inference Loop (Current)
- Training script implemented  
- FastAPI service (`/health`, `/predict`, `/metrics`)  
- Docker image build & run  