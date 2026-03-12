"""
SCRIPT DE PRUEBA PARA DB_MANAGER
"""

from database.db_manager import DatabaseManager


def run_tests():

    db = DatabaseManager()

    print("\n========== TEST LOGIN ==========")

    user = db.validate_login("admin", "hashed_password_admin")

    if user:
        print("Login exitoso:")
        print(user)
    else:
        print("Login fallido")

    print("\n========== TEST PACIENTE ==========")

    patient = db.get_or_create_patient(
        rut="18.123.456-7",
        full_name="Paciente de Prueba",
        age=45,
        sex="F",
        created_by_user_id=1
    )

    print("Paciente encontrado o creado:")
    print(patient)

    print("\n========== TEST MEDICIÓN ==========")

    measurement_data = {

        "radius_mean": 13.5,
        "texture_mean": 18.6,
        "perimeter_mean": 88.7,
        "area_mean": 610.9,
        "smoothness_mean": 0.086,
        "compactness_mean": 0.100,
        "concavity_mean": 0.080,
        "concave_points_mean": 0.040,
        "symmetry_mean": 0.170,
        "fractal_dimension_mean": 0.058,

        "radius_se": 0.350,
        "texture_se": 1.050,
        "perimeter_se": 2.900,
        "area_se": 28.700,
        "smoothness_se": 0.005,
        "compactness_se": 0.018,
        "concavity_se": 0.025,
        "concave_points_se": 0.009,
        "symmetry_se": 0.019,
        "fractal_dimension_se": 0.003,

        "radius_worst": 16.1,
        "texture_worst": 24.2,
        "perimeter_worst": 104.9,
        "area_worst": 810.8,
        "smoothness_worst": 0.120,
        "compactness_worst": 0.260,
        "concavity_worst": 0.280,
        "concave_points_worst": 0.100,
        "symmetry_worst": 0.240,
        "fractal_dimension_worst": 0.075
    }

    measurement_id = db.create_clinical_measurement(

        patient_id=patient["patient_id"],
        recorded_by_user_id=1,
        evaluation_date="2026-03-06",
        measurement_data=measurement_data,
        predicted_class="Benign",
        prediction_score=0.41,
        model_version="rf_v1"

    )

    print("Medición creada con ID:")
    print(measurement_id)

    print("\n========== HISTORIAL PACIENTE ==========")

    history = db.get_measurements_by_patient(patient["patient_id"])

    print(history)


if __name__ == "__main__":
    run_tests()