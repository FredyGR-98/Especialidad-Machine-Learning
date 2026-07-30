"""
Tema visual centralizado del frontend.

Define la paleta institucional de la aplicación y los nombres
canónicos de las visualizaciones generadas por el backend.
"""

APP_THEME = {
    "primary": "#C2185B",
    "primary_soft": "#E75480",
    "primary_dark": "#880E4F",
    "surface": "#FFFFFF",
    "surface_soft": "#FFF8FB",
    "surface_alt": "#FFF4F8",
    "background": "#FFF6FA",
    "background_gradient_start": "#FFE5EF",
    "background_gradient_end": "#FFD9E8",
    "border": "#F3BFD0",
    "border_soft": "#F4CDDD",
    "text": "#4A3B47",
    "text_muted": "#6D5863",
    "text_soft": "#7A6571",
    "shadow": "rgba(231, 84, 128, 0.06)",
    "shadow_soft": "rgba(231, 84, 128, 0.05)",
    "class_malignant": "#E75480",
    "class_benign": "#F0A6C1",
}

VISUALIZATION_FILES = {
    "confusion_matrix.png": "Matriz de confusión",
    "correlation_matrix.png": "Matriz de correlación",
    "feature_importance.png": "Importancia de variables",
    "roc_curve.png": "Curva ROC",
}
