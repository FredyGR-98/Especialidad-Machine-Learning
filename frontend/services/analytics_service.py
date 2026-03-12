"""
===========================================================
analytics_service.py
===========================================================

Servicio encargado de recuperar información analítica desde
la API del proyecto.

Responsabilidades:
- Obtener metadatos y métricas del modelo.
- Obtener ejemplos si la API los expone.
- Construir URLs de visualizaciones generadas por backend.

Este servicio desacopla la lógica de análisis respecto de las
vistas del frontend.
===========================================================
"""

from services.api_client import ApiClient


class AnalyticsService:
    """
    Servicio de acceso a información analítica del sistema.

    Attributes:
        api_client (ApiClient): Cliente base para consumir la API.
    """

    def __init__(self, api_client: ApiClient) -> None:
        """
        Inicializa el servicio analítico.

        Args:
            api_client (ApiClient): Cliente HTTP base para la API.
        """
        self.api_client = api_client

    def get_model_info(self) -> dict:
        """
        Obtiene información general y métricas del modelo.

        Returns:
            dict: Respuesta JSON con información del modelo.

        Raises:
            RuntimeError: Si ocurre un error de conexión o solicitud.
        """
        return self.api_client.get("/model/info")

    def get_examples(self) -> dict:
        """
        Obtiene ejemplos desde la API, si se encuentran disponibles.

        Returns:
            dict: Respuesta JSON con ejemplos o datos ilustrativos.

        Raises:
            RuntimeError: Si ocurre un error de conexión o solicitud.
        """
        return self.api_client.get("/examples")

    def get_visualization_url(self, filename: str) -> str:
        """
        Construye la URL pública de una visualización expuesta por la API.

        Args:
            filename (str): Nombre del archivo de imagen.

        Returns:
            str: URL completa para consumir la visualización.
        """
        filename = filename.lstrip("/")
        return f"{self.api_client.base_url}/visualizations/{filename}"