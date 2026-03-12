"""
===========================================================
auth_service.py
===========================================================

Servicio encargado de la autenticación del frontend.

Responsabilidades:
- Consumir el endpoint de login de la API.
- Validar credenciales mediante el backend.
- Entregar una respuesta uniforme a la vista de login.

Este módulo desacopla la lógica de autenticación respecto
de la interfaz gráfica.
===========================================================
"""

from services.api_client import ApiClient


class AuthService:
    """
    Servicio de autenticación del frontend.

    Attributes:
        api_client (ApiClient): Cliente base para consumir la API.
    """

    def __init__(self, api_client: ApiClient) -> None:
        """
        Inicializa el servicio de autenticación.

        Args:
            api_client (ApiClient): Cliente HTTP base para la API.
        """
        self.api_client = api_client

    def login(self, username: str, password: str) -> dict:
        """
        Intenta autenticar un usuario contra la API.

        Args:
            username (str): Nombre de usuario.
            password (str): Contraseña del usuario.

        Returns:
            dict: Respuesta JSON entregada por la API.

        Raises:
            RuntimeError: Si ocurre un error de conexión o de solicitud.
        """
        payload = {
            "username": username,
            "password": password,
        }

        return self.api_client.post("/login", payload)