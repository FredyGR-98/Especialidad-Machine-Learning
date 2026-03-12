"""
===========================================================
router.py
===========================================================

Controla la navegación principal del frontend.

Responsabilidades:
- Mostrar la vista de login si no existe sesión autenticada.
- Resolver qué pantalla renderizar según la página activa.
- Mantener desacoplado el flujo general respecto de las vistas.

Este módulo no debe contener lógica visual detallada, solo la
decisión de qué vista corresponde mostrar.
===========================================================
"""

from core.session_manager import SessionManager


class Router:
    """
    Router principal del frontend.

    Attributes:
        views (dict): Diccionario de vistas instanciadas, indexadas
            por una clave interna.
    """

    def __init__(self, views: dict) -> None:
        """
        Inicializa el router con las vistas disponibles.

        Args:
            views (dict): Diccionario con instancias de las vistas.
        """
        self.views = views

    def render(self) -> None:
        """
        Renderiza la vista adecuada según el estado de sesión.

        Flujo:
        - Si el usuario no está autenticado, muestra el login.
        - Si está autenticado, resuelve la página actual y muestra
          la vista correspondiente.
        """
        if not SessionManager.is_authenticated():
            self.views["login"].render()
            return

        current_page = SessionManager.get_current_page()

        page_map = {
            "Inicio": "home",
            "Análisis del Modelo": "model_analysis",
            "Dashboard Clínico": "clinical_dashboard",
            "Pacientes": "patients",
        }

        selected_view_key = page_map.get(current_page, "home")
        selected_view = self.views[selected_view_key]
        selected_view.render()