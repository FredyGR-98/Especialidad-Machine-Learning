"""
===========================================================
📌 api.py — API Flask para exponer el modelo entrenado
===========================================================

Esta API carga los artefactos generados en train_model.py
y expone endpoints para predicción, métricas e imágenes.

⚠️ IMPORTANTE:
Este proyecto es con fines EDUCATIVOS y no constituye diagnóstico médico.
===========================================================
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import joblib
import json
from pathlib import Path
import pandas as pd
import logging
import os

# === CONFIGURACIÓN DE RUTAS ===
BASE_DIR = Path(__file__).resolve().parent.parent
ARTIFACTS_DIR = BASE_DIR / "artifacts"

MODEL_PATH = ARTIFACTS_DIR / "model" / "model.pkl"
FEATURE_INFO_PATH = ARTIFACTS_DIR / "info" / "feature_info.json"
METRICS_PATH = ARTIFACTS_DIR / "info" / "model_metrics.json"
EXAMPLES_PATH = ARTIFACTS_DIR / "info" / "example_cases.json"
VISUALIZATIONS_DIR = ARTIFACTS_DIR / "visualizations"

# === INICIALIZACIÓN ===
app = Flask(__name__)
CORS(app)

# Configuración de logging
LOG_LEVEL = os.getenv("DEBUG", "false").lower() == "true"
logging.basicConfig(
    level=logging.DEBUG if LOG_LEVEL else logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = app.logger

# Cargar artefactos en memoria al iniciar
model = joblib.load(MODEL_PATH)
with open(FEATURE_INFO_PATH) as f:
    feature_info = json.load(f)
with open(METRICS_PATH) as f:
    metrics = json.load(f)
with open(EXAMPLES_PATH) as f:
    examples = json.load(f)


# === ENDPOINTS ===
@app.route("/", methods=["GET"])
def root():
    return jsonify({
        "message": "Bienvenido a la API de Clasificación de Cáncer de Mama 🚀",
        "endpoints": {
            "/health": "Prueba de estado",
            "/model/info": "Información del modelo y métricas",
            "/examples": "Casos de ejemplo (benigno/maligno)",
            "/predict": "Predicción individual (POST JSON)",
            "/predict/batch": "Predicción por lotes (POST CSV)",
            "/visualizations/<filename>": "Visualizaciones generadas"
        }
    })


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "message": "API funcionando 🚀"})


@app.route("/model/info", methods=["GET"])
def model_info():
    return jsonify({
        "features": feature_info["feature_names"],
        "targets": feature_info["target_names"],
        "metrics": metrics
    })


@app.route("/examples", methods=["GET"])
def example_cases():
    return jsonify(examples)


@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No se enviaron datos en el JSON"}), 400

        # 🚨 Nueva validación: asegurar que sea un dict y que tenga al menos una feature válida
        if not isinstance(data, dict):
            return jsonify({"error": "El formato debe ser un diccionario JSON"}), 400

        valid_features = set(feature_info["feature_names"])
        provided_features = set(data.keys())

        if not provided_features.issubset(valid_features):
            return jsonify({
                "error": "Se enviaron características inválidas",
                "invalid_features": list(provided_features - valid_features)
            }), 400

        if len(provided_features) == 0:
            return jsonify({"error": "No se enviaron características reconocidas"}), 400

        # Convertir a DataFrame y asegurar todas las columnas
        df = pd.DataFrame([data])
        df = df.reindex(columns=feature_info["feature_names"], fill_value=0)

        logger.debug(f"/predict recibido con {len(data)} features")

        prediction = model.predict(df)[0]
        proba = model.predict_proba(df)[0].tolist()

        return jsonify({
            "input": data,
            "prediction": int(prediction),
            "probability": proba
        }), 200
    except Exception as e:
        logger.error(f"Error en /predict: {str(e)}")
        return jsonify({"error": "Error en la predicción. Revisa los datos enviados."}), 400

@app.route("/predict/batch", methods=["POST"])
def predict_batch():
    try:
        if "file" not in request.files:
            return jsonify({"error": "No se encontró archivo en la petición"}), 400

        file = request.files["file"]
        df = pd.read_csv(file)

        df = df.reindex(columns=feature_info["feature_names"], fill_value=0)

        predictions = model.predict(df).tolist()
        probas = model.predict_proba(df).tolist()

        return jsonify({
            "predictions": predictions,
            "probabilities": probas
        })
    except Exception as e:
        logger.error(f"Error en /predict/batch: {str(e)}")
        return jsonify({"error": "Error al procesar el archivo. Revisa el formato CSV."}), 400


@app.route("/visualizations/<filename>", methods=["GET"])
def get_visualization(filename):
    try:
        return send_from_directory(VISUALIZATIONS_DIR, filename)
    except Exception as e:
        logger.error(f"Error al acceder a visualización {filename}: {str(e)}")
        return jsonify({"error": "Visualización no encontrada"}), 404


# === MAIN ===
if __name__ == "__main__":
    app.run(debug=LOG_LEVEL, host="0.0.0.0", port=5000)