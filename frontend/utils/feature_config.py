"""
===========================================================
feature_config.py
===========================================================

Genera una configuración de entrada para las variables clínicas
del proyecto usando el dataset load_breast_cancer de sklearn.

Responsabilidades:
- Cargar el dataset base.
- Traducir nombres originales a snake_case compatible con la app.
- Calcular min, max, mediana y step sugerido por variable.
- Entregar metadata reutilizable para formularios clínicos.
===========================================================
"""

from __future__ import annotations

import math
from typing import Any

import numpy as np
import pandas as pd
from sklearn.datasets import load_breast_cancer


FEATURE_NAME_MAP = {
    "mean radius": "radius_mean",
    "mean texture": "texture_mean",
    "mean perimeter": "perimeter_mean",
    "mean area": "area_mean",
    "mean smoothness": "smoothness_mean",
    "mean compactness": "compactness_mean",
    "mean concavity": "concavity_mean",
    "mean concave points": "concave_points_mean",
    "mean symmetry": "symmetry_mean",
    "mean fractal dimension": "fractal_dimension_mean",
    "radius error": "radius_se",
    "texture error": "texture_se",
    "perimeter error": "perimeter_se",
    "area error": "area_se",
    "smoothness error": "smoothness_se",
    "compactness error": "compactness_se",
    "concavity error": "concavity_se",
    "concave points error": "concave_points_se",
    "symmetry error": "symmetry_se",
    "fractal dimension error": "fractal_dimension_se",
    "worst radius": "radius_worst",
    "worst texture": "texture_worst",
    "worst perimeter": "perimeter_worst",
    "worst area": "area_worst",
    "worst smoothness": "smoothness_worst",
    "worst compactness": "compactness_worst",
    "worst concavity": "concavity_worst",
    "worst concave points": "concave_points_worst",
    "worst symmetry": "symmetry_worst",
    "worst fractal dimension": "fractal_dimension_worst",
}


def _suggest_step(min_value: float, max_value: float) -> float:
    """
    Sugiere un step razonable según el rango de una variable.

    Args:
        min_value (float): Valor mínimo observado.
        max_value (float): Valor máximo observado.

    Returns:
        float: Paso sugerido para number_input.
    """
    span = max_value - min_value

    if span <= 0:
        return 0.001

    raw_step = span / 200

    if raw_step >= 10:
        return 1.0
    if raw_step >= 1:
        return 0.1
    if raw_step >= 0.1:
        return 0.01
    if raw_step >= 0.01:
        return 0.001

    return 0.0001


def build_feature_input_config() -> dict[str, dict[str, Any]]:
    """
    Construye metadata de entrada para las variables clínicas
    usando el dataset base de sklearn.

    Returns:
        dict[str, dict[str, Any]]: Configuración por variable.
    """
    dataset = load_breast_cancer(as_frame=True)
    df: pd.DataFrame = dataset.data.copy()

    config: dict[str, dict[str, Any]] = {}

    for original_name in df.columns:
        internal_name = FEATURE_NAME_MAP[original_name]

        series = df[original_name].astype(float)

        min_value = float(series.min())
        max_value = float(series.max())
        median_value = float(series.median())
        q1_value = float(series.quantile(0.25))
        q3_value = float(series.quantile(0.75))

        step_value = _suggest_step(min_value, max_value)

        config[internal_name] = {
            "label": original_name.title(),
            "min": min_value,
            "max": max_value,
            "default": median_value,
            "q1": q1_value,
            "q3": q3_value,
            "step": step_value,
        }

    return config


FEATURE_INPUT_CONFIG = build_feature_input_config()