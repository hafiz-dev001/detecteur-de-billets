from fastapi import FastAPI, UploadFile, File
import joblib
import numpy as np
from PIL import Image
import io

app = FastAPI()

# Charger le modèle une seule fois au démarrage
model = joblib.load("fcfa_detector_model.pkl")

@app.get("/")
def home():
    return {
        "status": "ok", 
        "model": "fcfa_detector_model.pkl",
        "denominations": ["500", "1000", "2000", "5000", "10000"]
    }

@app.post("/predict-image")
async def predict_image(file: UploadFile = File(...)):
    # Lire l'image envoyée
    contents = await file.read()
    image = Image.open(io.BytesIO(contents)).convert('RGB')
    
    # Redimensionner comme à l'entraînement - ta classe utilise 64x64
    image = image.resize((64, 64))
    
    # Extraire features comme dans ta classe FCFAExtractor
    arr = np.array(image).flatten()
    hist = np.histogram(arr, bins=8, range=(0, 255))[0]
    
    # Concaténer pixels + histo comme dans _extract_features
    features = np.concatenate([arr[:64*64], hist]).reshape(1, -1)
    
    # Prédiction
    pred = model.predict(features)[0]
    
    return {
        "denomination": str(pred),
        "status": "success"
    }
