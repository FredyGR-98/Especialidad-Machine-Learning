"""
===========================================================
model_analysis_view.py
===========================================================

Vista de análisis del modelo de Machine Learning.

Responsabilidades:
- Presentar el objetivo analítico del modelo.
- Mostrar métricas principales de desempeño.
- Mostrar información general del modelo obtenida desde la API.
- Visualizar gráficos generados por backend.

Esta vista cumple un rol explicativo y técnico dentro de la
plataforma, separada del flujo operativo de pacientes.
===========================================================
"""

import streamlit as st

from services.analytics_service import AnalyticsService


class ModelAnalysisView:
    """
    Renderiza la sección de análisis del modelo de Machine Learning.
    """

    VISUALIZATION_FILES = [
        "confusion_matrix_pink.png",
        "correlation_matrix_pink.png",
        "feature_importance_pink.png",
        "roc_curve_pink.png",
    ]

    def __init__(self, api_client) -> None:
        self.analytics_service = AnalyticsService(api_client)

    def render(self) -> None:
        """
        Renderiza el contenido principal de la vista.
        """
        self._inject_styles()
        self._render_header()
        self._render_model_info()
        self._render_visualizations()

    def _inject_styles(self) -> None:
        """
        Inyecta estilos locales de la vista.
        """
        st.markdown(
            """
            <style>
            .pink-hero {
                background: linear-gradient(135deg, #fff7fb 0%, #fdeef4 100%);
                border: 1px solid #f8bbd0;
                border-radius: 24px;
                padding: 28px 30px;
                margin-bottom: 1.5rem;
                box-shadow: 0 10px 28px rgba(194, 24, 91, 0.08);
            }

            .pink-hero h1 {
                color: #c2185b;
                font-size: 2.35rem;
                font-weight: 800;
                margin: 0 0 0.5rem 0;
            }

            .pink-hero p {
                color: #5c4a56;
                margin: 0;
                line-height: 1.7;
                font-size: 1rem;
            }

            .badge-row {
                margin-top: 1rem;
                display: flex;
                flex-wrap: wrap;
                gap: 0.5rem;
            }

            .soft-badge {
                display: inline-block;
                background: #ffffff;
                color: #c2185b;
                border: 1px solid #f8bbd0;
                border-radius: 999px;
                padding: 0.35rem 0.85rem;
                font-size: 0.85rem;
                font-weight: 600;
            }

            .soft-section {
                background: #ffffff;
                border: 1px solid #f4cddd;
                border-radius: 22px;
                padding: 22px 24px;
                margin-bottom: 1.2rem;
                box-shadow: 0 8px 24px rgba(231, 84, 128, 0.06);
            }

            .soft-section-title {
                color: #c2185b;
                font-size: 1.55rem;
                font-weight: 800;
                margin-bottom: 0.35rem;
            }

            .soft-section-subtitle {
                color: #6a5662;
                font-size: 0.98rem;
                line-height: 1.6;
            }

            .info-card {
                background: #fff8fb;
                border: 1px solid #f8d4e1;
                border-radius: 18px;
                padding: 18px 20px;
                min-height: 220px;
                box-shadow: 0 6px 18px rgba(231, 84, 128, 0.05);
            }

            .info-card h4 {
                color: #c2185b;
                font-size: 1.05rem;
                margin-bottom: 0.9rem;
                font-weight: 700;
            }

            .info-item {
                color: #4a3b47;
                margin-bottom: 0.65rem;
                line-height: 1.65;
                font-size: 1rem;
            }

            .highlight-box {
                background: #fff4f8;
                border-left: 5px solid #e75480;
                border-radius: 14px;
                padding: 16px 18px;
                margin-top: 1rem;
                color: #5c4a56;
                line-height: 1.7;
            }

            .viz-title {
                color: #c2185b;
                font-size: 1.05rem;
                font-weight: 700;
                margin-bottom: 0.65rem;
            }

            div[data-testid="stMetric"] {
                background: #ffffff;
                border: 1px solid #f4cddd;
                border-radius: 20px;
                padding: 14px 12px;
                box-shadow: 0 8px 22px rgba(231, 84, 128, 0.05);
            }

            div[data-testid="stMetricLabel"] {
                color: #7a6571 !important;
                font-weight: 600 !important;
            }

            div[data-testid="stMetricValue"] {
                color: #c2185b !important;
                font-weight: 800 !important;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )

    def _render_header(self) -> None:
        st.markdown(
            """
            <div class="pink-hero">
                <h1>Análisis del Modelo</h1>
                <p>
                    Esta sección resume el desempeño del modelo de Machine Learning,
                    su contexto analítico y las principales visualizaciones generadas
                    durante el entrenamiento.
                </p>
                <div class="badge-row">
                    <span class="soft-badge">Random Forest</span>
                    <span class="soft-badge">Clasificación binaria</span>
                    <span class="soft-badge">30 variables clínicas</span>
                    <span class="soft-badge">Dataset diagnóstico mamario</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    def _render_model_info(self) -> None:
        try:
            model_info = self.analytics_service.get_model_info()
        except RuntimeError as exc:
            st.error(f"No fue posible cargar la información del modelo: {exc}")
            return

        if not isinstance(model_info, dict):
            st.error("La API devolvió una respuesta inválida para la información del modelo.")
            return

        st.markdown(
            """
            <div class="soft-section">
                <div class="soft-section-title">Resumen del modelo</div>
                <div class="soft-section-subtitle">
                    A continuación se presentan las métricas principales y una síntesis
                    técnica del modelo entrenado.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        self._render_metrics(model_info)
        self._render_model_details(model_info)

    def _render_metrics(self, model_info: dict) -> None:
        metrics = model_info.get("metrics", {})

        accuracy = metrics.get("accuracy")
        f1_score = metrics.get("f1_score")
        roc_auc = metrics.get("roc_auc")

        st.markdown("#### Métricas principales")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Accuracy", self._format_percentage_metric(accuracy))
        with col2:
            st.metric("F1-Score", self._format_percentage_metric(f1_score))
        with col3:
            st.metric("ROC-AUC", self._format_decimal_metric(roc_auc))

        st.markdown("<br>", unsafe_allow_html=True)

    def _render_model_details(self, model_info: dict) -> None:
        features = model_info.get("features", [])
        targets = model_info.get("targets", [])

        model_name = "Random Forest Classifier"
        dataset_name = "Wisconsin Breast Cancer Diagnostic Dataset"
        target_name = "Diagnóstico (Benigno / Maligno)"
        description = (
            "Modelo de clasificación supervisada entrenado para estimar "
            "la probabilidad de cáncer de mama a partir de variables clínicas "
            "numéricas derivadas de mediciones celulares."
        )

        num_features = len(features) if isinstance(features, list) else 0
        num_samples = 569
        targets_text = ", ".join(targets) if isinstance(targets, list) and targets else "N/D"

        st.markdown(
            """
            <div class="soft-section">
                <div class="soft-section-title">Ficha técnica del modelo</div>
                <div class="soft-section-subtitle">
                    Resumen estructurado del algoritmo, dataset y variables empleadas
                    en el proceso de entrenamiento.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        col1, col2 = st.columns(2)

        with col1:
            st.markdown(
                f"""
                <div class="info-card">
                    <h4>Contexto general</h4>
                    <div class="info-item"><strong>Modelo:</strong> {model_name}</div>
                    <div class="info-item"><strong>Dataset:</strong> {dataset_name}</div>
                    <div class="info-item"><strong>Variable objetivo:</strong> {target_name}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with col2:
            st.markdown(
                f"""
                <div class="info-card">
                    <h4>Dimensión del entrenamiento</h4>
                    <div class="info-item"><strong>Cantidad de variables:</strong> {num_features}</div>
                    <div class="info-item"><strong>Cantidad de registros:</strong> {num_samples}</div>
                    <div class="info-item"><strong>Clases objetivo:</strong> {targets_text}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown(
            f"""
            <div class="highlight-box">
                <strong>Descripción general:</strong><br>
                {description}
            </div>
            """,
            unsafe_allow_html=True,
        )

        if isinstance(features, list) and features:
            with st.expander("Ver variables utilizadas por el modelo"):
                for feature in features:
                    st.write(f"- {feature}")

    def _render_visualizations(self) -> None:
        st.markdown(
            """
            <div class="soft-section">
                <div class="soft-section-title">Visualizaciones analíticas</div>
                <div class="soft-section-subtitle">
                    Estas visualizaciones permiten interpretar el rendimiento del modelo,
                    la relación entre variables clínicas y la importancia relativa de
                    los atributos utilizados durante el entrenamiento.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        titles = {
            "confusion_matrix_pink.png": "Matriz de confusión",
            "correlation_matrix_pink.png": "Matriz de correlación",
            "feature_importance_pink.png": "Importancia de variables",
            "roc_curve_pink.png": "Curva ROC",
        }

        col1, col2 = st.columns(2)
        cols = [col1, col2]

        for index, filename in enumerate(self.VISUALIZATION_FILES):
            image_url = self.analytics_service.get_visualization_url(filename)
            viz_title = titles.get(filename, filename)

            with cols[index % 2]:
                st.markdown(f"##### {viz_title}")
                st.image(image_url, use_column_width=True)
                st.markdown("<br>", unsafe_allow_html=True)

    @staticmethod
    def _format_percentage_metric(value) -> str:
        if value is None:
            return "N/D"

        try:
            return f"{float(value):.2%}"
        except (TypeError, ValueError):
            return str(value)

    @staticmethod
    def _format_decimal_metric(value) -> str:
        if value is None:
            return "N/D"

        try:
            return f"{float(value):.3f}"
        except (TypeError, ValueError):
            return str(value)