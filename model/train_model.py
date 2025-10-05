"""
===========================================================
📌 train_model.py — Entrenamiento y generación de artefactos
===========================================================

Este script entrena un modelo de clasificación de cáncer de mama,
genera métricas, visualizaciones y guarda todos los artefactos
necesarios para que luego sean servidos por la API y mostrados en
el frontend.

⚠️ IMPORTANTE:
Este proyecto es con fines EDUCATIVOS y no constituye diagnóstico médico.
===========================================================
"""
# === IMPORTACIONES ===
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import json
import joblib
from pathlib import Path
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score, f1_score, roc_auc_score,
    confusion_matrix, roc_curve
)

# 🔧 FIX: importar utils aunque corras desde /model
import sys
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))  

from utils.feature_names import FEATURE_TRANSLATIONS

# === CONFIGURACIÓN DE RUTAS ===
BASE_DIR = Path(__file__).resolve().parent.parent
ARTIFACTS_DIR = BASE_DIR / "artifacts"

MODEL_PATH = ARTIFACTS_DIR / "model" / "model.pkl"
FEATURE_INFO_PATH = ARTIFACTS_DIR / "info" / "feature_info.json"
METRICS_PATH = ARTIFACTS_DIR / "info" / "model_metrics.json"
EXAMPLES_PATH = ARTIFACTS_DIR / "info" / "example_cases.json"
VISUALIZATIONS_DIR = ARTIFACTS_DIR / "visualizations"

# Crear subcarpetas si no existen
for folder in [MODEL_PATH.parent, FEATURE_INFO_PATH.parent, VISUALIZATIONS_DIR]:
    folder.mkdir(parents=True, exist_ok=True)


# === 1. CARGA DE DATOS ===
def load_data():
    dataset = load_breast_cancer()
    X = pd.DataFrame(dataset.data, columns=dataset.feature_names)
    y = pd.Series(dataset.target)
    return X, y, dataset


# === 2. ENTRENAMIENTO ===
def train_model(X, y):
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    model = RandomForestClassifier(
        n_estimators=200,
        max_depth=6,
        random_state=42,
        class_weight="balanced"
    )
    model.fit(X_train, y_train)

    # Predicciones
    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]

    # Métricas
    metrics = {
        "accuracy": accuracy_score(y_test, y_pred),
        "f1_score": f1_score(y_test, y_pred),
        "roc_auc": roc_auc_score(y_test, y_proba),
    }

    return model, metrics, (X_test, y_test, y_pred, y_proba)


# === 3. GUARDADO DEL MODELO Y METADATA ===
def save_artifacts(model, dataset, metrics, X_test):
    # Guardar modelo
    joblib.dump(model, MODEL_PATH)

    # Guardar info de features
    feature_info = {
        "feature_names": list(dataset.feature_names),
        "target_names": list(dataset.target_names)
    }
    with open(FEATURE_INFO_PATH, "w") as f:
        json.dump(feature_info, f, indent=4)

    # Guardar métricas
    with open(METRICS_PATH, "w") as f:
        json.dump(metrics, f, indent=4)

    # Guardar ejemplos precargados
    examples = {
        "benign_case": X_test.iloc[0].to_dict(),
        "malignant_case": X_test.iloc[-1].to_dict()
    }
    with open(EXAMPLES_PATH, "w") as f:
        json.dump(examples, f, indent=4)

