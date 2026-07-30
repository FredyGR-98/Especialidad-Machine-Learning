r"""
Genera pacientes y evaluaciones clinicas sinteticas para poblar
la base de datos demo del proyecto.

Uso:
    .\mlops-env\Scripts\python.exe scripts\seed_demo_patients.py
    .\mlops-env\Scripts\python.exe scripts\seed_demo_patients.py --patients 20 --evaluations 3
    .\mlops-env\Scripts\python.exe scripts\seed_demo_patients.py --patients 60 --evaluations 4 --start-year 2020 --end-year 2026
"""

from __future__ import annotations

import argparse
import logging
import random
import sys
from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from api.api import app
from database.db_manager import DatabaseManager
from frontend.utils.feature_config import FEATURE_INPUT_CONFIG


logging.getLogger("api.api").setLevel(logging.WARNING)
db = DatabaseManager()


FIRST_NAMES = [
    "Camila",
    "Valentina",
    "Martina",
    "Sofia",
    "Isidora",
    "Antonia",
    "Josefa",
    "Catalina",
    "Florencia",
    "Fernanda",
    "Daniela",
    "Paula",
    "Andrea",
    "Claudia",
    "Carolina",
    "Maria Jose",
]

LAST_NAMES = [
    "Gonzalez",
    "Munoz",
    "Rojas",
    "Diaz",
    "Perez",
    "Soto",
    "Contreras",
    "Silva",
    "Martinez",
    "Sepulveda",
    "Morales",
    "Torres",
    "Castillo",
    "Flores",
    "Reyes",
    "Herrera",
]

HIGH_RISK_FIELDS = {
    "radius_mean",
    "texture_mean",
    "perimeter_mean",
    "area_mean",
    "compactness_mean",
    "concavity_mean",
    "concave_points_mean",
    "radius_worst",
    "texture_worst",
    "perimeter_worst",
    "area_worst",
    "compactness_worst",
    "concavity_worst",
    "concave_points_worst",
}


@dataclass
class SeedStats:
    patients_created: int = 0
    evaluations_created: int = 0
    failed_requests: int = 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Carga pacientes y evaluaciones sinteticas en la base demo."
    )
    parser.add_argument(
        "--patients",
        type=int,
        default=18,
        help="Cantidad de pacientes sinteticos a generar.",
    )
    parser.add_argument(
        "--evaluations",
        type=int,
        default=2,
        help="Cantidad de evaluaciones por paciente.",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=20260729,
        help="Semilla para resultados reproducibles.",
    )
    parser.add_argument(
        "--start-year",
        type=int,
        default=2020,
        help="Ano inicial para distribuir las evaluaciones sinteticas.",
    )
    parser.add_argument(
        "--end-year",
        type=int,
        default=date.today().year,
        help="Ano final para distribuir las evaluaciones sinteticas.",
    )
    parser.add_argument(
        "--min-age",
        type=int,
        default=31,
        help="Edad minima para los pacientes sinteticos.",
    )
    parser.add_argument(
        "--max-age",
        type=int,
        default=78,
        help="Edad maxima para los pacientes sinteticos.",
    )
    return parser


def sample_value(field_name: str, metadata: dict, profile: str) -> float:
    min_value = float(metadata["min"])
    max_value = float(metadata["max"])
    q1_value = float(metadata["q1"])
    q3_value = float(metadata["q3"])
    step_value = float(metadata["step"])

    if profile == "malignant":
        if field_name in HIGH_RISK_FIELDS:
            lower = q3_value
            upper = max_value
        else:
            lower = q1_value
            upper = max_value
    else:
        if field_name in HIGH_RISK_FIELDS:
            lower = min_value
            upper = q1_value
        else:
            lower = min_value
            upper = q3_value

    if upper < lower:
        lower, upper = upper, lower

    sampled = random.uniform(lower, upper)
    decimals = infer_decimals(step_value)
    return round(clamp(sampled, min_value, max_value), decimals)


def infer_decimals(step_value: float) -> int:
    step_text = f"{step_value:.5f}".rstrip("0")

    if "." not in step_text:
        return 0

    return len(step_text.split(".")[1])


def clamp(value: float, min_value: float, max_value: float) -> float:
    return max(min_value, min(max_value, value))


def generate_measurement(profile: str) -> dict[str, float]:
    measurement: dict[str, float] = {}

    for field_name, metadata in FEATURE_INPUT_CONFIG.items():
        measurement[field_name] = sample_value(field_name, metadata, profile)

    return measurement


def generate_patient_name(index: int) -> str:
    first_name = FIRST_NAMES[index % len(FIRST_NAMES)]
    last_name = LAST_NAMES[(index * 3) % len(LAST_NAMES)]
    second_last_name = LAST_NAMES[(index * 5 + 2) % len(LAST_NAMES)]
    return f"{first_name} {last_name} {second_last_name}"


