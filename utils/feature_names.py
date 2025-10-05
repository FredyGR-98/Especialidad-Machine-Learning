"""
===========================================================
📌 feature_names.py — Diccionario de traducción de features
===========================================================

Este módulo contiene las traducciones de las variables
del dataset Breast Cancer Wisconsin.
Se importa desde train_model.py y frontend.py
para mantener consistencia y evitar duplicación.
"""

FEATURE_TRANSLATIONS = {
    # === Promedios (mean) ===
    "mean radius": "Radio promedio",
    "mean texture": "Textura promedio",
    "mean perimeter": "Perímetro promedio",
    "mean area": "Área promedio",
    "mean smoothness": "Suavidad promedio",
    "mean compactness": "Compacidad promedio",
    "mean concavity": "Concavidad promedio",
    "mean concave points": "Puntos cóncavos promedio",
    "mean symmetry": "Simetría promedio",
    "mean fractal dimension": "Dimensión fractal promedio",

    # === Error estándar (se) ===
    "radius error": "Error en radio",
    "texture error": "Error en textura",
    "perimeter error": "Error en perímetro",
    "area error": "Error en área",
    "smoothness error": "Error en suavidad",
    "compactness error": "Error en compacidad",
    "concavity error": "Error en concavidad",
    "concave points error": "Error en puntos cóncavos",
    "symmetry error": "Error en simetría",
    "fractal dimension error": "Error en dimensión fractal",

    # === Peor valor (worst) ===
    "worst radius": "Radio peor caso",
    "worst texture": "Textura peor caso",
    "worst perimeter": "Perímetro peor caso",
    "worst area": "Área peor caso",
    "worst smoothness": "Suavidad peor caso",
    "worst compactness": "Compacidad peor caso",
    "worst concavity": "Concavidad peor caso",
    "worst concave points": "Puntos cóncavos peor caso",
    "worst symmetry": "Simetría peor caso",
    "worst fractal dimension": "Dimensión fractal peor caso"
}