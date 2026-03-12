"""
===========================================================
home_view.py
===========================================================

Vista de inicio del frontend.

Responsabilidades:
- Presentar la plataforma al usuario autenticado.
- Explicar el objetivo general del sistema.
- Informar el carácter educativo del proyecto.
- Resumir el dataset utilizado en el modelo.
- Resumir la utilidad de la nueva base de datos clínica.
- Mostrar las capacidades principales de la plataforma.

Esta vista cumple un rol informativo e institucional dentro
del flujo del frontend.
===========================================================
"""

import streamlit as st


class HomeView:
    """
    Renderiza la pantalla de inicio de la plataforma.

    Attributes:
        api_client: Cliente base para comunicación con la API.
    """

    def __init__(self, api_client) -> None:
        """
        Inicializa la vista de inicio.

        Args:
            api_client: Cliente base para comunicación con la API.
        """
        self.api_client = api_client

    def render(self) -> None:
        """
        Renderiza el contenido principal de la vista de inicio.
        """
        self._inject_styles()
        self._render_header()
        self._render_intro()
        self._render_system_capabilities()
        self._render_data_summary()
        self._render_footer_note()

    def _inject_styles(self) -> None:
        """
        Inyecta estilos locales de la vista Home.
        """
        st.markdown(
            """
            <style>
            .home-hero {
                background: linear-gradient(135deg, #fde7f0 0%, #fceff5 100%);
                border: 1px solid #f6bfd3;
                border-radius: 28px;
                padding: 34px 36px;
                margin-bottom: 1.5rem;
                box-shadow: 0 12px 28px rgba(231, 84, 128, 0.08);
            }

            .home-hero h1 {
                color: #c2185b;
                font-size: 2.55rem;
                font-weight: 800;
                margin: 0 0 0.65rem 0;
                line-height: 1.15;
            }

            .home-hero h3 {
                color: #6b5562;
                font-size: 1.2rem;
                font-weight: 600;
                margin: 0 0 1rem 0;
            }

            .home-hero p {
                color: #5d4c57;
                font-size: 1rem;
                line-height: 1.75;
                margin: 0;
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
                border: 1px solid #f7bfd2;
                border-radius: 999px;
                padding: 0.38rem 0.9rem;
                font-size: 0.85rem;
                font-weight: 600;
            }

            .section-block {
                background: #ffffff;
                border: 1px solid #f3c9d9;
                border-radius: 24px;
                padding: 24px 26px;
                margin-bottom: 1.25rem;
                box-shadow: 0 10px 26px rgba(231, 84, 128, 0.06);
            }

            .section-title {
                color: #c2185b;
                font-size: 1.65rem;
                font-weight: 800;
                margin-bottom: 0.45rem;
            }

            .section-subtitle {
                color: #6d5863;
                font-size: 0.98rem;
                line-height: 1.65;
                margin-bottom: 0.3rem;
            }

            .soft-alert {
                background: #fff4f8;
                border-left: 5px solid #e75480;
                border-radius: 16px;
                padding: 16px 18px;
                color: #5d4c57;
                line-height: 1.65;
                margin-top: 1rem;
            }

            .capability-card {
                background: #ffffff;
                border: 1px solid #f3c9d9;
                border-radius: 22px;
                padding: 20px 20px;
                min-height: 180px;
                box-shadow: 0 8px 20px rgba(231, 84, 128, 0.05);
                margin-bottom: 1rem;
            }

            .capability-card h4 {
                color: #c2185b;
                font-size: 1.08rem;
                font-weight: 700;
                margin-bottom: 0.75rem;
            }

            .capability-card p {
                color: #5d4c57;
                font-size: 0.98rem;
                line-height: 1.7;
                margin: 0;
            }

            .data-card {
                background: #fff9fc;
                border: 1px solid #f4d4e1;
                border-radius: 20px;
                padding: 20px 22px;
                min-height: 235px;
                box-shadow: 0 7px 18px rgba(231, 84, 128, 0.05);
            }

            .data-card h4 {
                color: #c2185b;
                font-size: 1.08rem;
                font-weight: 700;
                margin-bottom: 0.85rem;
            }

            .data-card p {
                color: #5d4c57;
                font-size: 0.97rem;
                line-height: 1.7;
                margin-bottom: 0.9rem;
            }

            .footer-note {
                background: #fff4f8;
                border: 1px solid #f5cfdd;
                border-radius: 18px;
                padding: 14px 18px;
                color: #6e5b66;
                font-size: 0.95rem;
                line-height: 1.65;
                margin-top: 0.5rem;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )

    def _render_header(self) -> None:
        """
        Renderiza el encabezado principal del sistema.
        """
        st.markdown(
            """
            <div class="home-hero">
                <h1>Breast Cancer Clinical Data Analysis Platform</h1>
                <h3>Análisis clínico, predicción y seguimiento en una sola interfaz</h3>
                <p>
                    Plataforma educativa orientada al análisis de variables clínicas asociadas
                    a tumores mamarios mediante Machine Learning, incorporando además registro
                    de pacientes, evaluaciones y visualización de resultados acumulados.
                </p>
                <div class="badge-row">
                    <span class="soft-badge">Machine Learning</span>
                    <span class="soft-badge">Registro clínico</span>
                    <span class="soft-badge">Dashboard</span>
                    <span class="soft-badge">Base de datos SQLite</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    def _render_intro(self) -> None:
        """
        Renderiza la introducción general de la plataforma.
        """
        st.markdown(
            """
            <div class="section-block">
                <div class="section-title">Propósito de la plataforma</div>
                <div class="section-subtitle">
                    Esta solución integra una capa analítica y una capa operativa dentro
                    de una misma interfaz, permitiendo comprender el comportamiento del modelo
                    y, al mismo tiempo, simular el uso de un entorno clínico con pacientes,
                    evaluaciones y resultados históricos.
                </div>
                <div class="soft-alert">
                    <strong>Uso educativo:</strong> esta plataforma no reemplaza evaluación
                    médica ni diagnóstico profesional. Su objetivo es demostrar integración
                    entre análisis de datos clínicos, API, frontend interactivo y persistencia
                    de información.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    def _render_system_capabilities(self) -> None:
        """
        Renderiza las capacidades principales del sistema mediante tarjetas.
        """
        st.markdown(
            """
            <div class="section-block">
                <div class="section-title">¿Qué permite el sistema?</div>
                <div class="section-subtitle">
                    La plataforma organiza sus funcionalidades en módulos que apoyan tanto
                    el análisis técnico del modelo como el seguimiento de información clínica simulada.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        col1, col2 = st.columns(2)

        with col1:
            st.markdown(
                """
                <div class="capability-card">
                    <h4>Analizar variables clínicas</h4>
                    <p>
                        Explorar métricas del modelo, relaciones entre variables y artefactos
                        visuales derivados del entrenamiento para comprender el comportamiento
                        del clasificador.
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.markdown(
                """
                <div class="capability-card">
                    <h4>Registrar evaluaciones clínicas</h4>
                    <p>
                        Guardar pacientes, mediciones y resultados de evaluación dentro
                        de la base de datos conectada al sistema, permitiendo construir
                        un historial operativo consultable.
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with col2:
            st.markdown(
                """
                <div class="capability-card">
                    <h4>Estimar probabilidad diagnóstica</h4>
                    <p>
                        Ejecutar predicciones a partir de variables clínicas ingresadas
                        en una evaluación, obteniendo una clase estimada y un nivel
                        de confianza asociado al modelo entrenado.
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.markdown(
                """
                <div class="capability-card">
                    <h4>Visualizar estadísticas acumuladas</h4>
                    <p>
                        Consultar información registrada en el sistema y analizarla
                        mediante el dashboard clínico, apoyando una lectura más ejecutiva
                        de los datos almacenados.
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    def _render_data_summary(self) -> None:
        """
        Renderiza el resumen del dataset original y de la base de datos operativa.
        """
        st.markdown(
            """
            <div class="section-block">
                <div class="section-title">Fuentes de datos utilizadas</div>
                <div class="section-subtitle">
                    La solución combina un dataset de entrenamiento para el modelo predictivo
                    y una base de datos operativa para persistir el uso clínico simulado.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        col1, col2 = st.columns(2)

        with col1:
            st.markdown(
                """
                <div class="data-card">
                    <h4>Dataset del modelo</h4>
                    <p>
                        El modelo fue entrenado con un dataset clínico orientado al análisis
                        de características de tumores mamarios, considerando variables
                        numéricas derivadas de estudios médicos para clasificar casos
                        en categorías diagnósticas.
                    </p>
                    <p>
                        Este conjunto de datos permite estudiar patrones, correlaciones
                        entre variables y desempeño predictivo del algoritmo utilizado.
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with col2:
            st.markdown(
                """
                <div class="data-card">
                    <h4>Base de datos clínica del sistema</h4>
                    <p>
                        Además del dataset de entrenamiento, la plataforma incorpora
                        una base de datos SQLite para registrar la operación clínica simulada
                        dentro del sistema.
                    </p>
                    <p>
                        En esta base se almacenan pacientes registrados, evaluaciones clínicas,
                        resultados de predicción y antecedentes que posteriormente alimentan
                        el dashboard clínico.
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    def _render_footer_note(self) -> None:
        """
        Renderiza una nota final de contexto para el usuario.
        """
        st.markdown(
            """
            <div class="footer-note">
                Proyecto educativo orientado a análisis de datos clínicos, integración con API,
                entrenamiento de modelo, persistencia en base de datos y visualización de resultados.
            </div>
            """,
            unsafe_allow_html=True,
        )