"""
===========================================================
app.py
===========================================================

Punto de entrada principal del frontend en Streamlit.

Responsabilidades:
- Configurar la página de Streamlit.
- Inicializar el estado global de sesión.
- Instanciar servicios base.
- Registrar las vistas principales.
- Renderizar la navegación lateral cuando exista login.
- Delegar la navegación al router.

Este archivo actúa como orquestador general del frontend.
===========================================================
"""

import streamlit as st

from components.sidebar_nav import SidebarNav
from core.router import Router
from core.session_manager import SessionManager
from services.api_client import ApiClient
from services.auth_service import AuthService


class FrontendApp:
    """
    Clase principal de la aplicación frontend.

    Attributes:
        api_client (ApiClient): Cliente base para comunicación con la API.
        auth_service (AuthService): Servicio de autenticación.
        sidebar_nav (SidebarNav): Componente de navegación lateral.
        views (dict): Diccionario con las vistas instanciadas.
    """

    def __init__(self) -> None:
        """
        Inicializa la aplicación frontend.
        """
        self.api_client = ApiClient()
        self.auth_service = AuthService(self.api_client)
        self.sidebar_nav = SidebarNav()
        self.views = {}

    def configure_page(self) -> None:
        """
        Configura los parámetros base de la página en Streamlit.
        """
        st.set_page_config(
            page_title="Breast Cancer Clinical Data Analysis Platform",
            page_icon="🩺",
            layout="wide",
            initial_sidebar_state="expanded",
        )

    def inject_global_styles(self) -> None:
        """
        Inyecta estilos globales base de la aplicación.
        """
        st.markdown(
            """
            <style>
            /* =========================
               FONDO GENERAL
            ========================= */
            .stApp {
                background: #fff6fa;
            }

            /* =========================
               SIDEBAR GENERAL
            ========================= */
            section[data-testid="stSidebar"] {
                background: linear-gradient(180deg, #ffe5ef 0%, #ffd9e8 100%);
                border-right: 1px solid #f3bfd0;
            }

            section[data-testid="stSidebar"] > div {
                padding-top: 0.6rem;
            }

            /* Texto general sidebar */
            section[data-testid="stSidebar"] * {
                color: #4a3b47;
            }

            /* Radio labels */
            section[data-testid="stSidebar"] div[role="radiogroup"] label {
                border-radius: 14px;
                padding: 0.2rem 0.35rem;
            }

            /* Botones sidebar */
            section[data-testid="stSidebar"] button {
                border-radius: 14px !important;
                border: 1px solid #efbfd0 !important;
                background: #ffffff !important;
                color: #c2185b !important;
                font-weight: 700 !important;
            }

            section[data-testid="stSidebar"] button:hover {
                border-color: #e75480 !important;
                color: #e75480 !important;
            }

            /* Línea divisoria */
            section[data-testid="stSidebar"] hr {
                border-color: #f1bfd0 !important;
            }

            /* =========================
               HEADER PERSONALIZADO SIDEBAR
            ========================= */
            .sidebar-brand {
                background: rgba(255, 255, 255, 0.72);
                border: 1px solid #f3bfd0;
                border-radius: 22px;
                padding: 18px 16px;
                margin-bottom: 1rem;
                box-shadow: 0 8px 20px rgba(231, 84, 128, 0.06);
            }

            .sidebar-brand-title {
                color: #c2185b;
                font-size: 1.25rem;
                font-weight: 800;
                line-height: 1.2;
                margin-bottom: 0.35rem;
            }

            .sidebar-brand-subtitle {
                color: #6d5863;
                font-size: 0.88rem;
                line-height: 1.45;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )

    def initialize(self) -> None:
        """
        Ejecuta la inicialización general de la aplicación.

        Incluye:
        - configuración visual base
        - inicialización de variables de sesión
        """
        self.configure_page()
        self.inject_global_styles()
        SessionManager.initialize()

    def register_views(self) -> None:
        """
        Registra e instancia las vistas principales de la aplicación.
        """
        from views.login_view import LoginView
        from views.home_view import HomeView
        from views.model_analysis_view import ModelAnalysisView
        from views.clinical_dashboard_view import ClinicalDashboardView
        from views.patients_view import PatientsView

        self.views = {
            "login": LoginView(self.auth_service),
            "home": HomeView(self.api_client),
            "model_analysis": ModelAnalysisView(self.api_client),
            "clinical_dashboard": ClinicalDashboardView(self.api_client),
            "patients": PatientsView(self.api_client),
        }

    def render_layout(self) -> None:
        """
        Renderiza componentes globales del layout.

        Actualmente:
        - barra lateral de navegación para usuarios autenticados
        """
        if SessionManager.is_authenticated():
            st.sidebar.markdown(
                """
                <div class="sidebar-brand">
                    <div class="sidebar-brand-title">
                        Breast Cancer Platform
                    </div>
                    <div class="sidebar-brand-subtitle">
                        Análisis clínico y predicción mediante Machine Learning
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            self.sidebar_nav.render()

    def run(self) -> None:
        """
        Ejecuta el flujo principal del frontend.

        Pasos:
        - inicializar aplicación
        - registrar vistas
        - renderizar layout global
        - crear router
        - renderizar la vista correspondiente
        """
        self.initialize()
        self.register_views()
        self.render_layout()

        router = Router(self.views)
        router.render()


if __name__ == "__main__":
    app = FrontendApp()
    app.run()