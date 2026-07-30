"""
Pruebas automatizadas para la API Flask del proyecto.

Estas pruebas validan:
- disponibilidad de endpoints base
- consistencia de metadata del modelo
- predicción con un ejemplo completo
- rechazo de payloads incompletos
"""

from api.api import app


def test_health():
    """Valida que el endpoint de salud responda correctamente."""
    with app.test_client() as client:
        response = client.get("/health")

    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "ok"


def test_model_info():
    """Valida que la API exponga features, labels y métricas."""
    with app.test_client() as client:
        response = client.get("/model/info")

    assert response.status_code == 200
    data = response.get_json()
    assert "features" in data
    assert "metrics" in data
    assert "class_labels" in data
    assert len(data["features"]) == 30
    assert data["class_labels"] == ["Malignant", "Benign"]


def test_predict_valid_example_case():
    """Valida predicción usando un ejemplo completo generado por entrenamiento."""
    with app.test_client() as client:
        examples_response = client.get("/examples")
        assert examples_response.status_code == 200
        examples = examples_response.get_json()

        payload = examples["benign_case"]
        response = client.post("/predict", json=payload)

    assert response.status_code == 200
    data = response.get_json()
    assert "prediction" in data
    assert "probability" in data
    assert "class_probabilities" in data
    assert "predicted_class" in data
    assert set(data["class_probabilities"].keys()) == {"Malignant", "Benign"}


def test_predict_rejects_incomplete_payload():
    """Valida que /predict rechace entradas incompletas."""
    incomplete_case = {
        "mean radius": 12.32,
        "mean texture": 12.39,
        "mean perimeter": 78.85,
    }

    with app.test_client() as client:
        response = client.post("/predict", json=incomplete_case)

    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data
    assert "missing_features" in data
    assert "mean area" in data["missing_features"]