# === 4. VISUALIZACIONES ===
def generate_visualizations(y_test, y_pred, y_proba, model, X):
    from sklearn.metrics import confusion_matrix, roc_curve, roc_auc_score
    import seaborn as sns
    import matplotlib.pyplot as plt
    import numpy as np

    def save_confusion(cm, theme):
        plt.figure(figsize=(6, 5))
        cmap = "RdPu" if theme == "light" else "magma"
        annot_color = "black" if theme == "light" else "white"
        facecolor = "white" if theme == "light" else "black"

        if theme == "dark":
            plt.style.use("dark_background")

        sns.heatmap(
            cm, annot=True, fmt="d", cmap=cmap, cbar=True,
            xticklabels=["Benigno", "Maligno"],
            yticklabels=["Benigno", "Maligno"],
            annot_kws={"color": annot_color}
        )
        plt.title("Matriz de Confusión — Clasificador de Cáncer de Mama",
                  fontsize=14, pad=15, color=annot_color)
        plt.xlabel("Predicción", fontsize=12, color=annot_color)
        plt.ylabel("Real", fontsize=12, color=annot_color)
        plt.tight_layout()
        plt.savefig(VISUALIZATIONS_DIR / f"confusion_matrix_{theme}.png",
                    dpi=150, facecolor=facecolor)
        plt.close()

    def save_roc(fpr, tpr, auc, theme):
        plt.figure(figsize=(6, 5))
        color = "deeppink" if theme == "light" else "cyan"
        text_color = "black" if theme == "light" else "white"
        facecolor = "white" if theme == "light" else "black"

        if theme == "dark":
            plt.style.use("dark_background")

        plt.plot(fpr, tpr, color=color, linewidth=2, label=f"AUC = {auc:.2f}")
        plt.plot([0, 1], [0, 1], linestyle="--", color="gray")
        plt.xlabel("Tasa de Falsos Positivos", fontsize=12, color=text_color)
        plt.ylabel("Tasa de Verdaderos Positivos", fontsize=12, color=text_color)
        plt.title("Curva ROC — Clasificador de Cáncer de Mama",
                  fontsize=14, pad=15, color=text_color)
        plt.legend(loc="lower right")
        plt.tight_layout()
        plt.savefig(VISUALIZATIONS_DIR / f"roc_curve_{theme}.png",
                    dpi=150, facecolor=facecolor)
        plt.close()

    def save_importance(importances, idx, X, theme):
        plt.figure(figsize=(8, 6))
        colors = (plt.cm.PuRd if theme == "light" else plt.cm.plasma)(
            np.linspace(0.4, 0.9, len(idx))
        )
        text_color = "black" if theme == "light" else "white"
        facecolor = "white" if theme == "light" else "black"

        if theme == "dark":
            plt.style.use("dark_background")

        plt.barh(range(len(idx)), importances[idx], align="center", color=colors)
        plt.yticks(
            range(len(idx)),
            [FEATURE_TRANSLATIONS.get(col, col) for col in np.array(X.columns)[idx]],
            fontsize=10, color=text_color
        )
        plt.title("Top 10 Características más Importantes",
                  fontsize=14, pad=15, color=text_color)
        plt.xlabel("Importancia", fontsize=12, color=text_color)
        plt.ylabel("Características", fontsize=12, color=text_color)
        plt.tight_layout()
        plt.savefig(VISUALIZATIONS_DIR / f"feature_importance_{theme}.png",
                    dpi=150, facecolor=facecolor)
        plt.close()

    def save_correlation(corr, theme):
        plt.figure(figsize=(12, 10))
        cmap = "RdPu" if theme == "light" else "inferno"
        text_color = "black" if theme == "light" else "white"
        facecolor = "white" if theme == "light" else "black"

        if theme == "dark":
            plt.style.use("dark_background")

        sns.heatmap(corr, cmap=cmap, center=0, xticklabels=True, yticklabels=True)
        plt.title("Matriz de Correlación (Características)",
                  fontsize=14, pad=15, color=text_color)
        plt.xticks(rotation=90, ha="right", fontsize=8, color=text_color)
        plt.yticks(rotation=0, fontsize=8, color=text_color)
        plt.tight_layout()
        plt.savefig(VISUALIZATIONS_DIR / f"correlation_matrix_{theme}.png",
                    dpi=200, facecolor=facecolor)
        plt.close()

    # === Datos para gráficas ===
    cm = confusion_matrix(y_test, y_pred)
    fpr, tpr, _ = roc_curve(y_test, y_proba)
    auc = roc_auc_score(y_test, y_proba)
    importances = model.feature_importances_
    idx = np.argsort(importances)[-10:]
    corr = X.corr()

    # === Generar ambas versiones ===
    for theme in ["light", "dark"]:
        save_confusion(cm, theme)
        save_roc(fpr, tpr, auc, theme)
        save_importance(importances, idx, X, theme)
        save_correlation(corr, theme)

# === MAIN ===
if __name__ == "__main__":
    print("🚀 Iniciando entrenamiento")

    X, y, dataset = load_data()
    model, metrics, results = train_model(X, y)
    save_artifacts(model, dataset, metrics, results[0])
    generate_visualizations(results[1], results[2], results[3], model, X)

    print("✅ Entrenamiento completo. Artefactos guardados en /artifacts/")