"""
===========================================================
prediction_service.py
===========================================================

Servicio encargado de ejecutar predicción y guardado de una
nueva evaluación clínica mediante la API.

Responsabilidades:
- Construir el payload esperado por /predict.
- Construir el payload esperado por /predict-and-save.
- Ejecutar predicción simple para vista previa.
- Guardar evaluación clínica una vez confirmada por el usuario.
===========================================================
"""

from services.api_client import ApiClient


class PredictionService:
    """
    Servicio de predicción y guardado de evaluaciones clínicas.

    Attributes:
        api_client (ApiClient): Cliente base para consumir la API.
    """

    def __init__(self, api_client: ApiClient) -> None:
        """
        Inicializa el servicio de predicción.

        Args:
            api_client (ApiClient): Cliente HTTP base para la API.
        """
        self.api_client = api_client

    def predict(self, measurement: dict) -> dict:
        """
        Ejecuta una predicción simple sin guardar en la base de datos.

        Args:
            measurement (dict): Variables clínicas en snake_case.

        Returns:
            dict: Respuesta JSON entregada por la API.
        """
        return self.api_client.post("/predict", measurement)

    def predict_and_save(
        self,
        user_id: int,
        patient: dict,
        measurement: dict,
        evaluation_date: str,
    ) -> dict:
        """
        Ejecuta predicción y guarda la evaluación en la base de datos.

        Args:
            user_id (int): ID del usuario autenticado en sesión.
            patient (dict): Datos del paciente.
            measurement (dict): Variables clínicas en snake_case.
            evaluation_date (str): Fecha de evaluación en formato YYYY-MM-DD.

        Returns:
            dict: Respuesta JSON entregada por la API.
        """
        payload = {
            "user_id": user_id,
            "patient": patient,
            "measurement": measurement,
            "evaluation_date": evaluation_date,
        }

        return self.api_client.post("/predict-and-save", payload)