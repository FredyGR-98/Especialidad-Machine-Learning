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
from utils.theme import APP_THEME


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
            page_icon="BC",
            layout="wide",
            initial_sidebar_state="expanded",
        )

    def inject_global_styles(self) -> None:
        """
        Inyecta estilos globales base de la aplicación.
        """
        css_variables = f"""
        :root {{
            --color-primary: {APP_THEME["primary"]};
            --color-primary-soft: {APP_THEME["primary_soft"]};
            --color-primary-dark: {APP_THEME["primary_dark"]};
            --color-surface: {APP_THEME["surface"]};
            --color-surface-soft: {APP_THEME["surface_soft"]};
            --color-surface-alt: {APP_THEME["surface_alt"]};
            --color-background: {APP_THEME["background"]};
            --color-background-start: {APP_THEME["background_gradient_start"]};
            --color-background-end: {APP_THEME["background_gradient_end"]};
            --color-border: {APP_THEME["border"]};
            --color-border-soft: {APP_THEME["border_soft"]};
            --color-text: {APP_THEME["text"]};
            --color-text-muted: {APP_THEME["text_muted"]};
            --color-text-soft: {APP_THEME["text_soft"]};
            --shadow-primary: {APP_THEME["shadow"]};
            --shadow-soft: {APP_THEME["shadow_soft"]};
        }}
        """

        css_rules = """
            /* =========================
               FONDO GENERAL
            ========================= */
            .stApp {
                background: var(--color-background);
            }

            /* =========================
               SIDEBAR GENERAL
            ========================= */
            section[data-testid="stSidebar"] {
                background: linear-gradient(
                    180deg,
                    var(--color-background-start) 0%,
                    var(--color-background-end) 100%
                );
                border-right: 1px solid var(--color-border);
            }

            section[data-testid="stSidebar"] > div {
                padding-top: 0.6rem;
            }

            /* Texto general sidebar */
            section[data-testid="stSidebar"] * {
                color: var(--color-text);
            }

            /* Radio labels */
            section[data-testid="stSidebar"] div[role="radiogroup"] label {
                border-radius: 14px;
                padding: 0.2rem 0.35rem;
            }

            /* Botones sidebar */
            section[data-testid="stSidebar"] button {
                border-radius: 14px !important;
                border: 1px solid var(--color-border) !important;
                background: var(--color-surface) !important;
                color: var(--color-primary) !important;
                font-weight: 700 !important;
            }

            section[data-testid="stSidebar"] button:hover {
                border-color: var(--color-primary-soft) !important;
                color: var(--color-primary-soft) !important;
            }

            /* Línea divisoria */
            section[data-testid="stSidebar"] hr {
                border-color: var(--color-border) !important;
            }

            /* =========================
               HEADER PERSONALIZADO SIDEBAR
            ========================= */
            .sidebar-brand {
                position: relative;
                background:
                    radial-gradient(circle at top left, rgba(231, 84, 128, 0.18), transparent 34%),
                    rgba(255, 255, 255, 0.78);
                border: 1px solid var(--color-border);
                border-radius: 24px;
                padding: 16px 15px 15px 15px;
                margin-bottom: 0.9rem;
                box-shadow: 0 10px 22px var(--shadow-primary);
            }

            .sidebar-brand-title {
                color: var(--color-primary);
                font-size: 1.18rem;
                font-weight: 800;
                line-height: 1.2;
                margin-bottom: 0.28rem;
            }

            .sidebar-brand-subtitle {
                color: var(--color-text-muted);
                font-size: 0.84rem;
                line-height: 1.45;
            }

            .sidebar-brand-kicker {
                color: var(--color-primary);
                font-size: 0.76rem;
                font-weight: 800;
                letter-spacing: 0.16em;
                text-transform: uppercase;
                margin-bottom: 0.45rem;
            }
        """

        st.markdown(
            "<style>" + css_variables + css_rules + "</style>",
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
                    <div class="sidebar-brand-kicker">
                        Plataforma
                    </div>
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
