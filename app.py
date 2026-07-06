from flask import Flask, request, jsonify
import joblib
import numpy as np
from PIL import Image
import io
import random
from sklearn.preprocessing import StandardScaler
from sklearn.svm import LinearSVC
from PIL import ImageDraw

app = Flask(_name_)

class FCFADetector:
    """Prototype simple de détecteur de billets FCFA"""
    def _init_(self, denominations=None):
        self.denominations = list(denominations or ["500", "1000", "2000", "5000", "10000"])
        self.model = None
        self.feature_size = 64 * 64 + 8 * 3
        self.scaler = StandardScaler()
        self._train_dummy_model()

    def _make_bill_image(self, denomination, size=(64, 64)):
        img = Image.new("RGB", size, (235, 235, 235))
        draw = ImageDraw.Draw(img)
        colors = {
            "500": (255, 196, 0),
            "1000": (255, 140, 0),
            "2000": (255, 99, 71),
            "5000": (100, 149, 237),
            "10000": (60, 179, 113),
        }
        draw.rounded_rectangle((4, 4, size[0] - 5, size[1] - 5), radius=6, outline=(30, 30, 30))
        draw.rectangle((8, 8, size[0] - 9, size[1] - 9), fill=colors[denomination])
        draw.text((11, 16), f"FCFA\n{denomination}", fill=(20, 20, 20))
        return img

    def _extract_features(self, img):
        img = img.resize((64, 64)).convert('RGB')
        arr = np.array(img).flatten()
        hist = np.histogram(arr, bins=8, range=(0, 255))[0]
        return np.concatenate([arr[:100], hist]) # réduit pour demo

    def _train_dummy_model(self):
        X, y = [], []
        for denom in self.denominations:
            for _ in range(10):
                img = self._make_bill_image(denom)
                X.append(self._extract_features(img))
                y.append(denom)
        X = self.scaler.fit_transform(X)
        self.model = LinearSVC()
        self.model.fit(X, y)

    def predict(self, img):
        features = self._extract_features(img)
        features = self.scaler.transform([features])
        pred = self.model.predict(features)[0]
        return pred

detector = FCFADetector()

@app.route('/')
def home():
    return "API Detecteur FCFA OK ✅ Envoie POST sur /detect avec 'image'"

@app.route('/detect', methods=['POST'])
def detect():
    if 'image' not in request.files:
        return jsonify({"error": "Envoie une image avec key='image'"}), 400
    
    file = request.files['image']
    img = Image.open(file.stream)
    
    billet = detector.predict(img)
    
    return jsonify({"billet_detecte": f"{billet} FCFA", "status": "success"})

if _name_ == '_main_':
    app.run(host='0.0.0.0', port=10000)