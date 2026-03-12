"""
===========================================================
api_client.py
===========================================================

Cliente base para consumir la API Flask del proyecto.

Responsabilidades:
- Centralizar la URL base del backend.
- Ejecutar solicitudes GET y POST.
- Unificar manejo de errores.
- Evitar que las vistas trabajen directamente con requests.

Este módulo será utilizado por servicios especializados como:
- auth_service
- analytics_service
- patient_service
- prediction_service
===========================================================
"""

import os
import requests


class ApiClient:
    """
    Cliente HTTP sencillo para consumir endpoints del backend.

    Attributes:
        base_url (str): URL base de la API.
        timeout (int): Tiempo máximo de espera por solicitud.
    """

    def __init__(self, base_url: str | None = None, timeout: int = 10) -> None:
        """
        Inicializa el cliente API.

        Args:
            base_url (str | None): URL base personalizada. Si es None,
                se toma desde la variable de entorno API_URL o se usa
                el valor por defecto local.
            timeout (int): Tiempo máximo de espera por solicitud en segundos.
        """
        self.base_url = base_url or os.getenv("API_URL", "http://localhost:5000")
        self.timeout = timeout

    def _build_url(self, endpoint: str) -> str:
        """
        Construye la URL completa a partir de un endpoint relativo.

        Args:
            endpoint (str): Ruta del endpoint, por ejemplo '/login'.

        Returns:
            str: URL completa lista para consumir.
        """
        endpoint = endpoint.lstrip("/")
        return f"{self.base_url}/{endpoint}"

    def get(self, endpoint: str, params: dict | None = None) -> dict:
        """
        Ejecuta una solicitud HTTP GET.

        Args:
            endpoint (str): Endpoint relativo.
            params (dict | None): Parámetros query opcionales.

        Returns:
            dict: Respuesta JSON convertida a diccionario.

        Raises:
            RuntimeError: Si ocurre un error en la solicitud.
        """
        url = self._build_url(endpoint)

        try:
            response = requests.get(url, params=params, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as exc:
            raise RuntimeError(f"Error GET {url}: {exc}") from exc

    def post(self, endpoint: str, payload: dict | None = None) -> dict:
        """
        Ejecuta una solicitud HTTP POST.

        Args:
            endpoint (str): Endpoint relativo.
            payload (dict | None): Cuerpo JSON de la solicitud.

        Returns:
            dict: Respuesta JSON convertida a diccionario.

        Raises:
            RuntimeError: Si ocurre un error en la solicitud.
        """
        url = self._build_url(endpoint)

        try:
            response = requests.post(url, json=payload, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as exc:
            raise RuntimeError(f"Error POST {url}: {exc}") from exc

    # =========================================================
    # MÉTODOS ESPECIALIZADOS PARA EL DASHBOARD CLÍNICO
    # =========================================================

    def get_patients(self, search: str | None = None) -> dict:
        """
        Obtiene la lista de pacientes registrados.

        Args:
            search (str | None): Texto opcional para filtrar pacientes.

        Returns:
            dict: Respuesta del endpoint /patients.
        """
        params = {"search": search} if search else None
        return self.get("/patients", params=params)

    def get_patient_measurements(self, patient_id: int) -> dict:
        """
        Obtiene el historial de evaluaciones clínicas de un paciente.

        Args:
            patient_id (int): ID del paciente.

        Returns:
            dict: Respuesta del endpoint /patients/<patient_id>/measurements.
        """
        return self.get(f"/patients/{patient_id}/measurements")