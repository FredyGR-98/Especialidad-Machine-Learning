"""
===========================================================
patient_service.py
===========================================================

Servicio encargado de consultar información de pacientes y
su historial clínico desde la API del proyecto.

Responsabilidades:
- Buscar/listar pacientes registrados.
- Obtener detalle de un paciente por ID.
- Obtener historial de mediciones de un paciente.

Este módulo desacopla la lógica de consulta respecto de la
vista de pacientes.
===========================================================
"""

from services.api_client import ApiClient


class PatientService:
    """
    Servicio de acceso a información de pacientes.

    Attributes:
        api_client (ApiClient): Cliente base para consumir la API.
    """

    def __init__(self, api_client: ApiClient) -> None:
        """
        Inicializa el servicio de pacientes.

        Args:
            api_client (ApiClient): Cliente HTTP base para la API.
        """
        self.api_client = api_client

    def get_patients(self, search: str | None = None) -> dict:
        """
        Obtiene la lista de pacientes registrados, con búsqueda opcional.

        Args:
            search (str | None): Texto opcional para buscar por nombre o RUT.

        Returns:
            dict: Respuesta JSON de la API.
        """
        params = {}

        if search and search.strip():
            params["search"] = search.strip()

        return self.api_client.get("/patients", params=params if params else None)

    def get_patient_detail(self, patient_id: int) -> dict:
        """
        Obtiene el detalle de un paciente por ID.

        Args:
            patient_id (int): ID del paciente.

        Returns:
            dict: Respuesta JSON de la API.
        """
        return self.api_client.get(f"/patients/{patient_id}")

    def get_patient_measurements(self, patient_id: int) -> dict:
        """
        Obtiene el historial clínico de un paciente por ID.

        Args:
            patient_id (int): ID del paciente.

        Returns:
            dict: Respuesta JSON de la API.
        """
        return self.api_client.get(f"/patients/{patient_id}/measurements")