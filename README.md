# Détecteur de billets FCFA pour Android

Ce projet contient un prototype de détecteur de billets FCFA basé sur l’apprentissage automatique, un backend FastAPI pour l’inférence et une application Android minimale qui envoie une photo au modèle.

## Architecture
- Backend Python : charge le modèle, reçoit une image et retourne une prédiction.
- Application Android : permet de prendre une photo ou de choisir une image depuis le téléphone, puis d’envoyer cette image au backend.

## Fichiers clés
- [fcfa_detector.py](fcfa_detector.py) : génération du dataset synthétique, entraînement et inférence.
- [main.py](main.py) : API FastAPI.
- [android/app/src/main/java/com/example/fcfa_detector/MainActivity.kt](android/app/src/main/java/com/example/fcfa_detector/MainActivity.kt) : écran Android principal.
- [android/app/src/main/res/layout/activity_main.xml](android/app/src/main/res/layout/activity_main.xml) : interface de l’application.

## Prérequis
- Python 3.10+
- Android Studio Hedgehog ou plus récent
- Un compte GitHub
- Un hébergeur pour l’API Python : Render, Railway, Fly.io, Azure App Service, etc.

## 1. Lancer le backend localement
1. Ouvrir un terminal dans la racine du projet.
2. Créer l’environnement virtuel :
   - `python -m venv .venv`
3. Activer l’environnement :
   - Windows PowerShell : `.venv\Scripts\Activate.ps1`
4. Installer les dépendances :
   - `pip install -r requirements.txt`
5. Lancer l’API :
   - `uvicorn main:app --host 0.0.0.0 --port 8000`
6. Vérifier :
   - Ouvrir `http://localhost:8000/health`
   - Vous devez voir : `{"status":"ok"}`

## 2. Déployer le backend en production
### Option A : Render
1. Pousser le projet sur GitHub.
2. Se connecter à Render.
3. Cliquer sur New Web Service.
4. Choisir le dépôt GitHub.
5. Définir la commande de démarrage :
   - `gunicorn main:app -k uvicorn.workers.UvicornWorker --host 0.0.0.0 --port $PORT`
6. Déployer.
7. Récupérer l’URL publique de votre API, par exemple :
   - `https://nom-service.onrender.com`

### Option B : Railway
1. Connecter le dépôt GitHub à Railway.
2. Ajouter un service Python.
3. Définir la commande de démarrage :
   - `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. Déployer et récupérer l’URL publique.

### Option C : Docker
1. Construire l’image :
   - `docker build -t fcfa-detector .`
2. Lancer le conteneur :
   - `docker run -p 8000:8000 fcfa-detector`

## 3. Préparer l’application Android
1. Ouvrir le dossier [android](android) dans Android Studio.
2. Dans [android/app/src/main/java/com/example/fcfa_detector/MainActivity.kt](android/app/src/main/java/com/example/fcfa_detector/MainActivity.kt), remplacer l’URL de l’API :
   - `https://your-api-url.com/predict-image`
   - par votre vraie URL backend.
3. Compiler et installer l’application.

## 4. Builder et installer sur un téléphone
1. Dans Android Studio, ouvrir le projet [android](android).
2. Connecter un téléphone Android en mode développeur.
3. Cliquer sur Run > Run 'app'.
4. L’application sera installée et lancée sur le téléphone.

## 5. Tester l’application
- Choisir une image depuis la galerie.
- Ou prendre une photo avec la caméra.
- Appuyer sur Envoyer au détecteur.
- L’API renverra une prédiction au format JSON.

## 6. Améliorations recommandées pour un vrai produit
- Remplacer le dataset synthétique par des photos réelles de billets FCFA.
- Utiliser un modèle plus robuste comme MobileNet, EfficientNet ou YOLO.
- Ajouter une vraie détection de zone du billet avant la classification.
- Déployer l’application avec un backend sécurisé et une authentification si nécessaire.

## Important
Le modèle actuel est un prototype. Il montre le flux complet, mais il ne suffit pas encore pour une production robuste.
