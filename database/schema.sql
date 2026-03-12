PRAGMA foreign_keys = ON;

-- =========================================================
-- TABLA 1: USUARIOS DEL SISTEMA
-- =========================================================
CREATE TABLE IF NOT EXISTS system_users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'analyst',
    is_active INTEGER NOT NULL DEFAULT 1 CHECK (is_active IN (0, 1)),
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- =========================================================
-- TABLA 2: PACIENTES
-- =========================================================
CREATE TABLE IF NOT EXISTS patients (
    patient_id INTEGER PRIMARY KEY AUTOINCREMENT,
    rut TEXT NOT NULL UNIQUE,
    full_name TEXT NOT NULL,
    age INTEGER NOT NULL CHECK (age > 0),
    sex TEXT NOT NULL CHECK (sex IN ('F', 'M', 'Other')),
    created_by_user_id INTEGER NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    is_active INTEGER NOT NULL DEFAULT 1 CHECK (is_active IN (0, 1)),
    FOREIGN KEY (created_by_user_id) REFERENCES system_users(user_id)
);

-- =========================================================
-- TABLA 3: MEDICIONES CLÍNICAS
-- =========================================================
CREATE TABLE IF NOT EXISTS clinical_measurements (
    measurement_id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER NOT NULL,
    recorded_by_user_id INTEGER NOT NULL,

    evaluation_date TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,

    radius_mean REAL NOT NULL,
    texture_mean REAL NOT NULL,
    perimeter_mean REAL NOT NULL,
    area_mean REAL NOT NULL,
    smoothness_mean REAL NOT NULL,
    compactness_mean REAL NOT NULL,
    concavity_mean REAL NOT NULL,
    concave_points_mean REAL NOT NULL,
    symmetry_mean REAL NOT NULL,
    fractal_dimension_mean REAL NOT NULL,

    radius_se REAL NOT NULL,
    texture_se REAL NOT NULL,
    perimeter_se REAL NOT NULL,
    area_se REAL NOT NULL,
    smoothness_se REAL NOT NULL,
    compactness_se REAL NOT NULL,
    concavity_se REAL NOT NULL,
    concave_points_se REAL NOT NULL,
    symmetry_se REAL NOT NULL,
    fractal_dimension_se REAL NOT NULL,

    radius_worst REAL NOT NULL,
    texture_worst REAL NOT NULL,
    perimeter_worst REAL NOT NULL,
    area_worst REAL NOT NULL,
    smoothness_worst REAL NOT NULL,
    compactness_worst REAL NOT NULL,
    concavity_worst REAL NOT NULL,
    concave_points_worst REAL NOT NULL,
    symmetry_worst REAL NOT NULL,
    fractal_dimension_worst REAL NOT NULL,

    predicted_class TEXT NOT NULL CHECK (predicted_class IN ('Benign', 'Malignant')),
    prediction_score REAL NOT NULL CHECK (prediction_score >= 0 AND prediction_score <= 1),
    model_version TEXT NOT NULL,

    FOREIGN KEY (patient_id) REFERENCES patients(patient_id),
    FOREIGN KEY (recorded_by_user_id) REFERENCES system_users(user_id)
);

-- =========================================================
-- ÍNDICES PARA MEJORAR CONSULTAS
-- =========================================================
CREATE INDEX IF NOT EXISTS idx_patients_rut
ON patients(rut);

CREATE INDEX IF NOT EXISTS idx_measurements_patient_id
ON clinical_measurements(patient_id);

CREATE INDEX IF NOT EXISTS idx_measurements_recorded_by_user_id
ON clinical_measurements(recorded_by_user_id);

CREATE INDEX IF NOT EXISTS idx_measurements_evaluation_date
ON clinical_measurements(evaluation_date);