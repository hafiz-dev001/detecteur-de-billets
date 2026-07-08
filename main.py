from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import joblib
import numpy as np
from PIL import Image
import io

app = FastAPI(docs_url="/", redoc_url=None, title="FCFA Detector API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Charger le modèle une seule fois au démarrage
model_payload = joblib.load("fcfa_detector_model.pkl")
model = model_payload["model"]

@app.get("/")
def home():
    return {
        "status": "ok", 
        "model": "fcfa_detector_model.pkl",
        "denominations": ["500", "1000", "2000", "5000", "10000"]
    }

def extract_features(image: Image.Image) -> np.ndarray:
    img = image.resize((64, 64)).convert("RGB")
    arr = np.array(img, dtype=np.float32)
    gray = np.mean(arr, axis=2).flatten()

    hist_r = np.histogram(arr[:, :, 0], bins=8, range=(0, 256))[0].astype(np.float32)
    hist_g = np.histogram(arr[:, :, 1], bins=8, range=(0, 256))[0].astype(np.float32)
    hist_b = np.histogram(arr[:, :, 2], bins=8, range=(0, 256))[0].astype(np.float32)

    return np.concatenate([gray, hist_r, hist_g, hist_b]).reshape(1, -1)


@app.post("/predict-image")
async def predict_image(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents)).convert("RGB")

        features = extract_features(image)
        pred = model.predict(features)[0]

        return {
            "denomination": str(pred),
            "status": "success"
        }
    except Exception as exc:
        return {
            "status": "error",
            "message": f"Prediction failed: {exc}"
        }
