"""
===========================================================
sidebar_nav.py
===========================================================

Componente de navegación lateral del frontend.

Responsabilidades:
- Mostrar las páginas principales del sistema.
- Permitir cambiar la página activa.
- Mostrar información básica del usuario autenticado.
- Permitir cierre de sesión.

Este componente se renderiza únicamente cuando existe una
sesión autenticada.
===========================================================
"""

import streamlit as st

from core.session_manager import SessionManager


class SidebarNav:
    """
    Componente de navegación lateral principal.
    """

    PAGES = [
        "Inicio",
        "Análisis del Modelo",
        "Dashboard Clínico",
        "Pacientes",
    ]

    PAGE_META = {
        "Inicio": {
            "eyebrow": "Resumen",
            "description": "Panorama general del caso y alcance analítico.",
        },
        "Análisis del Modelo": {
            "eyebrow": "Modelo",
            "description": "Métricas, hallazgos y lectura del entrenamiento.",
        },
        "Dashboard Clínico": {
            "eyebrow": "Exploración",
            "description": "Comparación visual y acceso al dashboard interactivo.",
        },
        "Pacientes": {
            "eyebrow": "Operación",
            "description": "Gestión de casos, pruebas nuevas e historial clínico.",
        },
    }

    def render(self) -> None:
        """
        Renderiza la barra lateral de navegación.

        Incluye:
        - información del usuario autenticado
        - selector de página
        - botón de cierre de sesión
        """
        self._inject_styles()

        with st.sidebar:
            user = st.session_state.get("user", {})
            username = user.get("username", "Usuario")
            current_page = SessionManager.get_current_page()
            current_page_meta = self.PAGE_META.get(current_page, {})

            st.markdown(
                f"""
                <div class="sidebar-session-card sidebar-session-card-primary">
                    <div class="sidebar-card-kicker">Workspace</div>
                    <div class="sidebar-session-user">Navegación clínica</div>
                    <div class="sidebar-session-text">
                        Acceso directo a vistas analíticas, operación de pacientes y resultados del proyecto.
                    </div>
                    <div class="sidebar-user-pill">Sesión: {username}</div>
                </div>
                <div class="sidebar-nav-shell">
                    <div class="sidebar-card-kicker">App</div>
                    <div class="sidebar-shell-title">Módulos disponibles</div>
                    <div class="sidebar-page-meta">{current_page_meta.get("description", "")}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            current_index = self._get_current_page_index(current_page)

            selected_page = st.radio(
                "Navegación principal",
                options=self.PAGES,
                index=current_index,
                key="sidebar_navigation_radio",
                label_visibility="collapsed",
            )

            if selected_page != current_page:
                SessionManager.set_current_page(selected_page)
                st.rerun()

            st.markdown("<div class='sidebar-divider'></div>", unsafe_allow_html=True)

            if st.button("Cerrar sesión", key="sidebar_logout_button"):
                SessionManager.logout()
                st.rerun()

    def _inject_styles(self) -> None:
        """
        Inyecta estilos locales del componente sidebar.
        """
        st.markdown(
            """
            <style>
            .sidebar-session-card {
                background: rgba(255, 255, 255, 0.72);
                border: 1px solid var(--color-border);
                border-radius: 22px;
                padding: 15px 14px;
                margin-bottom: 0.9rem;
                box-shadow: 0 6px 16px var(--shadow-soft);
            }

            .sidebar-session-card-primary {
                background:
                    radial-gradient(circle at top right, rgba(231, 84, 128, 0.16), transparent 42%),
                    rgba(255, 255, 255, 0.82);
                box-shadow: 0 10px 24px var(--shadow-primary);
            }

            .sidebar-section-title {
                color: var(--color-primary);
                font-size: 1.15rem;
                font-weight: 800;
                margin-bottom: 0.45rem;
            }

            .sidebar-card-kicker {
                color: var(--color-primary);
                font-size: 0.8rem;
                font-weight: 800;
                letter-spacing: 0.14em;
                text-transform: uppercase;
                margin-bottom: 0.45rem;
            }

            .sidebar-session-user {
                color: var(--color-text);
                font-size: 1.18rem;
                font-weight: 800;
                line-height: 1.1;
                margin-bottom: 0.42rem;
            }

            .sidebar-session-text {
                color: var(--color-text-muted);
                font-size: 0.88rem;
                line-height: 1.5;
            }

            .sidebar-user-pill {
                display: inline-flex;
                align-items: center;
                margin-top: 0.8rem;
                padding: 0.34rem 0.72rem;
                border-radius: 999px;
                background: rgba(255, 255, 255, 0.85);
                border: 1px solid var(--color-border);
                color: var(--color-primary);
                font-size: 0.82rem;
                font-weight: 700;
            }

            .sidebar-nav-shell {
                margin-bottom: 0.45rem;
            }

            .sidebar-shell-title {
                color: var(--color-text);
                font-size: 1rem;
                font-weight: 700;
                line-height: 1.2;
                margin-bottom: 0.3rem;
            }

            .sidebar-page-meta {
                color: var(--color-text-soft);
                font-size: 0.88rem;
                line-height: 1.45;
                margin-top: 0.15rem;
            }

            .sidebar-divider {
                border-top: 1px solid var(--color-border);
                margin: 0.9rem 0 0.8rem 0;
            }

            section[data-testid="stSidebar"] label[data-testid="stWidgetLabel"] p {
                color: var(--color-text) !important;
                font-weight: 700 !important;
                font-size: 0.95rem !important;
                letter-spacing: 0.02em;
            }

            section[data-testid="stSidebar"] div[role="radiogroup"] {
                display: flex;
                flex-direction: column;
                gap: 0.28rem;
            }

            section[data-testid="stSidebar"] div[role="radiogroup"] > label {
                background: rgba(255, 255, 255, 0.42);
                border: 1px solid transparent;
                border-radius: 16px;
                padding: 0.28rem 0.4rem;
                margin-bottom: 0;
                transition: 0.2s ease;
                box-shadow: 0 6px 14px rgba(231, 84, 128, 0.03);
            }

            section[data-testid="stSidebar"] div[role="radiogroup"] > label:hover {
                border: 1px solid var(--color-border);
                background: rgba(255, 255, 255, 0.82);
                transform: translateX(2px);
            }

            section[data-testid="stSidebar"] div[role="radiogroup"] > label > div:first-child {
                display: none;
            }

            section[data-testid="stSidebar"] div[role="radiogroup"] p {
                color: var(--color-text) !important;
                font-weight: 600 !important;
                font-size: 0.93rem !important;
            }

            section[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) {
                background: linear-gradient(90deg, rgba(231, 84, 128, 0.22), rgba(255, 255, 255, 0.96));
                border: 1px solid var(--color-border);
                box-shadow: 0 8px 18px rgba(231, 84, 128, 0.09);
            }

            section[data-testid="stSidebar"] div[data-testid="stButton"] > button {
                width: 100%;
                border-radius: 16px !important;
                border: 1px solid var(--color-border) !important;
                background: var(--color-surface) !important;
                color: var(--color-primary) !important;
                font-weight: 700 !important;
                padding: 0.78rem 1rem !important;
                box-shadow: 0 6px 14px var(--shadow-soft);
            }

            section[data-testid="stSidebar"] div[data-testid="stButton"] > button:hover {
                border-color: var(--color-primary-soft) !important;
                color: var(--color-primary-soft) !important;
                background: var(--color-surface-soft) !important;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )

    def _get_current_page_index(self, current_page: str) -> int:
        """
        Obtiene el índice de la página actual dentro del menú.

        Args:
            current_page (str): Nombre de la página activa.

        Returns:
            int: Índice correspondiente dentro de la lista PAGES.
        """
        try:
            return self.PAGES.index(current_page)
        except ValueError:
            return 0
