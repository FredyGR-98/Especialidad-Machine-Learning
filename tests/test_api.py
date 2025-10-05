"""
===========================================================
🧪 tests/test_api.py — Pruebas automáticas (pytest)
===========================================================

Estas pruebas validan el funcionamiento de la API de Flask:
1. Revisa que /health responda correctamente.
2. Verifica que /model/info contenga features y métricas.
3. Evalúa predicción para un caso válido (Benigno).
4. Evalúa manejo de errores con datos inválidos.

✅ Diseñado para integrarse con CI/CD (GitHub Actions).
===========================================================
"""

import requests
import os

# URL de la API: usa variable de entorno si existe, sino localhost
BASE_URL = os.environ.get("API_URL", "http://127.0.0.1:5000")

# Caso benigno (simplificado con algunos features clave)
CASE_BENIGN = {
    "mean radius": 12.32,
    "mean texture": 12.39,
    "mean perimeter": 78.85,
    "mean area": 464.1,
    "mean smoothness": 0.1028,
    "mean compactness": 0.06981,
    "mean concavity": 0.03987,
    "mean concave points": 0.037,
    "mean symmetry": 0.1959,
    "mean fractal dimension": 0.05955,
}

# Caso inválido (estructura incorrecta)
CASE_INVALID = {"foo": "bar"}


def test_health():
    """Prueba que el endpoint /health responde correctamente."""
    r = requests.get(f"{BASE_URL}/health")
    assert r.status_code == 200
    data = r.json()
    assert "status" in data
    assert data["status"] == "ok"


def test_model_info():
    """Prueba que /model/info devuelve información esperada."""
    r = requests.get(f"{BASE_URL}/model/info")
    assert r.status_code == 200
    data = r.json()
    assert "features" in data
    assert "metrics" in data
    assert isinstance(data["features"], list)


def test_predict_valid():
    """Prueba /predict con un caso válido (benigno)."""
    r = requests.post(f"{BASE_URL}/predict", json=CASE_BENIGN)
    assert r.status_code == 200
    data = r.json()
    assert "prediction" in data
    assert "probability" in data
    assert isinstance(data["probability"], list)


def test_predict_invalid():
    """Prueba /predict con datos inválidos (estructura incorrecta)."""
    r = requests.post(f"{BASE_URL}/predict", json=CASE_INVALID)
    assert r.status_code == 400
    data = r.json()
    assert "error" in data