def generate_rut(index: int) -> str:
    base = 20_000_000 + index * 731
    digits = f"{base:08d}"
    return f"{digits[:2]}.{digits[2:5]}.{digits[5:8]}-{index % 10}"


def get_existing_patient_count() -> int:
    with db.get_connection() as conn:
        return int(conn.execute("SELECT COUNT(*) FROM patients").fetchone()[0])


def build_patient_schedule(
    evaluations: int,
    global_start: date,
    global_end: date,
) -> list[date]:
    if evaluations <= 0:
        return []

    if evaluations == 1:
        span_days = max((global_end - global_start).days, 0)
        return [global_start + timedelta(days=random.randint(0, span_days))]

    max_gap_days = 180
    min_gap_days = 35
    reserved_span = (evaluations - 1) * max_gap_days
    latest_first_date = global_end - timedelta(days=reserved_span)

    if latest_first_date < global_start:
        latest_first_date = global_start

    first_span_days = max((latest_first_date - global_start).days, 0)
    first_date = global_start + timedelta(days=random.randint(0, first_span_days))

    schedule = [first_date]
    current_date = first_date

    for _ in range(1, evaluations):
        next_gap = random.randint(min_gap_days, max_gap_days)
        next_date = current_date + timedelta(days=next_gap)
        schedule.append(min(next_date, global_end))
        current_date = schedule[-1]

    return schedule


def generate_payload(
    patient_index: int,
    evaluation_index: int,
    patient_offset: int,
    evaluation_date: date,
    min_age: int,
    max_age: int,
) -> dict:
    profile = "malignant" if (patient_index + evaluation_index) % 4 == 0 else "benign"
    patient_age = random.randint(min_age, max_age)
    patient_id_offset = patient_offset + patient_index + 1

    return {
        "user_id": (patient_index % 3) + 1,
        "patient": {
            "rut": generate_rut(patient_id_offset),
            "full_name": generate_patient_name(patient_id_offset),
            "age": patient_age,
            "sex": "F",
        },
        "measurement": generate_measurement(profile),
        "evaluation_date": evaluation_date.isoformat(),
    }


def seed_demo_data(
    patients: int,
    evaluations: int,
    seed: int,
    start_year: int,
    end_year: int,
    min_age: int,
    max_age: int,
) -> SeedStats:
    random.seed(seed)
    stats = SeedStats()
    registered_ruts: set[str] = set()
    patient_offset = get_existing_patient_count()
    start_date = date(start_year, 1, 1)
    max_end_date = date.today()
    requested_end_date = date(end_year, 12, 31)
    end_date = min(requested_end_date, max_end_date)

    with app.test_client() as client:
        for patient_index in range(patients):
            schedule = build_patient_schedule(evaluations, start_date, end_date)

            for evaluation_index, evaluation_date in enumerate(schedule):
                payload = generate_payload(
                    patient_index=patient_index,
                    evaluation_index=evaluation_index,
                    patient_offset=patient_offset,
                    evaluation_date=evaluation_date,
                    min_age=min_age,
                    max_age=max_age,
                )
                response = client.post("/predict-and-save", json=payload)
                body = response.get_json(silent=True) or {}

                if response.status_code != 200 or not body.get("success"):
                    stats.failed_requests += 1
                    print(
                        f"[ERROR] paciente={patient_index + 1} "
                        f"evaluacion={evaluation_index + 1} "
                        f"status={response.status_code} detail={body}"
                    )
                    continue

                stats.evaluations_created += 1
                rut = payload["patient"]["rut"]

                if rut not in registered_ruts:
                    registered_ruts.add(rut)
                    stats.patients_created += 1

    return stats


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.patients <= 0 or args.evaluations <= 0:
        raise SystemExit("Los parametros --patients y --evaluations deben ser mayores que 0.")

    if args.start_year > args.end_year:
        raise SystemExit("El ano inicial no puede ser mayor que el ano final.")

    if args.min_age > args.max_age:
        raise SystemExit("La edad minima no puede ser mayor que la edad maxima.")

    print("Cargando datos sinteticos en la base demo...")
    print(
        f"Pacientes nuevos: {args.patients} | "
        f"Evaluaciones por paciente: {args.evaluations} | "
        f"Periodo: {args.start_year}-{args.end_year} | "
        f"Edades: {args.min_age}-{args.max_age}"
    )

    stats = seed_demo_data(
        patients=args.patients,
        evaluations=args.evaluations,
        seed=args.seed,
        start_year=args.start_year,
        end_year=args.end_year,
        min_age=args.min_age,
        max_age=args.max_age,
    )

    print("")
    print("Carga finalizada")
    print(f"Pacientes insertados: {stats.patients_created}")
    print(f"Evaluaciones creadas: {stats.evaluations_created}")
    print(f"Solicitudes fallidas: {stats.failed_requests}")


if __name__ == "__main__":
    main()
