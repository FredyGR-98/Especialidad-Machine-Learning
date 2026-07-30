"""
Vista de inicio del frontend.

Presenta el caso principal de uso con un enfoque más profesional,
resumido y orientado a análisis aplicado.
"""

import streamlit as st


class HomeView:
    """
    Renderiza la pantalla de inicio de la plataforma.
    """

    def __init__(self, api_client) -> None:
        self.api_client = api_client

    def render(self) -> None:
        self._inject_styles()
        self._render_hero()
        self._render_dataset_context()
        self._render_purpose_section()
        self._render_scope_note()

    def _inject_styles(self) -> None:
        st.markdown(
            """
            <style>
            .home-hero {
                background: linear-gradient(
                    135deg,
                    var(--color-background-start) 0%,
                    var(--color-surface-soft) 100%
                );
                border: 1px solid var(--color-border);
                border-radius: 30px;
                padding: 38px 40px;
                margin-bottom: 1.5rem;
                box-shadow: 0 14px 34px var(--shadow-primary);
            }

            .home-kicker {
                color: var(--color-primary);
                font-size: 0.9rem;
                font-weight: 800;
                letter-spacing: 0.08em;
                text-transform: uppercase;
                margin-bottom: 0.9rem;
            }

            .home-hero h1 {
                color: var(--color-primary);
                font-size: 3rem;
                line-height: 1.06;
                font-weight: 900;
                margin: 0 0 0.9rem 0;
            }

            .home-hero p {
                color: var(--color-text);
                font-size: 1.02rem;
                line-height: 1.75;
                margin: 0;
                max-width: 900px;
            }

            .hero-badges {
                display: flex;
                flex-wrap: wrap;
                gap: 0.55rem;
                margin-top: 1.15rem;
            }

            .hero-badge {
                display: inline-block;
                background: rgba(255, 255, 255, 0.9);
                color: var(--color-primary);
                border: 1px solid var(--color-border);
                border-radius: 999px;
                padding: 0.42rem 0.95rem;
                font-size: 0.85rem;
                font-weight: 700;
            }

            .content-section {
                background: var(--color-surface);
                border: 1px solid var(--color-border-soft);
                border-radius: 24px;
                padding: 24px 26px;
                margin-bottom: 1.25rem;
                box-shadow: 0 10px 24px var(--shadow-soft);
            }

            .section-label {
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
                font-size: 1.8rem;
                font-weight: 850;
                margin-bottom: 0.55rem;
            }

            .section-text {
                color: var(--color-text-muted);
                font-size: 0.99rem;
                line-height: 1.7;
            }

            .detail-card {
                background: var(--color-surface-soft);
                border: 1px solid var(--color-border-soft);
                border-radius: 22px;
                padding: 22px 22px;
                height: 100%;
                box-shadow: 0 8px 18px var(--shadow-soft);
            }

            .detail-card h4 {
                color: var(--color-primary);
                font-size: 1.05rem;
                font-weight: 800;
                margin-bottom: 0.8rem;
            }

            .detail-card p {
                color: var(--color-text);
                font-size: 0.97rem;
                line-height: 1.7;
                margin-bottom: 0.85rem;
            }

            .tag-group {
                display: flex;
                flex-wrap: wrap;
                gap: 0.65rem;
                margin-top: 1rem;
            }

            .tag-item {
                display: inline-flex;
                align-items: center;
                background: var(--color-surface);
                border: 1px solid var(--color-border);
                color: var(--color-primary);
                border-radius: 999px;
                padding: 0.45rem 0.9rem;
                font-size: 0.88rem;
                font-weight: 700;
                line-height: 1.2;
            }

            .purpose-grid {
                display: grid;
                grid-template-columns: repeat(2, minmax(0, 1fr));
                gap: 1rem;
                margin-top: 1rem;
            }

            .purpose-card {
                background: linear-gradient(
                    180deg,
                    var(--color-surface) 0%,
                    var(--color-surface-soft) 100%
                );
                border: 1px solid var(--color-border-soft);
                border-radius: 24px;
                padding: 22px 22px;
                box-shadow: 0 10px 22px var(--shadow-soft);
            }

            .purpose-card h4 {
                color: var(--color-primary);
                font-size: 1.08rem;
                font-weight: 800;
                margin-bottom: 0.75rem;
            }

            .purpose-card p {
                color: var(--color-text);
                font-size: 0.97rem;
                line-height: 1.7;
                margin-bottom: 0.8rem;
            }

            .purpose-card ul {
                color: var(--color-text-muted);
                margin: 0;
                padding-left: 1.1rem;
                line-height: 1.75;
                font-size: 0.95rem;
            }

            .scope-note {
                background: var(--color-surface-alt);
                border: 1px solid var(--color-border-soft);
                border-left: 5px solid var(--color-primary-soft);
                border-radius: 18px;
                padding: 16px 18px;
                color: var(--color-text);
                line-height: 1.7;
            }

            @media (max-width: 900px) {
                .home-hero h1 {
                    font-size: 2.35rem;
                }

                .purpose-grid {
                    grid-template-columns: 1fr;
                }
            }
            </style>
            """,
            unsafe_allow_html=True,
        )

    def _render_hero(self) -> None:
        st.markdown(
            """
            <div class="home-hero">
                <div class="home-kicker">Aplicación Analítica</div>
                <h1>Predictor y Analizador de Casos de Cáncer de Mama</h1>
                <p>
                    Esta aplicación integra clasificación supervisada, registro estructurado
                    de casos y visualización analítica para apoyar la evaluación de tumores
                    mamarios a partir de variables clínicas cuantitativas. El foco del caso
                    es demostrar cómo un modelo predictivo puede convertirse en una solución
                    reproducible, interpretable y utilizable dentro de un flujo de análisis.
                </p>
                <div class="hero-badges">
                    <span class="hero-badge">Clasificación binaria</span>
                    <span class="hero-badge">30 variables clínicas</span>
                    <span class="hero-badge">Flask API</span>
                    <span class="hero-badge">Streamlit UI</span>
                    <span class="hero-badge">Seguimiento de resultados</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    def _render_dataset_context(self) -> None:
        st.markdown(
            """
            <div class="content-section">
                <div class="section-label">Base Analítica</div>
                <div class="section-title">Origen del dataset y variables evaluadas</div>
                <div class="section-text">
                    El modelo fue entrenado con el Wisconsin Breast Cancer Diagnostic Dataset,
                    disponible a través de <code>sklearn.datasets.load_breast_cancer</code>.
                    Este conjunto contiene mediciones numéricas derivadas de imágenes digitalizadas
                    de masas mamarias y permite clasificar cada observación como benigna o maligna.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        col1, col2 = st.columns(2, gap="large")

        with col1:
            st.markdown(
                """
                <div class="detail-card">
                    <h4>Fuente de datos</h4>
                    <p>
                        El caso utiliza un dataset clínico ampliamente usado en problemas de
                        clasificación supervisada. Su valor en este proyecto está en servir como
                        base para construir un flujo completo: entrenamiento, predicción,
                        persistencia y análisis posterior.
                    </p>
                    <div class="tag-group">
                        <span class="tag-item">569 registros</span>
                        <span class="tag-item">30 atributos numéricos</span>
                        <span class="tag-item">2 clases objetivo</span>
                        <span class="tag-item">Caso analítico aplicado</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with col2:
            st.markdown(
                """
                <div class="detail-card">
                    <h4>Variables analizadas</h4>
                    <p>
                        Las variables corresponden a mediciones morfológicas del tumor,
                        organizadas en tres bloques: promedio, error estándar y peor valor
                        observado para cada característica.
                    </p>
                    <div class="tag-group">
                        <span class="tag-item">Radio, textura, perímetro y área</span>
                        <span class="tag-item">Suavidad, compacidad y concavidad</span>
                        <span class="tag-item">Puntos cóncavos, simetría y dimensión fractal</span>
                        <span class="tag-item">Medidas mean, error y worst</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    def _render_purpose_section(self) -> None:
        st.markdown(
            """
            <div class="content-section">
                <div class="section-label">Propósito del caso</div>
                <div class="section-title">¿Cuál es el propósito de esta solución?</div>
                <div class="section-text">
                    La aplicación está diseñada para cubrir dos necesidades complementarias:
                    generar una predicción sobre un caso clínico y, posteriormente, convertir
                    esos resultados en información observable, acumulable y analizable desde
                    una vista separada.
                </div>
                <div class="purpose-grid">
                    <div class="purpose-card">
                        <h4>Predicción de casos</h4>
                        <p>
                            Permite ingresar variables clínicas de un caso, ejecutar una
                            predicción con el modelo entrenado y obtener una clasificación
                            estimada junto con su nivel de confianza.
                        </p>
                        <ul>
                            <li>Ingreso estructurado de variables clínicas</li>
                            <li>Predicción individual basada en el modelo entrenado</li>
                            <li>Registro del caso y del resultado asociado</li>
                        </ul>
                    </div>
                    <div class="purpose-card">
                        <h4>Análisis y seguimiento de resultados</h4>
                        <p>
                            Los casos procesados pueden proyectarse hacia un dashboard y una
                            capa de análisis clínico para observar tendencias, distribuciones,
                            diferencias entre grupos y comportamiento de los registros acumulados.
                        </p>
                        <ul>
                            <li>Visualización de resultados históricos</li>
                            <li>Exploración descriptiva en dashboard separado</li>
                            <li>Apoyo a lectura analítica y seguimiento del flujo</li>
                        </ul>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    def _render_scope_note(self) -> None:
        st.markdown(
            """
            <div class="scope-note">
                Esta implementación se presenta como un caso aplicado de machine learning y MLOps.
                Su objetivo es demostrar diseño de flujo, exposición del modelo, experiencia de uso
                y análisis posterior de resultados. No corresponde a una herramienta clínica validada
                para diagnóstico real.
            </div>
            """,
            unsafe_allow_html=True,
        )
