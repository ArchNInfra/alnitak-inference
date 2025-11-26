from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse, Response
from pydantic import BaseModel
import joblib
import numpy as np
from prometheus_client import Counter, generate_latest

app = FastAPI()

model = None
model_loaded = False

# --- Metrics ---
PREDICTION_COUNT = Counter(
    "alphard_predictions_total",
    "Total number of prediction requests served by Alphard"
)


class PredictionInput(BaseModel):
    features: list[float]


# --- Global exception handler ---
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "error": "internal_error",
            "detail": str(exc),
        },
    )


# --- Startup: load model ---
@app.on_event("startup")
def load_model():
    global model, model_loaded
    try:
        model = joblib.load("ml/models/model-latest.pkl")
        model_loaded = True
        print("[INFO] Model loaded successfully")
    except Exception as e:
        model = None
        model_loaded = False
        print(f"[ERROR] Failed to load model: {e}")


@app.get("/health")
def health():
    if not model_loaded:
        raise HTTPException(status_code=503, detail="model_not_loaded")
    return {"status": "healthy"}


# --- Metrics endpoint（Prometheus） ---
@app.get("/metrics")
def metrics():
    data = generate_latest()
    return Response(content=data, media_type="text/plain; version=0.0.4")


# --- Predict ---
@app.post("/predict")
def predict(input: PredictionInput):
    if not model_loaded:
        raise HTTPException(status_code=503, detail="model_not_loaded")

    features = np.array(input.features).reshape(1, -1)
    prediction = model.predict(features)[0]

    PREDICTION_COUNT.inc()

    return {"prediction": int(prediction)}
