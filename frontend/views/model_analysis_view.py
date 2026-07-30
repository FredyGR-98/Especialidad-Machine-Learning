"""
Vista de análisis del modelo.

Presenta una narrativa ejecutiva del caso, resume el dataset
y explica de forma guiada las métricas y visualizaciones.
"""

import streamlit as st

from services.analytics_service import AnalyticsService
from utils.theme import VISUALIZATION_FILES as VISUALIZATION_TITLES


class ModelAnalysisView:
    """
    Renderiza la sección de análisis del modelo.
    """

    VISUALIZATION_FILES = list(VISUALIZATION_TITLES.keys())

    def __init__(self, api_client) -> None:
        self.analytics_service = AnalyticsService(api_client)

    def render(self) -> None:
        self._inject_styles()
        self._render_header()

        try:
            model_info = self.analytics_service.get_model_info()
        except RuntimeError as exc:
            st.error(f"No fue posible cargar la información del modelo: {exc}")
            return

        if not isinstance(model_info, dict):
            st.error("La API devolvió una respuesta inválida para la información del modelo.")
            return

        self._render_metrics(model_info)
        self._render_dataset_summary(model_info)
        self._render_variable_table()
        self._render_visualizations()

    def _inject_styles(self) -> None:
        st.markdown(
            """
            <style>
            .model-hero {
                background: linear-gradient(
                    135deg,
                    var(--color-surface-soft) 0%,
                    var(--color-background-start) 100%
                );
                border: 1px solid var(--color-border);
                border-radius: 28px;
                padding: 30px 32px;
                margin-bottom: 1.35rem;
                box-shadow: 0 12px 28px var(--shadow-primary);
            }

            .model-hero h1 {
                color: var(--color-primary);
                font-size: 2.55rem;
                font-weight: 900;
                margin: 0 0 0.7rem 0;
                line-height: 1.08;
            }

            .model-hero p {
                color: var(--color-text);
                margin: 0;
                line-height: 1.72;
                font-size: 1rem;
                max-width: 980px;
            }

            .badge-row {
                margin-top: 1rem;
                display: flex;
                flex-wrap: wrap;
                gap: 0.55rem;
            }

            .soft-badge {
                display: inline-block;
                background: var(--color-surface);
                color: var(--color-primary);
                border: 1px solid var(--color-border);
                border-radius: 999px;
                padding: 0.36rem 0.88rem;
                font-size: 0.85rem;
                font-weight: 700;
            }

            .section-block {
                background: var(--color-surface);
                border: 1px solid var(--color-border-soft);
                border-radius: 24px;
                padding: 22px 24px;
                margin-bottom: 1.2rem;
                box-shadow: 0 8px 22px var(--shadow-soft);
            }

            .section-kicker {
                color: var(--color-primary);
                font-size: 0.74rem;
                font-weight: 750;
                letter-spacing: 0.16em;
                text-transform: uppercase;
                margin-bottom: 0.35rem;
                opacity: 0.9;
            }

            .section-title {
                color: var(--color-primary);
                font-size: 1.65rem;
                font-weight: 850;
                margin-bottom: 0.45rem;
            }

            .section-text {
                color: var(--color-text-muted);
                font-size: 0.98rem;
                line-height: 1.68;
            }

            .metric-card {
                background: linear-gradient(
                    180deg,
                    var(--color-surface) 0%,
                    var(--color-surface-soft) 100%
                );
                border: 1px solid var(--color-border-soft);
                border-radius: 22px;
                padding: 20px 18px;
                min-height: 182px;
                box-shadow: 0 8px 20px var(--shadow-soft);
            }

            .metric-label {
                color: var(--color-text-soft);
                font-size: 0.82rem;
                font-weight: 700;
                text-transform: uppercase;
                letter-spacing: 0.08em;
                margin-bottom: 0.45rem;
            }

            .metric-value {
                color: var(--color-primary);
                font-size: 2rem;
                font-weight: 900;
                line-height: 1.05;
                margin-bottom: 0.7rem;
            }

            .metric-copy {
                color: var(--color-text);
                font-size: 0.95rem;
                line-height: 1.65;
            }

            .info-card {
                background: linear-gradient(
                    180deg,
                    var(--color-surface) 0%,
                    var(--color-surface-soft) 100%
                );
                border: 1px solid var(--color-border-soft);
                border-radius: 22px;
                padding: 22px 20px;
                min-height: 208px;
                box-shadow: 0 8px 20px var(--shadow-soft);
                margin-bottom: 1rem;
            }

            .info-card-title {
                color: var(--color-text);
                font-size: 0.84rem;
                font-weight: 800;
                text-transform: uppercase;
                letter-spacing: 0.08em;
                margin-bottom: 0.7rem;
            }

            .info-card-value {
                color: var(--color-primary);
                font-size: 1.9rem;
                font-weight: 900;
                line-height: 1.18;
                margin-bottom: 0.7rem;
            }

            .info-card-value.is-long {
                font-size: 1.2rem;
                line-height: 1.48;
            }

            .info-card-note {
                color: var(--color-text);
                font-size: 0.94rem;
                line-height: 1.68;
            }

            .insight-box {
                background: var(--color-surface-alt);
                border-left: 5px solid var(--color-primary-soft);
                border-radius: 16px;
                padding: 15px 17px;
                color: var(--color-text);
                line-height: 1.7;
                margin-top: 1rem;
            }

            .table-shell {
                background: var(--color-surface);
                border: 1px solid var(--color-border-soft);
                border-radius: 22px;
                overflow: hidden;
                box-shadow: 0 8px 20px var(--shadow-soft);
                margin: 1rem 0 1.9rem 0;
            }

            .variables-table {
                width: 100%;
                border-collapse: collapse;
                table-layout: fixed;
            }

            .variables-table thead th {
                background: linear-gradient(
                    180deg,
                    var(--color-primary) 0%,
                    var(--color-primary-soft) 100%
                );
                color: white;
                text-align: left;
                padding: 14px 16px;
                font-size: 0.9rem;
                font-weight: 800;
                letter-spacing: 0.03em;
            }

            .variables-table tbody td {
                background: var(--color-surface-soft);
                color: var(--color-text);
                padding: 14px 16px;
                font-size: 0.93rem;
                line-height: 1.6;
                vertical-align: top;
                border-top: 1px solid var(--color-border-soft);
                word-wrap: break-word;
                overflow-wrap: break-word;
            }

            .variables-table tbody tr:nth-child(even) td {
                background: var(--color-surface-alt);
            }

            .variables-table .col-group {
                width: 21%;
                font-weight: 700;
            }

            .variables-table .col-vars {
                width: 27%;
                color: var(--color-primary);
                font-weight: 700;
            }

            .variables-table .col-reading {
                width: 52%;
            }

            .viz-help {
                position: relative;
                display: inline-flex;
                align-items: center;
                gap: 0.45rem;
                margin: 0.8rem 0 1.35rem 0;
            }

            .viz-help-chip {
                display: inline-flex;
                align-items: center;
                gap: 0.35rem;
                background: var(--color-surface);
                color: var(--color-primary);
                border: 1px solid var(--color-border);
                border-radius: 999px;
                padding: 0.42rem 0.85rem;
                font-size: 0.84rem;
                font-weight: 700;
                cursor: default;
                box-shadow: 0 6px 16px var(--shadow-soft);
            }

            .viz-help-tooltip {
                position: absolute;
                left: 0;
                top: calc(100% + 0.55rem);
                width: min(420px, 82vw);
                background: var(--color-surface-soft);
                border: 1px solid var(--color-border-soft);
                border-radius: 16px;
                padding: 14px 15px;
                color: var(--color-text);
                font-size: 0.93rem;
                line-height: 1.66;
                box-shadow: 0 10px 24px var(--shadow-soft);
                opacity: 0;
                visibility: hidden;
                transform: translateY(-4px);
                transition: opacity 0.18s ease, transform 0.18s ease, visibility 0.18s ease;
                z-index: 20;
            }

            .viz-help:hover .viz-help-tooltip {
                opacity: 1;
                visibility: visible;
                transform: translateY(0);
            }
            </style>
            """,
            unsafe_allow_html=True,
        )

    def _render_header(self) -> None:
        st.markdown(
            """
            <div class="model-hero">
                <h1>Análisis del Modelo</h1>
                <p>
                    Para abordar este caso se utilizó un modelo de clasificación supervisada
                    basado en Random Forest, con el objetivo de estimar si un caso presenta
                    un comportamiento más cercano a un diagnóstico benigno o maligno a partir
                    de 30 variables clínicas. Esta vista busca explicar qué tan bien responde
                    el modelo, qué contiene el dataset y cómo interpretar sus resultados de
                    forma simple y útil para el análisis.
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

    def _render_metrics(self, model_info: dict) -> None:
        metrics = model_info.get("metrics", {})

        st.markdown(
            """
            <div class="section-block">
                <div class="section-kicker">Rendimiento</div>
                <div class="section-title">Métricas principales</div>
                <div class="section-text">
                    Estas métricas resumen el comportamiento general del modelo sobre el set de evaluación.
                    No solo muestran qué tan seguido acierta, sino también si mantiene un buen equilibrio
                    al clasificar ambas clases.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        col1, col2, col3 = st.columns(3, gap="large")

        with col1:
            self._metric_card(
                "Accuracy",
                self._format_percentage_metric(metrics.get("accuracy")),
                "Indica la proporción total de predicciones correctas sobre el conjunto evaluado."
            )

        with col2:
            self._metric_card(
                "F1-Score",
                self._format_percentage_metric(metrics.get("f1_score")),
                "Resume el equilibrio entre precisión y recall, útil cuando interesa evitar errores relevantes entre clases."
            )

        with col3:
            self._metric_card(
                "ROC-AUC",
                self._format_decimal_metric(metrics.get("roc_auc")),
                "Mide la capacidad del modelo para separar correctamente casos benignos y malignos a distintos umbrales."
            )

    def _render_dataset_summary(self, model_info: dict) -> None:
        features = model_info.get("features", [])
        targets = model_info.get("targets", [])
        class_labels = model_info.get("class_labels", [])

        dataset_name = "Wisconsin Breast Cancer Diagnostic Dataset"
        model_name = "Random Forest Classifier"
        target_name = "Diagnóstico tumoral"
        num_features = len(features) if isinstance(features, list) else 0
        num_samples = 569
        classes_text = ", ".join(class_labels) if class_labels else ", ".join(targets) if targets else "N/D"
        target_display = " / ".join(class_labels) if class_labels else "Benigno / Maligno"

        st.markdown(
            """
            <div class="section-block">
                <div class="section-kicker">Contexto del entrenamiento</div>
                <div class="section-title">Qué contenía el dataset y cómo se modeló el problema</div>
                <div class="section-text">
                    El caso fue estructurado como un problema de clasificación binaria a partir
                    de mediciones celulares cuantitativas. A continuación se resume el dataset,
                    el algoritmo utilizado y la dimensión general del entrenamiento.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        info_cards = [
            ("Dataset utilizado", dataset_name, "Base diagnóstica utilizada para entrenar y evaluar el modelo."),
            ("Modelo usado", model_name, "Algoritmo basado en ensambles de árboles para clasificación supervisada."),
            ("Variable objetivo", target_name, f"Clasificación final estimada: {target_display}."),
            ("Clasificaciones", classes_text, "Clases finales que el modelo aprende a distinguir."),
            ("Variables", str(num_features), "Cantidad total de atributos numéricos utilizados como entrada."),
            ("Registros", str(num_samples), "Observaciones disponibles en el dataset original de entrenamiento."),
        ]

        first_row = st.columns(3, gap="large")
        second_row = st.columns(3, gap="large")
        rows = [first_row, second_row]

        for index, (title, value, note) in enumerate(info_cards):
            value_class = "info-card-value is-long" if len(str(value)) > 24 else "info-card-value"
            with rows[index // 3][index % 3]:
                st.markdown(
                    f"""
                    <div class="info-card">
                        <div class="info-card-title">{title}</div>
                        <div class="{value_class}">{value}</div>
                        <div class="info-card-note">{note}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        st.markdown(
            """
            <div class="insight-box">
                En términos prácticos, el dataset combina un volumen manejable de observaciones
                con un número suficiente de variables como para construir una primera solución
                predictiva interpretable y útil dentro de un flujo aplicado de análisis clínico.
            </div>
            """,
            unsafe_allow_html=True,
        )

    def _render_variable_table(self) -> None:
        st.markdown("### Cómo se agrupan las variables analizadas")
        st.markdown(
            """
            <div class="section-text" style="margin-bottom: 0.6rem;">
                Las variables del dataset pueden resumirse en grupos morfológicos que describen
                tamaño, forma y textura del tumor. Cada grupo se observa en medidas promedio,
                error estándar y peor valor observado.
            </div>
            """,
            unsafe_allow_html=True,
        )

        table_html = """
        <div class="table-shell">
            <table class="variables-table">
                <thead>
                    <tr>
                        <th>Grupo</th>
                        <th>Variables</th>
                        <th>Lectura analítica</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td class="col-group">Tamaño y geometría</td>
                        <td class="col-vars">radius, perimeter, area</td>
                        <td class="col-reading">Describen dimensiones generales del tumor y suelen concentrar señales relevantes de separación.</td>
                    </tr>
                    <tr>
                        <td class="col-group">Textura y superficie</td>
                        <td class="col-vars">texture, smoothness</td>
                        <td class="col-reading">Aportan información sobre irregularidad superficial y comportamiento estructural.</td>
                    </tr>
                    <tr>
                        <td class="col-group">Forma e irregularidad</td>
                        <td class="col-vars">compactness, concavity, concave points, symmetry</td>
                        <td class="col-reading">Capturan cambios de forma y patrones asociados a masas más complejas o agresivas.</td>
                    </tr>
                    <tr>
                        <td class="col-group">Complejidad morfológica</td>
                        <td class="col-vars">fractal dimension</td>
                        <td class="col-reading">Resume patrones finos de borde y complejidad geométrica de la lesión.</td>
                    </tr>
                    <tr>
                        <td class="col-group">Tipos de medición</td>
                        <td class="col-vars">mean, error, worst</td>
                        <td class="col-reading">Permiten observar tanto el valor central como la dispersión y los extremos del comportamiento medido.</td>
                    </tr>
                </tbody>
            </table>
        </div>
        """

        st.markdown(table_html, unsafe_allow_html=True)

    def _render_visualizations(self) -> None:
        st.markdown(
            """
            <div class="section-block">
                <div class="section-kicker">Interpretación visual</div>
                <div class="section-title">Cómo leer las visualizaciones del modelo</div>
                <div class="section-text">
                    Las siguientes gráficas permiten pasar de una métrica global a una lectura
                    más específica de errores, separación entre clases, relación entre variables
                    y peso relativo de los atributos usados por el modelo.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        captions = {
            "confusion_matrix.png": (
                "La matriz de confusión muestra cómo se distribuyen los aciertos y errores del modelo. "
                "Los falsos positivos representan casos clasificados como malignos cuando en realidad no lo son, "
                "mientras que los falsos negativos representan casos que deberían recibir más atención porque el "
                "modelo los clasificó como benignos cuando pertenecían a la clase contraria."
            ),
            "roc_curve.png": (
                "La curva ROC resume la capacidad del modelo para separar ambas clases a distintos umbrales. "
                "Mientras más cerca esté la curva del extremo superior izquierdo y más alto sea el AUC, mejor es "
                "la capacidad discriminativa del modelo para diferenciar casos benignos y malignos."
            ),
            "feature_importance.png": (
                "Esta visualización destaca qué variables tienen mayor peso relativo en la decisión del modelo. "
                "Un hallazgo esperable en este caso es que mediciones asociadas al tamaño, perímetro y concavidad "
                "tengan una influencia importante en la clasificación final."
            ),
            "correlation_matrix.png": (
                "La matriz de correlación permite identificar relaciones directas entre variables. En este dataset, "
                "atributos como radio, perímetro y área suelen moverse en la misma dirección, por lo que cambios en "
                "estas mediciones tienden a reflejarse conjuntamente en el comportamiento del caso analizado."
            ),
        }

        col1, col2 = st.columns(2, gap="large")
        cols = [col1, col2]

        for index, filename in enumerate(self.VISUALIZATION_FILES):
            image_url = self.analytics_service.get_visualization_url(filename)
            viz_title = VISUALIZATION_TITLES.get(filename, filename)
            caption = captions.get(filename, "")
            with cols[index % 2]:
                st.markdown(f"##### {viz_title}")
                st.image(image_url, use_column_width=True)
                st.markdown(
                    f"""
                    <div class="viz-help">
                        <div class="viz-help-chip">Ver explicación</div>
                        <div class="viz-help-tooltip">{caption}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    @staticmethod
    def _metric_card(label: str, value: str, description: str) -> None:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">{label}</div>
                <div class="metric-value">{value}</div>
                <div class="metric-copy">{description}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

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
