PRAGMA foreign_keys = ON;

-- =========================================================
-- DATOS DE PRUEBA: USUARIOS
-- =========================================================
INSERT INTO system_users (username, password_hash, role)
VALUES
('admin', 'hashed_password_admin', 'admin'),
('analyst1', 'hashed_password_analyst1', 'analyst'),
('doctor_demo', 'hashed_password_doctor_demo', 'analyst');

-- =========================================================
-- DATOS DE PRUEBA: PACIENTES
-- =========================================================
INSERT INTO patients (rut, full_name, age, sex, created_by_user_id)
VALUES
('12.345.678-9', 'María González', 52, 'F', 1),
('9.876.543-2', 'Ana Rodríguez', 47, 'F', 1),
('15.234.567-8', 'Carolina Muñoz', 61, 'F', 2),
('11.222.333-4', 'Patricia Soto', 39, 'F', 2),
('17.888.999-0', 'Laura Herrera', 55, 'F', 3);

-- =========================================================
-- DATOS DE PRUEBA: MEDICIONES CLÍNICAS
-- =========================================================
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
VALUES
(
    1, 1, '2026-03-01',

    14.10, 20.30, 92.40, 654.20, 0.090, 0.120, 0.100, 0.050, 0.180, 0.060,
    0.400, 1.200, 3.100, 32.100, 0.006, 0.020, 0.030, 0.010, 0.020, 0.004,
    17.20, 28.30, 110.40, 880.50, 0.130, 0.300, 0.400, 0.120, 0.250, 0.080,

    'Malignant', 0.87, 'rf_v1'
),
(
    2, 2, '2026-03-02',

    12.30, 15.20, 78.20, 420.10, 0.080, 0.070, 0.050, 0.030, 0.150, 0.050,
    0.300, 1.000, 2.500, 24.300, 0.005, 0.015, 0.020, 0.009, 0.018, 0.003,
    13.80, 19.10, 90.30, 580.20, 0.110, 0.200, 0.150, 0.070, 0.220, 0.070,

    'Benign', 0.23, 'rf_v1'
),
(
    3, 2, '2026-03-03',

    18.10, 22.50, 118.00, 1020.00, 0.100, 0.180, 0.190, 0.090, 0.210, 0.070,
    0.600, 1.400, 4.800, 55.000, 0.007, 0.030, 0.040, 0.015, 0.025, 0.005,
    24.50, 30.80, 160.20, 1500.00, 0.140, 0.450, 0.500, 0.200, 0.300, 0.090,

    'Malignant', 0.95, 'rf_v1'
),
(
    4, 3, '2026-03-04',

    11.80, 14.70, 75.40, 390.60, 0.075, 0.060, 0.030, 0.020, 0.140, 0.055,
    0.250, 0.900, 2.100, 20.400, 0.004, 0.012, 0.018, 0.007, 0.016, 0.002,
    13.20, 17.90, 84.50, 500.70, 0.100, 0.150, 0.090, 0.050, 0.200, 0.060,

    'Benign', 0.12, 'rf_v1'
),
(
    5, 1, '2026-03-05',

    15.40, 19.80, 101.30, 720.40, 0.095, 0.140, 0.120, 0.060, 0.190, 0.062,
    0.450, 1.100, 3.600, 36.500, 0.006, 0.022, 0.032, 0.011, 0.021, 0.004,
    19.80, 25.70, 128.60, 980.30, 0.128, 0.320, 0.360, 0.140, 0.260, 0.082,

    'Malignant', 0.81, 'rf_v1'
),
(
    1, 2, '2026-03-06',

    13.50, 18.60, 88.70, 610.90, 0.086, 0.100, 0.080, 0.040, 0.170, 0.058,
    0.350, 1.050, 2.900, 28.700, 0.005, 0.018, 0.025, 0.009, 0.019, 0.003,
    16.10, 24.20, 104.90, 810.80, 0.120, 0.260, 0.280, 0.100, 0.240, 0.075,

    'Benign', 0.41, 'rf_v1'
);