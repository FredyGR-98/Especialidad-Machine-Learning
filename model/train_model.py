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
import json
import sys
from pathlib import Path

import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.datasets import load_breast_cancer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    roc_auc_score,
    roc_curve,
)
from sklearn.model_selection import train_test_split

# === CONFIGURACIÓN DE RUTAS ===
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from utils.feature_names import FEATURE_TRANSLATIONS

ARTIFACTS_DIR = BASE_DIR / "artifacts"

MODEL_PATH = ARTIFACTS_DIR / "model" / "model.pkl"
FEATURE_INFO_PATH = ARTIFACTS_DIR / "info" / "feature_info.json"
METRICS_PATH = ARTIFACTS_DIR / "info" / "model_metrics.json"
EXAMPLES_PATH = ARTIFACTS_DIR / "info" / "example_cases.json"
VISUALIZATIONS_DIR = ARTIFACTS_DIR / "visualizations"

# Crear subcarpetas si no existen
for folder in [MODEL_PATH.parent, FEATURE_INFO_PATH.parent, VISUALIZATIONS_DIR]:
    folder.mkdir(parents=True, exist_ok=True)

# === PALETA VISUAL DEL PROYECTO ===
PINK_MAIN = "#E75480"
PINK_DARK = "#C2185B"
PINK_SOFT = "#F8BBD0"
PINK_BG = "#FFF4F8"
CARD_BG = "#FFFFFF"
TEXT_MAIN = "#4A3B47"
ACCENT = "#B388C4"
GRID_SOFT = "#F3D6E2"


# === 1. CARGA DE DATOS ===
def load_data():
    """
    Carga el dataset de cáncer de mama desde sklearn y lo
    transforma a estructuras pandas para facilitar el trabajo.
    """
    dataset = load_breast_cancer()
    X = pd.DataFrame(dataset.data, columns=dataset.feature_names)
    y = pd.Series(dataset.target)
    return X, y, dataset


