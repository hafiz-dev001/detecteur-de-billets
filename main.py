from __future__ import annotations

import io
from pathlib import Path
from typing import Any

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image

from fcfa_detector import FCFADetector

MODEL_PATH = Path(__file__).resolve().parent / "fcfa_detector_model.pkl"

detector = FCFADetector()


def ensure_model_loaded() -> None:
    if MODEL_PATH.exists():
        detector.load(MODEL_PATH)
        return

    X, y = detector.build_dataset(samples_per_class=25)
    detector.train(X, y)
    detector.save(MODEL_PATH)


ensure_model_loaded()

app = FastAPI(title="FCFA Bill Detector API", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def health() -> dict[str, Any]:
    return {"status": "ok", "model": "fcfa_detector_model.pkl", "denominations": detector.denominations}


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/predict-image")
async def predict_image(request: Request) -> dict[str, Any]:
    body = await request.body()
    if not body:
        return {"status": "error", "message": "No image uploaded"}

    try:
        image = Image.open(io.BytesIO(body)).convert("RGB")
    except Exception as exc:  # pragma: no cover - defensive branch
        return {"status": "error", "message": f"Invalid image: {exc}"}

    prediction = detector.predict_image(image)
    return {"status": "ok", "prediction": prediction}
