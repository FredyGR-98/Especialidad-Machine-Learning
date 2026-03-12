"""
===========================================================
session_manager.py
===========================================================

Gestiona el estado global del frontend usando st.session_state.

Responsabilidades:
- Inicializar variables base de sesión.
- Controlar autenticación.
- Guardar la página actual.
- Mantener paciente seleccionado.
- Guardar resultados temporales de evaluación.

Este módulo busca centralizar el acceso al estado para evitar
tener claves dispersas por toda la aplicación.
===========================================================
"""

import streamlit as st


class SessionManager:
    """
    Clase utilitaria para manejar el estado global de la sesión.

    Esta clase opera directamente sobre st.session_state y ofrece
    métodos estáticos para inicializar, consultar y modificar
    variables relevantes del frontend.
    """

    DEFAULT_PAGE = "Inicio"

    @staticmethod
    def initialize() -> None:
        """
        Inicializa las variables de sesión con valores por defecto.

        Si una clave aún no existe en st.session_state, se crea
        con un valor inicial.
        """
        defaults = {
            "authenticated": False,
            "user": None,
            "current_page": SessionManager.DEFAULT_PAGE,
            "selected_patient_id": None,
            "selected_patient_data": None,
            "evaluation_result": None,
            "login_error": None,
        }

        for key, value in defaults.items():
            if key not in st.session_state:
                st.session_state[key] = value

    @staticmethod
    def is_authenticated() -> bool:
        """
        Indica si existe una sesión autenticada.

        Returns:
            bool: True si el usuario inició sesión, False en caso contrario.
        """
        return st.session_state.get("authenticated", False)

    @staticmethod
    def login(user_data: dict) -> None:
        """
        Registra una sesión autenticada en el estado global.

        Args:
            user_data (dict): Información básica del usuario autenticado.
        """
        st.session_state["authenticated"] = True
        st.session_state["user"] = user_data
        st.session_state["login_error"] = None
        st.session_state["current_page"] = SessionManager.DEFAULT_PAGE

    @staticmethod
    def logout() -> None:
        """
        Cierra la sesión actual y limpia el estado asociado.

        Reinicia variables relacionadas con autenticación, navegación,
        paciente seleccionado y resultados de evaluación.
        """
        st.session_state["authenticated"] = False
        st.session_state["user"] = None
        st.session_state["current_page"] = SessionManager.DEFAULT_PAGE
        st.session_state["selected_patient_id"] = None
        st.session_state["selected_patient_data"] = None
        st.session_state["evaluation_result"] = None
        st.session_state["login_error"] = None

    @staticmethod
    def set_current_page(page_name: str) -> None:
        """
        Actualiza la página activa del frontend.

        Args:
            page_name (str): Nombre de la página seleccionada.
        """
        st.session_state["current_page"] = page_name

    @staticmethod
    def get_current_page() -> str:
        """
        Obtiene la página actualmente seleccionada.

        Returns:
            str: Nombre de la página activa.
        """
        return st.session_state.get("current_page", SessionManager.DEFAULT_PAGE)

    @staticmethod
    def set_selected_patient(patient_id=None, patient_data=None) -> None:
        """
        Guarda en sesión el paciente actualmente seleccionado.

        Args:
            patient_id: Identificador del paciente.
            patient_data: Diccionario con información del paciente.
        """
        st.session_state["selected_patient_id"] = patient_id
        st.session_state["selected_patient_data"] = patient_data

    @staticmethod
    def clear_selected_patient() -> None:
        """
        Elimina de la sesión la selección actual de paciente.
        """
        st.session_state["selected_patient_id"] = None
        st.session_state["selected_patient_data"] = None

    @staticmethod
    def set_evaluation_result(result: dict | None) -> None:
        """
        Guarda un resultado temporal de evaluación clínica.

        Args:
            result (dict | None): Resultado de la predicción o evaluación.
        """
        st.session_state["evaluation_result"] = result

    @staticmethod
    def get_evaluation_result():
        """
        Obtiene el resultado temporal almacenado de evaluación.

        Returns:
            dict | None: Resultado guardado o None si no existe.
        """
        return st.session_state.get("evaluation_result")

    @staticmethod
    def set_login_error(message: str | None) -> None:
        """
        Guarda un mensaje de error asociado al login.

        Args:
            message (str | None): Mensaje de error o None para limpiar.
        """
        st.session_state["login_error"] = message