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

            st.markdown(
                f"""
                <div class="sidebar-session-card">
                    <div class="sidebar-section-title">Navegación</div>
                    <div class="sidebar-session-text">
                        Sesión activa: <strong>{username}</strong>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            current_page = SessionManager.get_current_page()
            current_index = self._get_current_page_index(current_page)

            selected_page = st.radio(
                "Ir a:",
                options=self.PAGES,
                index=current_index,
                key="sidebar_navigation_radio",
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
                border: 1px solid #f1bfd0;
                border-radius: 20px;
                padding: 16px 14px;
                margin-bottom: 1rem;
                box-shadow: 0 6px 18px rgba(231, 84, 128, 0.05);
            }

            .sidebar-section-title {
                color: #c2185b;
                font-size: 1.15rem;
                font-weight: 800;
                margin-bottom: 0.45rem;
            }

            .sidebar-session-text {
                color: #6c5863;
                font-size: 0.92rem;
                line-height: 1.5;
            }

            .sidebar-divider {
                border-top: 1px solid #efbfd0;
                margin: 1rem 0 0.85rem 0;
            }

            section[data-testid="stSidebar"] label[data-testid="stWidgetLabel"] p {
                color: #5a3f49 !important;
                font-weight: 700 !important;
            }

            section[data-testid="stSidebar"] div[role="radiogroup"] > label {
                background: rgba(255, 255, 255, 0.45);
                border: 1px solid transparent;
                border-radius: 14px;
                padding: 0.35rem 0.4rem;
                margin-bottom: 0.2rem;
                transition: 0.2s ease;
            }

            section[data-testid="stSidebar"] div[role="radiogroup"] > label:hover {
                border: 1px solid #efbfd0;
                background: rgba(255, 255, 255, 0.72);
            }

            section[data-testid="stSidebar"] div[role="radiogroup"] p {
                color: #4a3b47 !important;
                font-weight: 500 !important;
            }

            section[data-testid="stSidebar"] div[data-testid="stButton"] > button {
                width: 100%;
                border-radius: 14px !important;
                border: 1px solid #efbfd0 !important;
                background: #ffffff !important;
                color: #c2185b !important;
                font-weight: 700 !important;
                padding: 0.65rem 1rem !important;
                box-shadow: 0 6px 16px rgba(231, 84, 128, 0.05);
            }

            section[data-testid="stSidebar"] div[data-testid="stButton"] > button:hover {
                border-color: #e75480 !important;
                color: #e75480 !important;
                background: #fff8fb !important;
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