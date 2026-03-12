"""
===========================================================
login_view.py
===========================================================

Vista de login del frontend.

Responsabilidades:
- Renderizar el formulario de acceso.
- Validar credenciales básicas desde la interfaz.
- Ejecutar autenticación usando AuthService.
- Guardar la sesión autenticada mediante SessionManager.
- Mostrar mensajes de error o éxito según corresponda.
===========================================================
"""

import streamlit as st

from core.session_manager import SessionManager
from services.auth_service import AuthService


class LoginView:
    """
    Renderiza la pantalla de acceso de la aplicación.

    Attributes:
        auth_service (AuthService): Servicio encargado del login.
    """

    def __init__(self, auth_service: AuthService) -> None:
        """
        Inicializa la vista de login.

        Args:
            auth_service (AuthService): Servicio de autenticación.
        """
        self.auth_service = auth_service

    def render(self) -> None:
        """
        Renderiza la interfaz del login y procesa el acceso.
        """
        self._inject_styles()

        login_error = st.session_state.get("login_error")

        left_spacer, center_col, right_spacer = st.columns([1, 1.35, 1])

        with center_col:
            st.markdown(
                """
                <div class="login-hero">
                    <h1>Breast Cancer Clinical Analysis Platform</h1>
                    <p class="hero-subtitle">
                        Plataforma educativa que integra análisis clínico,
                        predicción mediante Machine Learning y registro
                        estructurado de evaluaciones médicas.
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.markdown(
                """
                <div class="login-form-card">
                    <h2>Iniciar sesión</h2>
                    <p class="login-description">
                        Ingresa tus credenciales para acceder al análisis del modelo,
                        dashboard clínico y gestión de pacientes.
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )

            if login_error:
                st.error(login_error)

            with st.form("login_form"):
                username = st.text_input(
                    "Usuario",
                    placeholder="Ingresa tu usuario"
                )
                password = st.text_input(
                    "Contraseña",
                    type="password",
                    placeholder="Ingresa tu contraseña"
                )

                submitted = st.form_submit_button("Acceder")

            st.markdown(
                """
                <div class="login-footnote">
                    Plataforma educativa orientada a análisis clínico,
                    predicción y registro estructurado de información.
                </div>
                """,
                unsafe_allow_html=True,
            )

        if submitted:
            self._handle_login(username=username, password=password)

    def _inject_styles(self) -> None:
        """
        Inyecta estilos visuales del login.
        """
        st.markdown(
            """
            <style>
            .stApp {
                background: linear-gradient(180deg, #fde7f0 0%, #fff3f8 100%);
            }

            .login-hero {
                text-align: center;
                margin-top: 4vh;
                margin-bottom: 1.8rem;
                padding: 0 1rem;
            }

            .hero-badge {
                display: inline-block;
                background: #fff4f8;
                color: #c2185b;
                border: 1px solid #f6bfd3;
                border-radius: 999px;
                padding: 0.38rem 0.95rem;
                font-size: 0.82rem;
                font-weight: 700;
                margin-bottom: 1rem;
            }

            .login-hero h1 {
                color: #c2185b;
                font-size: 2.85rem;
                font-weight: 800;
                margin: 0 0 0.7rem 0;
                line-height: 1.12;
            }

            .hero-subtitle {
                color: #6c5863;
                font-size: 1.03rem;
                line-height: 1.7;
                max-width: 640px;
                margin: 0 auto;
            }

            .login-form-card {
                background: rgba(255, 255, 255, 0.96);
                border: 1px solid #f5c5d8;
                border-radius: 28px;
                padding: 28px 30px 18px 30px;
                box-shadow: 0 16px 40px rgba(231, 84, 128, 0.10);
                margin-bottom: 0.8rem;
            }

            .login-form-card h2 {
                color: #c2185b;
                font-size: 1.7rem;
                font-weight: 800;
                margin: 0 0 0.35rem 0;
                line-height: 1.15;
            }

            .login-description {
                color: #6c5863;
                font-size: 0.97rem;
                line-height: 1.65;
                margin-bottom: 0;
            }

            .login-footnote {
                color: #7a6671;
                font-size: 0.93rem;
                line-height: 1.6;
                margin-top: 1rem;
                text-align: center;
                padding-bottom: 0.5rem;
            }

            div[data-testid="stForm"] {
                background: #ffffff;
                border: 1px solid #f4d0dc;
                border-radius: 22px;
                padding: 1.2rem 1rem 1rem 1rem;
                box-shadow: 0 8px 22px rgba(231, 84, 128, 0.06);
            }

            div[data-testid="stTextInput"] label {
                color: #5c4a56 !important;
                font-weight: 600 !important;
            }

            div[data-testid="stTextInput"] input {
                background-color: #fff9fc !important;
                border: 1px solid #efc5d6 !important;
                border-radius: 14px !important;
                color: #4a3b47 !important;
            }

            div[data-testid="stTextInput"] input:focus {
                border: 1px solid #e75480 !important;
                box-shadow: 0 0 0 1px #e75480 !important;
            }

            div[data-testid="stFormSubmitButton"] > button {
                width: 100%;
                border: none !important;
                border-radius: 14px !important;
                background: linear-gradient(90deg, #e75480 0%, #d93d72 100%) !important;
                color: white !important;
                font-weight: 700 !important;
                padding: 0.72rem 1rem !important;
                transition: 0.2s ease-in-out;
                box-shadow: 0 8px 18px rgba(231, 84, 128, 0.18);
            }

            div[data-testid="stFormSubmitButton"] > button:hover {
                filter: brightness(1.03);
                transform: translateY(-1px);
            }

            div[data-testid="stAlert"] {
                border-radius: 16px !important;
            }

            @media (max-width: 900px) {
                .login-hero h1 {
                    font-size: 2.2rem;
                }

                .hero-subtitle {
                    font-size: 0.98rem;
                }

                .login-form-card {
                    padding: 24px 22px 16px 22px;
                }
            }
            </style>
            """,
            unsafe_allow_html=True,
        )

    def _handle_login(self, username: str, password: str) -> None:
        """
        Procesa el intento de autenticación del usuario.

        Args:
            username (str): Nombre de usuario ingresado.
            password (str): Contraseña ingresada.
        """
        username = username.strip()

        if not username or not password:
            SessionManager.set_login_error(
                "Debe ingresar usuario y contraseña."
            )
            st.rerun()

        try:
            response = self.auth_service.login(
                username=username,
                password=password
            )

            if response.get("success"):
                user_info = response.get("user", {})

                user_data = {
                    "user_id": user_info.get("user_id"),
                    "username": user_info.get("username"),
                    "role": user_info.get("role"),
                    "message": response.get("message"),
                }

                SessionManager.login(user_data)

                st.success("Inicio de sesión exitoso.")
                st.rerun()

            error_message = response.get(
                "message",
                "No fue posible iniciar sesión."
            )

            SessionManager.set_login_error(error_message)
            st.rerun()

        except RuntimeError as exc:
            SessionManager.set_login_error(
                f"Error de conexión con la API: {exc}"
            )
            st.rerun()