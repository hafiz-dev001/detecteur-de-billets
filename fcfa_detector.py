from __future__ import annotations

import random
import pickle
from pathlib import Path
from typing import Iterable, Optional

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import LinearSVC


class FCFADetector:
    """Prototype simple de détecteur de billets FCFA basé sur des caractéristiques d'image.

    Ce prototype fonctionne sur des images synthétiques pour illustrer le pipeline ML.
    Pour un usage réel, il faut remplacer ce jeu de données par de vraies photos de billets.
    """

    def __init__(self, denominations: Optional[Iterable[str]] = None) -> None:
        self.denominations = list(denominations or ["500", "1000", "2000", "5000", "10000"])
        self.model = None
        self.feature_size = 64 * 64 + 8 * 3

    def _make_bill_image(self, denomination: str, size: tuple[int, int] = (64, 64)) -> Image.Image:
        img = Image.new("RGB", size, (235, 235, 235))
        draw = ImageDraw.Draw(img)

        colors = {
            "500": (255, 196, 0),
            "1000": (255, 140, 0),
            "2000": (255, 99, 71),
            "5000": (100, 149, 237),
            "10000": (60, 179, 113),
        }

        draw.rounded_rectangle((4, 4, size[0] - 5, size[1] - 5), radius=6, outline=(30, 30, 30), width=2)
        draw.rectangle((8, 8, size[0] - 9, size[1] - 9), fill=colors[denomination])
        draw.text((11, 16), f"FCFA\n{denomination}", fill=(20, 20, 20))
        draw.text((12, 42), "X", fill=(60, 60, 60))

        if random.random() > 0.5:
            img = img.rotate(random.uniform(-6, 6), expand=False, fillcolor=(235, 235, 235))

        return img

    def _extract_features(self, image: Image.Image) -> np.ndarray:
        img = image.resize((64, 64)).convert("RGB")
        arr = np.array(img, dtype=np.float32)
        gray = np.mean(arr, axis=2).flatten()

        hist_r = np.histogram(arr[:, :, 0], bins=8, range=(0, 256))[0].astype(np.float32)
        hist_g = np.histogram(arr[:, :, 1], bins=8, range=(0, 256))[0].astype(np.float32)
        hist_b = np.histogram(arr[:, :, 2], bins=8, range=(0, 256))[0].astype(np.float32)

        return np.concatenate([gray, hist_r, hist_g, hist_b])

    def build_dataset(self, samples_per_class: int = 25) -> tuple[np.ndarray, np.ndarray]:
        features: list[np.ndarray] = []
        labels: list[str] = []

        for denomination in self.denominations:
            for _ in range(samples_per_class):
                image = self._make_bill_image(denomination)
                features.append(self._extract_features(image))
                labels.append(denomination)

        return np.array(features, dtype=np.float32), np.array(labels)

    def train(self, X: np.ndarray, y: np.ndarray) -> float:
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )

        self.model = make_pipeline(
            StandardScaler(),
            LinearSVC(C=1.0, random_state=42),
        )
        self.model.fit(X_train, y_train)

        accuracy = self.model.score(X_test, y_test)
        print("Précision sur l’échantillon de test:", round(accuracy * 100, 2), "%")
        print(classification_report(y_test, self.model.predict(X_test)))
        return float(accuracy)

    def save(self, path: str | Path = "fcfa_detector_model.pkl") -> None:
        if self.model is None:
            raise ValueError("Le modèle n’a pas encore été entraîné.")

        with open(path, "wb") as handle:
            pickle.dump({"denominations": self.denominations, "model": self.model}, handle)

    def load(self, path: str | Path = "fcfa_detector_model.pkl") -> None:
        with open(path, "rb") as handle:
            payload = pickle.load(handle)
        self.denominations = payload["denominations"]
        self.model = payload["model"]

    def predict_image(self, image_path: str | Path | Image.Image) -> str:
        if self.model is None:
            raise ValueError("Le modèle n’a pas encore été entraîné.")

        if isinstance(image_path, Image.Image):
            img = image_path
        else:
            img = Image.open(image_path).convert("RGB")

        features = self._extract_features(img)
        return str(self.model.predict([features])[0])


def main() -> None:
    detector = FCFADetector()
    X, y = detector.build_dataset(samples_per_class=30)
    detector.train(X, y)
    detector.save("fcfa_detector_model.pkl")

    sample_path = Path("sample_bill.png")
    detector._make_bill_image("5000").save(sample_path)
    prediction = detector.predict_image(sample_path)
    print("Prédiction sur l’image de test:", prediction)
    print("Le modèle a été sauvegardé dans fcfa_detector_model.pkl")


if __name__ == "__main__":
    main()