# === 2. ENTRENAMIENTO ===
def train_model(X, y):
    """
    Divide los datos en entrenamiento y prueba, entrena un modelo
    RandomForest y calcula métricas principales.
    """
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )

    model = RandomForestClassifier(
        n_estimators=200,
        max_depth=6,
        random_state=42,
        class_weight="balanced",
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
    """
    Guarda el modelo entrenado, metadata del dataset,
    métricas y ejemplos de casos.
    """
    # Guardar modelo
    joblib.dump(model, MODEL_PATH)

    # Guardar info de features
    feature_info = {
        "feature_names": list(dataset.feature_names),
        "target_names": list(dataset.target_names),
    }
    with open(FEATURE_INFO_PATH, "w", encoding="utf-8") as f:
        json.dump(feature_info, f, indent=4, ensure_ascii=False)

    # Guardar métricas
    with open(METRICS_PATH, "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=4, ensure_ascii=False)

    # Guardar ejemplos precargados
    examples = {
        "benign_case": X_test.iloc[0].to_dict(),
        "malignant_case": X_test.iloc[-1].to_dict(),
    }
    with open(EXAMPLES_PATH, "w", encoding="utf-8") as f:
        json.dump(examples, f, indent=4, ensure_ascii=False)


# === 4. CONFIGURACIÓN GLOBAL DE ESTILO ===
def apply_plot_style():
    """
    Aplica una configuración visual coherente con la nueva interfaz:
    fondo pastel, texto oscuro suave y acentos rosados.
    """
    plt.style.use("default")
    sns.set_theme(style="whitegrid")

    plt.rcParams.update(
        {
            "figure.facecolor": PINK_BG,
            "axes.facecolor": CARD_BG,
            "axes.edgecolor": PINK_SOFT,
            "axes.labelcolor": TEXT_MAIN,
            "text.color": TEXT_MAIN,
            "xtick.color": TEXT_MAIN,
            "ytick.color": TEXT_MAIN,
            "grid.color": GRID_SOFT,
            "grid.alpha": 0.6,
            "axes.titleweight": "bold",
            "font.size": 11,
        }
    )


# === 5. LIMPIEZA DE VISUALIZACIONES ANTIGUAS ===
def remove_old_visualizations():
    """
    Elimina gráficos antiguos del esquema light/dark para evitar
    confusiones dentro de artifacts/visualizations.
    """
    old_files = [
        "confusion_matrix_light.png",
        "confusion_matrix_dark.png",
        "roc_curve_light.png",
        "roc_curve_dark.png",
        "feature_importance_light.png",
        "feature_importance_dark.png",
        "correlation_matrix_light.png",
        "correlation_matrix_dark.png",
    ]

    for filename in old_files:
        file_path = VISUALIZATIONS_DIR / filename
        if file_path.exists():
            file_path.unlink()


# === 6. VISUALIZACIONES ===
def generate_visualizations(y_test, y_pred, y_proba, model, X):
    """
    Genera las visualizaciones finales en una sola modalidad:
    estética rosada/pastel coherente con la UI del proyecto.
    """
    apply_plot_style()
    remove_old_visualizations()

    print("BASE_DIR:", BASE_DIR)
    print("ARTIFACTS_DIR:", ARTIFACTS_DIR)
    print("VISUALIZATIONS_DIR:", VISUALIZATIONS_DIR)

    # === Datos base para las gráficas ===
    cm = confusion_matrix(y_test, y_pred)
    fpr, tpr, _ = roc_curve(y_test, y_proba)
    auc = roc_auc_score(y_test, y_proba)

    importances = model.feature_importances_
    idx = np.argsort(importances)[-10:]
    idx_sorted = idx[np.argsort(importances[idx])]

    corr = X.corr()

    # === 6.1 MATRIZ DE CONFUSIÓN ===
    plt.figure(figsize=(6.5, 5.5))
    pink_cmap = sns.light_palette(PINK_MAIN, as_cmap=True)

    ax = sns.heatmap(
        cm,
        annot=True,
        fmt="d",
        cmap=pink_cmap,
        cbar=True,
        linewidths=1.2,
        linecolor=PINK_SOFT,
        xticklabels=["Benigno", "Maligno"],
        yticklabels=["Benigno", "Maligno"],
        annot_kws={"color": TEXT_MAIN, "fontsize": 12, "weight": "bold"},
    )

    ax.set_title(
        "Matriz de Confusión — Clasificador de Cáncer de Mama",
        fontsize=15,
        color=PINK_DARK,
        pad=14,
    )
    ax.set_xlabel("Predicción", fontsize=12, color=TEXT_MAIN)
    ax.set_ylabel("Real", fontsize=12, color=TEXT_MAIN)

    cm_path = VISUALIZATIONS_DIR / "confusion_matrix_pink.png"
    plt.tight_layout()
    plt.savefig(cm_path, dpi=300, bbox_inches="tight", facecolor=PINK_BG)
    plt.close()
    print("Guardado:", cm_path)

    # === 6.2 CURVA ROC ===
    plt.figure(figsize=(6.5, 5.5))

    plt.plot(
        fpr,
        tpr,
        color=PINK_MAIN,
        linewidth=3,
        label=f"AUC = {auc:.3f}",
    )
    plt.plot(
        [0, 1],
        [0, 1],
        linestyle="--",
        color=ACCENT,
        linewidth=1.8,
        label="Clasificador aleatorio",
    )

    plt.title(
        "Curva ROC — Clasificador de Cáncer de Mama",
        fontsize=15,
        color=PINK_DARK,
        pad=14,
    )
    plt.xlabel("Tasa de Falsos Positivos", fontsize=12, color=TEXT_MAIN)
    plt.ylabel("Tasa de Verdaderos Positivos", fontsize=12, color=TEXT_MAIN)
    plt.legend(loc="lower right", frameon=True, facecolor="white", edgecolor=PINK_SOFT)

    roc_path = VISUALIZATIONS_DIR / "roc_curve_pink.png"
    plt.tight_layout()
    plt.savefig(roc_path, dpi=300, bbox_inches="tight", facecolor=PINK_BG)
    plt.close()
    print("Guardado:", roc_path)

    # === 6.3 IMPORTANCIA DE VARIABLES ===
    plt.figure(figsize=(9, 6.5))

    translated_names = [
        FEATURE_TRANSLATIONS.get(col, col) for col in np.array(X.columns)[idx_sorted]
    ]

    colors = sns.color_palette(
        ["#F8BBD0", "#F48FB1", "#EC7098", "#E75480", "#C2185B"],
        n_colors=len(idx_sorted),
    )

    plt.barh(
        range(len(idx_sorted)),
        importances[idx_sorted],
        color=colors,
        edgecolor=PINK_SOFT,
    )

    plt.yticks(
        range(len(idx_sorted)),
        translated_names,
        fontsize=10,
        color=TEXT_MAIN,
    )
    plt.xlabel("Importancia", fontsize=12, color=TEXT_MAIN)
    plt.ylabel("Características", fontsize=12, color=TEXT_MAIN)
    plt.title(
        "Top 10 Características Más Importantes",
        fontsize=15,
        color=PINK_DARK,
        pad=14,
    )

    fi_path = VISUALIZATIONS_DIR / "feature_importance_pink.png"
    plt.tight_layout()
    plt.savefig(fi_path, dpi=300, bbox_inches="tight", facecolor=PINK_BG)
    plt.close()
    print("Guardado:", fi_path)

    # === 6.4 MATRIZ DE CORRELACIÓN ===
    plt.figure(figsize=(13, 10))

    corr_cmap = sns.diverging_palette(340, 15, s=85, l=55, as_cmap=True)

    ax = sns.heatmap(
        corr,
        cmap=corr_cmap,
        center=0,
        xticklabels=True,
        yticklabels=True,
        linewidths=0.2,
        linecolor=PINK_BG,
        cbar=True,
    )

    ax.set_title(
        "Matriz de Correlación (Características)",
        fontsize=15,
        color=PINK_DARK,
        pad=14,
    )
    plt.xticks(rotation=90, ha="right", fontsize=8, color=TEXT_MAIN)
    plt.yticks(rotation=0, fontsize=8, color=TEXT_MAIN)

    corr_path = VISUALIZATIONS_DIR / "correlation_matrix_pink.png"
    plt.tight_layout()
    plt.savefig(corr_path, dpi=250, bbox_inches="tight", facecolor=PINK_BG)
    plt.close()
    print("Guardado:", corr_path)


# === MAIN ===
if __name__ == "__main__":
    print("🚀 Iniciando entrenamiento")

    X, y, dataset = load_data()
    model, metrics, results = train_model(X, y)
    save_artifacts(model, dataset, metrics, results[0])
    generate_visualizations(results[1], results[2], results[3], model, X)

    print("✅ Entrenamiento completo. Artefactos guardados en /artifacts/")