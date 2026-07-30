"""
API Flask para exponer el modelo entrenado.

Esta API carga los artefactos generados en `train_model.py`
y expone endpoints para predicción, métricas e imágenes.

Este proyecto tiene fines educativos y no constituye diagnóstico médico.
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import joblib
import json
from pathlib import Path
import pandas as pd
import logging
import os
import sys

# === CONFIGURACIÓN DE RUTAS ===
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

from database.db_manager import DatabaseManager

ARTIFACTS_DIR = BASE_DIR / "artifacts"

MODEL_PATH = ARTIFACTS_DIR / "model" / "model.pkl"
FEATURE_INFO_PATH = ARTIFACTS_DIR / "info" / "feature_info.json"
METRICS_PATH = ARTIFACTS_DIR / "info" / "model_metrics.json"
EXAMPLES_PATH = ARTIFACTS_DIR / "info" / "example_cases.json"
VISUALIZATIONS_DIR = ARTIFACTS_DIR / "visualizations"

# === INICIALIZACIÓN ===
app = Flask(__name__)
CORS(app)

LOG_LEVEL = os.getenv("DEBUG", "false").lower() == "true"
logging.basicConfig(
    level=logging.DEBUG if LOG_LEVEL else logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = app.logger

# Cargar artefactos
model = joblib.load(MODEL_PATH)

with open(FEATURE_INFO_PATH, encoding="utf-8") as f:
    feature_info = json.load(f)

with open(METRICS_PATH, encoding="utf-8") as f:
    metrics = json.load(f)

with open(EXAMPLES_PATH, encoding="utf-8") as f:
    examples = json.load(f)

# DB manager
db = DatabaseManager()

# =========================================================
# MAPEO ENTRE NOMBRES DE DB Y NOMBRES DEL MODELO
# =========================================================
FEATURE_NAME_MAP = {
    "radius_mean": "mean radius",
    "texture_mean": "mean texture",
    "perimeter_mean": "mean perimeter",
    "area_mean": "mean area",
    "smoothness_mean": "mean smoothness",
    "compactness_mean": "mean compactness",
    "concavity_mean": "mean concavity",
    "concave_points_mean": "mean concave points",
    "symmetry_mean": "mean symmetry",
    "fractal_dimension_mean": "mean fractal dimension",

    "radius_se": "radius error",
    "texture_se": "texture error",
    "perimeter_se": "perimeter error",
    "area_se": "area error",
    "smoothness_se": "smoothness error",
    "compactness_se": "compactness error",
    "concavity_se": "concavity error",
    "concave_points_se": "concave points error",
    "symmetry_se": "symmetry error",
    "fractal_dimension_se": "fractal dimension error",

    "radius_worst": "worst radius",
    "texture_worst": "worst texture",
    "perimeter_worst": "worst perimeter",
    "area_worst": "worst area",
    "smoothness_worst": "worst smoothness",
    "compactness_worst": "worst compactness",
    "concavity_worst": "worst concavity",
    "concave_points_worst": "worst concave points",
    "symmetry_worst": "worst symmetry",
    "fractal_dimension_worst": "worst fractal dimension"
}

MODEL_FEATURE_SET = set(feature_info["feature_names"])
DB_FEATURE_SET = set(FEATURE_NAME_MAP.keys())
CLASS_LABELS = feature_info.get(
    "class_labels",
    [str(label).strip().capitalize() for label in feature_info["target_names"]],
)


# =========================================================
# FUNCIONES AUXILIARES
# =========================================================
def validate_feature_payload(data: dict) -> tuple[bool, dict | None, int]:
    """
    Valida que el payload tenga formato correcto y solo features válidas
    para el modelo ya entrenado.
    """
    if not data:
        return False, {"error": "No se enviaron datos en el JSON"}, 400

    if not isinstance(data, dict):
        return False, {"error": "El formato debe ser un diccionario JSON"}, 400

    valid_features = MODEL_FEATURE_SET
    provided_features = set(data.keys())
    missing_features = valid_features - provided_features

    if not provided_features.issubset(valid_features):
        return False, {
            "error": "Se enviaron características inválidas para el modelo",
            "invalid_features": sorted(list(provided_features - valid_features))
        }, 400

    if missing_features:
        return False, {
            "error": "Faltan características obligatorias para ejecutar la predicción",
            "missing_features": sorted(list(missing_features))
        }, 400

    return True, None, 200


def validate_measurement_keys(measurement_data: dict) -> tuple[bool, dict | None, int]:
    """
    Valida que el bloque measurement tenga exactamente las 30 variables
    clínicas esperadas en formato snake_case.
    """
    if not measurement_data:
        return False, {"error": "No se enviaron mediciones clínicas"}, 400

    if not isinstance(measurement_data, dict):
        return False, {"error": "measurement debe ser un diccionario JSON"}, 400

    required_keys = DB_FEATURE_SET
    provided_keys = set(measurement_data.keys())

    missing_keys = required_keys - provided_keys
    invalid_keys = provided_keys - required_keys

    if missing_keys:
        return False, {
            "error": "Faltan variables clínicas obligatorias",
            "missing_features": sorted(list(missing_keys))
        }, 400

    if invalid_keys:
        return False, {
            "error": "Se enviaron características inválidas en measurement",
            "invalid_features": sorted(list(invalid_keys))
        }, 400

    return True, None, 200


def map_measurement_to_model_features(measurement_data: dict) -> dict:
    """
    Convierte nombres snake_case usados en la base de datos
    a los nombres originales que espera el modelo entrenado.
    """
    mapped_data = {}

    for db_key, model_key in FEATURE_NAME_MAP.items():
        if db_key in measurement_data:
            mapped_data[model_key] = measurement_data[db_key]

    return mapped_data


def normalize_prediction_input(data: dict) -> tuple[bool, dict | None, int, dict | None]:
    """
    Permite que /predict acepte:
    - nombres del modelo (ej. 'mean radius')
    - o nombres snake_case del sistema (ej. 'radius_mean')

    Retorna:
        is_valid, error_response, status_code, normalized_data
    """
    if not data:
        return False, {"error": "No se enviaron datos en el JSON"}, 400, None

    if not isinstance(data, dict):
        return False, {"error": "El formato debe ser un diccionario JSON"}, 400, None

    provided_keys = set(data.keys())

    # Caso 1: ya vienen en nombres del modelo
    if provided_keys.issubset(MODEL_FEATURE_SET):
        is_valid, error_response, status_code = validate_feature_payload(data)
        return is_valid, error_response, status_code, data

    # Caso 2: vienen en snake_case del sistema
    if provided_keys.issubset(DB_FEATURE_SET):
        is_valid_measurement, error_response, status_code = validate_measurement_keys(data)
        if not is_valid_measurement:
            return False, error_response, status_code, None

        mapped_data = map_measurement_to_model_features(data)
        is_valid_model, error_response, status_code = validate_feature_payload(mapped_data)
        if not is_valid_model:
            return False, error_response, status_code, None

        return True, None, 200, mapped_data

    # Caso 3: mezcla rara o claves inválidas
    return False, {
        "error": "Se enviaron características inválidas",
        "invalid_features": sorted(list(provided_keys)),
        "hint": "Usa todas las features del modelo o las 30 variables clínicas en snake_case"
    }, 400, None


def build_feature_dataframe(data: dict) -> pd.DataFrame:
    """
    Convierte el payload en DataFrame y garantiza el orden completo de features.
    """
    df = pd.DataFrame([data])
    return df.reindex(columns=feature_info["feature_names"])


def run_model_prediction(data: dict) -> dict:
    """
    Ejecuta predicción y retorna un diccionario estandarizado.
    """
    df = build_feature_dataframe(data)

    prediction = int(model.predict(df)[0])
    probabilities = model.predict_proba(df)[0].tolist()

    predicted_class = CLASS_LABELS[prediction]
    prediction_score = float(max(probabilities))
    model_version = "rf_v1"
    class_probabilities = {
        class_label: float(probabilities[class_index])
        for class_index, class_label in enumerate(CLASS_LABELS)
    }

    return {
        "input": data,
        "prediction": prediction,
        "probability": probabilities,
        "class_probabilities": class_probabilities,
        "predicted_class": predicted_class,
        "prediction_score": prediction_score,
        "model_version": model_version
    }


# =========================================================
# ENDPOINTS BASE
# =========================================================
@app.route("/", methods=["GET"])
def root():
    return jsonify({
        "message": "Bienvenido a la API de clasificación de cáncer de mama",
        "endpoints": {
            "/health": "Prueba de estado",
            "/model/info": "Información del modelo y métricas",
            "/examples": "Casos de ejemplo (benigno/maligno)",
            "/patients": "Lista de pacientes registrados",
            "/patients/<patient_id>": "Detalle de paciente por ID",
            "/patients/<patient_id>/measurements": "Historial clínico de un paciente",
            "/login": "Validación básica de usuario (POST JSON)",
            "/predict": "Predicción individual (POST JSON)",
            "/predict-and-save": "Predicción + guardado en SQLite (POST JSON)",
            "/predict/batch": "Predicción por lotes (POST CSV)",
            "/visualizations/<filename>": "Visualizaciones generadas"
        }
    })


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "message": "API funcionando"})


@app.route("/model/info", methods=["GET"])
def model_info():
    return jsonify({
        "features": feature_info["feature_names"],
        "targets": feature_info["target_names"],
        "class_labels": CLASS_LABELS,
        "metrics": metrics
    })


@app.route("/examples", methods=["GET"])
def example_cases():
    return jsonify(examples)


# =========================================================
# LOGIN
# =========================================================
@app.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json(silent=True)

        if not data:
            return jsonify({"error": "No se enviaron datos en el JSON"}), 400

        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return jsonify({
                "error": "Se requieren username y password"
            }), 400

        user = db.validate_login(username, password)

        if not user:
            return jsonify({
                "success": False,
                "message": "Credenciales inválidas"
            }), 401

        return jsonify({
            "success": True,
            "message": "Login exitoso",
            "user": user
        }), 200

    except Exception as e:
        logger.exception("Error en /login")
        return jsonify({
            "error": "Error al validar el inicio de sesión",
            "detail": str(e)
        }), 500


# =========================================================
# PACIENTES
# =========================================================
@app.route("/patients", methods=["GET"])
def get_patients():
    """
    Lista pacientes registrados.

    Query params opcionales:
        - search: texto para buscar por nombre o RUT
    """
    try:
        search = request.args.get("search", default=None, type=str)
        patients = db.list_patients(search=search)

        return jsonify({
            "success": True,
            "count": len(patients),
            "patients": patients
        }), 200

    except Exception as e:
        logger.exception("Error en /patients")
        return jsonify({
            "success": False,
            "error": "Error al obtener pacientes",
            "detail": str(e)
        }), 500


@app.route("/patients/<int:patient_id>", methods=["GET"])
def get_patient_detail(patient_id: int):
    """
    Obtiene detalle de un paciente por ID.
    """
    try:
        patient = db.get_patient_by_id(patient_id)

        if not patient:
            return jsonify({
                "success": False,
                "error": "Paciente no encontrado"
            }), 404

        return jsonify({
            "success": True,
            "patient": patient
        }), 200

    except Exception as e:
        logger.exception("Error en /patients/<patient_id>")
        return jsonify({
            "success": False,
            "error": "Error al obtener el detalle del paciente",
            "detail": str(e)
        }), 500


@app.route("/patients/<int:patient_id>/measurements", methods=["GET"])
def get_patient_measurements(patient_id: int):
    """
    Obtiene historial clínico de un paciente por ID.
    """
    try:
        patient_data = db.get_patient_with_measurements(patient_id)

        if not patient_data:
            return jsonify({
                "success": False,
                "error": "Paciente no encontrado"
            }), 404

        return jsonify({
            "success": True,
            "patient": patient_data["patient"],
            "count": len(patient_data["measurements"]),
            "measurements": patient_data["measurements"]
        }), 200

    except Exception as e:
        logger.exception("Error en /patients/<patient_id>/measurements")
        return jsonify({
            "success": False,
            "error": "Error al obtener historial del paciente",
            "detail": str(e)
        }), 500


# =========================================================
# PREDICCIÓN SIMPLE
# =========================================================
@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json(silent=True)

        if not data:
            return jsonify({
                "error": "No se pudo interpretar el JSON enviado",
                "raw_data": request.get_data(as_text=True)
            }), 400

        is_valid, error_response, status_code, normalized_data = normalize_prediction_input(data)
        if not is_valid:
            return jsonify(error_response), status_code

        logger.debug(f"/predict recibido con {len(normalized_data)} features")

        result = run_model_prediction(normalized_data)

        return jsonify({
            "input": result["input"],
            "prediction": result["prediction"],
            "probability": result["probability"],
            "class_probabilities": result["class_probabilities"],
            "predicted_class": result["predicted_class"],
            "prediction_score": result["prediction_score"],
            "model_version": result["model_version"]
        }), 200

    except Exception as e:
        logger.exception("Error en /predict")
        return jsonify({
            "error": "Error en la predicción. Revisa los datos enviados.",
            "detail": str(e)
        }), 400


# =========================================================
# PREDICCIÓN + GUARDADO
# =========================================================
@app.route("/predict-and-save", methods=["POST"])
def predict_and_save():
    """
    Espera un JSON con esta estructura:

    {
      "user_id": 1,
      "patient": {
        "rut": "18.123.456-7",
        "full_name": "Paciente de Prueba",
        "age": 45,
        "sex": "F"
      },
      "measurement": {
        ... 30 features en snake_case ...
      },
      "evaluation_date": "2026-03-06"
    }
    """
    try:
        payload = request.get_json(silent=True)
        logger.info(f"Payload recibido en /predict-and-save: {payload}")

        if not payload:
            return jsonify({
                "error": "No se pudo interpretar el JSON enviado",
                "raw_data": request.get_data(as_text=True)
            }), 400

        user_id = payload.get("user_id")
        patient_data = payload.get("patient")
        measurement_data = payload.get("measurement")
        evaluation_date = payload.get("evaluation_date")

        if user_id is None or not patient_data or not measurement_data or not evaluation_date:
            return jsonify({
                "error": "Se requieren user_id, patient, measurement y evaluation_date"
            }), 400

        try:
            user_id = int(user_id)
        except (TypeError, ValueError):
            return jsonify({
                "error": "user_id debe ser un entero válido"
            }), 400

        user = db.get_user_by_id(user_id)
        if not user:
            return jsonify({
                "error": "Usuario no válido o inactivo"
            }), 401

        if not isinstance(patient_data, dict):
            return jsonify({
                "error": "patient debe ser un diccionario JSON"
            }), 400

        rut = patient_data.get("rut")
        full_name = patient_data.get("full_name")
        age = patient_data.get("age")
        sex = patient_data.get("sex")

        if not rut or not full_name or age is None or not sex:
            return jsonify({
                "error": "Datos de paciente incompletos",
                "patient_received": patient_data
            }), 400

        try:
            age = int(age)
        except (TypeError, ValueError):
            return jsonify({
                "error": "La edad del paciente debe ser un entero válido"
            }), 400

        logger.info(f"measurement keys recibidas: {sorted(list(measurement_data.keys()))}")

        # Validar que measurement tenga exactamente las 30 variables snake_case
        is_valid_measurement, error_response, status_code = validate_measurement_keys(measurement_data)
        if not is_valid_measurement:
            logger.warning(f"Measurement inválido: {error_response}")
            return jsonify(error_response), status_code

        # Traducir a nombres que entienda el modelo
        model_input = map_measurement_to_model_features(measurement_data)

        # Validar contra las features reales del modelo
        is_valid_model, error_response, status_code = validate_feature_payload(model_input)
        if not is_valid_model:
            logger.warning(f"Model input inválido: {error_response}")
            return jsonify(error_response), status_code

        # Ejecutar predicción con nombres del modelo
        result = run_model_prediction(model_input)
        logger.info(
            f"Predicción ejecutada correctamente | "
            f"class={result['predicted_class']} | score={result['prediction_score']:.4f}"
        )

        # Reutilizar paciente si ya existe; si no, crearlo
        patient = db.get_or_create_patient(
            rut=rut,
            full_name=full_name,
            age=age,
            sex=sex,
            created_by_user_id=user["user_id"]
        )

        # Guardar medición usando nombres snake_case de la DB
        measurement_id = db.create_clinical_measurement(
            patient_id=patient["patient_id"],
            recorded_by_user_id=user["user_id"],
            evaluation_date=evaluation_date,
            measurement_data=measurement_data,
            predicted_class=result["predicted_class"],
            prediction_score=result["prediction_score"],
            model_version=result["model_version"]
        )

        logger.info(
            f"Registro guardado correctamente | patient_id={patient['patient_id']} | "
            f"measurement_id={measurement_id}"
        )

        return jsonify({
            "success": True,
            "message": "Predicción realizada y registro guardado correctamente",
            "user": {
                "user_id": user["user_id"],
                "username": user["username"],
                "role": user["role"]
            },
            "patient": patient,
            "measurement_id": measurement_id,
            "result": {
                "prediction": result["prediction"],
                "probability": result["probability"],
                "predicted_class": result["predicted_class"],
                "prediction_score": result["prediction_score"],
                "model_version": result["model_version"]
            }
        }), 200

    except Exception as e:
        logger.exception("Error en /predict-and-save")
        return jsonify({
            "error": "Error al procesar la predicción y guardar el registro",
            "detail": str(e)
        }), 500


# =========================================================
# PREDICCIÓN BATCH
# =========================================================
@app.route("/predict/batch", methods=["POST"])
def predict_batch():
    try:
        if "file" not in request.files:
            return jsonify({"error": "No se encontró archivo en la petición"}), 400

        file = request.files["file"]
        df = pd.read_csv(file)
        provided_columns = set(df.columns)
        expected_columns = MODEL_FEATURE_SET
        missing_columns = expected_columns - provided_columns
        invalid_columns = provided_columns - expected_columns

        if missing_columns or invalid_columns:
            return jsonify({
                "error": "El CSV debe contener exactamente las columnas esperadas por el modelo",
                "missing_features": sorted(list(missing_columns)),
                "invalid_features": sorted(list(invalid_columns))
            }), 400

        df = df.reindex(columns=feature_info["feature_names"])

        predictions = model.predict(df).tolist()
        probas = model.predict_proba(df).tolist()

        return jsonify({
            "predictions": predictions,
            "probabilities": probas
        })
    except Exception as e:
        logger.exception("Error en /predict/batch")
        return jsonify({
            "error": "Error al procesar el archivo. Revisa el formato CSV.",
            "detail": str(e)
        }), 400


# =========================================================
# VISUALIZACIONES
# =========================================================
@app.route("/visualizations/<filename>", methods=["GET"])
def get_visualization(filename):
    try:
        return send_from_directory(VISUALIZATIONS_DIR, filename)
    except Exception as e:
        logger.error(f"Error al acceder a visualización {filename}: {str(e)}")
        return jsonify({"error": "Visualización no encontrada"}), 404


# =========================================================
# MAIN
# =========================================================
if __name__ == "__main__":
    app.run(debug=LOG_LEVEL, host="0.0.0.0", port=5000)
