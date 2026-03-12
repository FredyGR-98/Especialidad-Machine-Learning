"""
MÓDULO: db_manager.py

OBJETIVO:
    Centralizar la lógica de conexión y acceso a datos SQLite
    del proyecto "Breast Cancer Clinical Data Analysis Platform".

RESPONSABILIDADES:
    - abrir conexiones a la base de datos
    - validar inicio de sesión
    - buscar y registrar pacientes
    - guardar mediciones clínicas
    - consultar historial básico
"""

from pathlib import Path
import sqlite3
from typing import Any, Optional


class DatabaseManager:
    """
    Clase encargada de administrar la conexión y operaciones CRUD
    sobre la base de datos SQLite del proyecto.
    """

    def __init__(self, db_name: str = "breast_cancer_clinical.db") -> None:
        """
        Inicializa el manejador de base de datos.

        Parámetros:
            db_name (str): nombre del archivo de base de datos SQLite.
        """
        project_root = Path(__file__).resolve().parent.parent
        self.db_path = project_root / "database" / db_name

    # =========================================================
    # CONEXIÓN BASE
    # =========================================================
    def get_connection(self) -> sqlite3.Connection:
        """
        Crea y retorna una conexión a SQLite con acceso por nombre de columna.
        """
        connection = sqlite3.connect(self.db_path)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON;")
        return connection

    # =========================================================
    # AUTENTICACIÓN / USUARIOS
    # =========================================================
    def get_user_by_username(self, username: str) -> Optional[dict[str, Any]]:
        """
        Busca un usuario por username.

        Retorna:
            dict con datos del usuario si existe, o None si no existe.
        """
        query = """
            SELECT user_id, username, password_hash, role, is_active, created_at
            FROM system_users
            WHERE username = ?
        """

        with self.get_connection() as conn:
            row = conn.execute(query, (username,)).fetchone()

        return dict(row) if row else None

    def validate_login(self, username: str, password_hash: str) -> Optional[dict[str, Any]]:
        """
        Valida inicio de sesión comparando username y password_hash.

        NOTA:
            En esta etapa usamos comparación directa con password_hash
            almacenado. Más adelante convendrá usar werkzeug.security
            para verificar hash real.

        Retorna:
            dict del usuario si credenciales válidas y usuario activo.
            None si falla validación.
        """
        query = """
            SELECT user_id, username, role, is_active, created_at
            FROM system_users
            WHERE username = ?
              AND password_hash = ?
              AND is_active = 1
        """

        with self.get_connection() as conn:
            row = conn.execute(query, (username, password_hash)).fetchone()

        return dict(row) if row else None

    def create_user(self, username: str, password_hash: str, role: str = "analyst") -> int:
        """
        Crea un nuevo usuario.

        Retorna:
            user_id del usuario creado.
        """
        query = """
            INSERT INTO system_users (username, password_hash, role)
            VALUES (?, ?, ?)
        """

        with self.get_connection() as conn:
            cursor = conn.execute(query, (username, password_hash, role))
            conn.commit()
            return cursor.lastrowid

    # =========================================================
    # PACIENTES
    # =========================================================
    def get_patient_by_rut(self, rut: str) -> Optional[dict[str, Any]]:
        """
        Busca un paciente por RUT.

        Retorna:
            dict con datos del paciente si existe, o None si no existe.
        """
        query = """
            SELECT patient_id, rut, full_name, age, sex,
                   created_by_user_id, created_at, is_active
            FROM patients
            WHERE rut = ?
        """

        with self.get_connection() as conn:
            row = conn.execute(query, (rut,)).fetchone()

        return dict(row) if row else None

    def get_patient_by_id(self, patient_id: int) -> Optional[dict[str, Any]]:
        """
        Busca un paciente por ID.

        Parámetros:
            patient_id: ID interno del paciente.

        Retorna:
            dict con datos del paciente si existe, o None si no existe.
        """
        query = """
            SELECT patient_id, rut, full_name, age, sex,
                   created_by_user_id, created_at, is_active
            FROM patients
            WHERE patient_id = ?
        """

        with self.get_connection() as conn:
            row = conn.execute(query, (patient_id,)).fetchone()

        return dict(row) if row else None

    def create_patient(
        self,
        rut: str,
        full_name: str,
        age: int,
        sex: str,
        created_by_user_id: int
    ) -> int:
        """
        Registra un nuevo paciente.

        Retorna:
            patient_id del paciente creado.
        """
        query = """
            INSERT INTO patients (rut, full_name, age, sex, created_by_user_id)
            VALUES (?, ?, ?, ?, ?)
        """

        with self.get_connection() as conn:
            cursor = conn.execute(query, (rut, full_name, age, sex, created_by_user_id))
            conn.commit()
            return cursor.lastrowid

    def get_or_create_patient(
        self,
        rut: str,
        full_name: str,
        age: int,
        sex: str,
        created_by_user_id: int
    ) -> dict[str, Any]:
        """
        Busca un paciente por RUT. Si no existe, lo crea.

        Retorna:
            dict con datos del paciente encontrado o creado.
        """
        patient = self.get_patient_by_rut(rut)

        if patient:
            return patient

        patient_id = self.create_patient(
            rut=rut,
            full_name=full_name,
            age=age,
            sex=sex,
            created_by_user_id=created_by_user_id
        )

        return {
            "patient_id": patient_id,
            "rut": rut,
            "full_name": full_name,
            "age": age,
            "sex": sex,
            "created_by_user_id": created_by_user_id
        }

    def list_patients(self, search: str | None = None) -> list[dict[str, Any]]:
        """
        Lista pacientes registrados, con búsqueda opcional.

        Parámetros:
            search: texto opcional para filtrar por nombre o RUT.

        Retorna:
            lista de pacientes en formato diccionario.
        """
        query = """
            SELECT
                p.patient_id,
                p.rut,
                p.full_name,
                p.age,
                p.sex,
                p.created_at,
                p.is_active,
                COUNT(cm.measurement_id) AS total_measurements,
                MAX(cm.evaluation_date) AS last_evaluation_date
            FROM patients p
            LEFT JOIN clinical_measurements cm
                ON p.patient_id = cm.patient_id
            WHERE p.is_active = 1
        """

        params: list[Any] = []

        if search and search.strip():
            query += """
                AND (
                    p.full_name LIKE ?
                    OR p.rut LIKE ?
                )
            """
            like_value = f"%{search.strip()}%"
            params.extend([like_value, like_value])

        query += """
            GROUP BY
                p.patient_id,
                p.rut,
                p.full_name,
                p.age,
                p.sex,
                p.created_at,
                p.is_active
            ORDER BY
                p.full_name ASC,
                p.patient_id ASC
        """

        with self.get_connection() as conn:
            rows = conn.execute(query, params).fetchall()

        return [dict(row) for row in rows]

    def get_patient_with_measurements(self, patient_id: int) -> Optional[dict[str, Any]]:
        """
        Obtiene un paciente junto con su historial de mediciones.

        Parámetros:
            patient_id: ID interno del paciente.

        Retorna:
            dict con datos del paciente y lista de mediciones,
            o None si el paciente no existe.
        """
        patient = self.get_patient_by_id(patient_id)

        if not patient:
            return None

        measurements = self.get_measurements_by_patient(patient_id)

        return {
            "patient": patient,
            "measurements": measurements
        }

    # =========================================================
    # MEDICIONES CLÍNICAS
    # =========================================================
    def create_clinical_measurement(
        self,
        patient_id: int,
        recorded_by_user_id: int,
        evaluation_date: str,
        measurement_data: dict[str, Any],
        predicted_class: str,
        prediction_score: float,
        model_version: str
    ) -> int:
        """
        Inserta una medición clínica asociada a un paciente.

        Parámetros:
            patient_id: ID del paciente.
            recorded_by_user_id: ID del usuario que registra.
            evaluation_date: fecha clínica de evaluación (YYYY-MM-DD).
            measurement_data: diccionario con las 30 variables clínicas.
            predicted_class: clase predicha por el modelo.
            prediction_score: probabilidad/confianza.
            model_version: versión del modelo usada.

        Retorna:
            measurement_id del registro creado.
        """
        query = """
            INSERT INTO clinical_measurements (
                patient_id,
                recorded_by_user_id,
                evaluation_date,

                radius_mean,
                texture_mean,
                perimeter_mean,
                area_mean,
                smoothness_mean,
                compactness_mean,
                concavity_mean,
                concave_points_mean,
                symmetry_mean,
                fractal_dimension_mean,

                radius_se,
                texture_se,
                perimeter_se,
                area_se,
                smoothness_se,
                compactness_se,
                concavity_se,
                concave_points_se,
                symmetry_se,
                fractal_dimension_se,

                radius_worst,
                texture_worst,
                perimeter_worst,
                area_worst,
                smoothness_worst,
                compactness_worst,
                concavity_worst,
                concave_points_worst,
                symmetry_worst,
                fractal_dimension_worst,

                predicted_class,
                prediction_score,
                model_version
            )
            VALUES (
                ?, ?, ?,
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                ?, ?, ?
            )
        """

        values = (
            patient_id,
            recorded_by_user_id,
            evaluation_date,

            measurement_data["radius_mean"],
            measurement_data["texture_mean"],
            measurement_data["perimeter_mean"],
            measurement_data["area_mean"],
            measurement_data["smoothness_mean"],
            measurement_data["compactness_mean"],
            measurement_data["concavity_mean"],
            measurement_data["concave_points_mean"],
            measurement_data["symmetry_mean"],
            measurement_data["fractal_dimension_mean"],

            measurement_data["radius_se"],
            measurement_data["texture_se"],
            measurement_data["perimeter_se"],
            measurement_data["area_se"],
            measurement_data["smoothness_se"],
            measurement_data["compactness_se"],
            measurement_data["concavity_se"],
            measurement_data["concave_points_se"],
            measurement_data["symmetry_se"],
            measurement_data["fractal_dimension_se"],

            measurement_data["radius_worst"],
            measurement_data["texture_worst"],
            measurement_data["perimeter_worst"],
            measurement_data["area_worst"],
            measurement_data["smoothness_worst"],
            measurement_data["compactness_worst"],
            measurement_data["concavity_worst"],
            measurement_data["concave_points_worst"],
            measurement_data["symmetry_worst"],
            measurement_data["fractal_dimension_worst"],

            predicted_class,
            prediction_score,
            model_version
        )

        with self.get_connection() as conn:
            cursor = conn.execute(query, values)
            conn.commit()
            return cursor.lastrowid

    def get_measurements_by_patient(self, patient_id: int) -> list[dict[str, Any]]:
        """
        Obtiene historial de mediciones de un paciente.
        """
        query = """
            SELECT *
            FROM clinical_measurements
            WHERE patient_id = ?
            ORDER BY evaluation_date DESC, measurement_id DESC
        """

        with self.get_connection() as conn:
            rows = conn.execute(query, (patient_id,)).fetchall()

        return [dict(row) for row in rows]
    
    
    def get_user_by_id(self, user_id: int) -> Optional[dict[str, Any]]:
        """
        Busca un usuario por su ID.

        Retorna:
            dict con datos del usuario si existe, o None si no existe.
        """
        query = """
            SELECT user_id, username, role, is_active, created_at
            FROM system_users
            WHERE user_id = ?
              AND is_active = 1
        """

        with self.get_connection() as conn:
            row = conn.execute(query, (user_id,)).fetchone()

        return dict(row) if row else None