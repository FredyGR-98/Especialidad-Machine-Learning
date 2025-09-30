"""
===========================================================
🧪 test_api.py — Pruebas automáticas para la API
===========================================================

Este script realiza pruebas automáticas sobre la API de Flask:
1. Valida que el endpoint raíz `/` responda correctamente.
2. Envía un ejemplo de caso Maligno y muestra la predicción.
3. Envía un ejemplo de caso Benigno y muestra la predicción.
4. Envía datos inválidos para verificar manejo de errores.

✅ Además, imprime los datos de entrada usados en cada prueba,
para que el usuario pueda copiarlos y probarlos manualmente
con `curl` o Postman si lo desea.
"""

import requests

BASE_URL = "http://127.0.0.1:5000"

# Ejemplos de prueba (extraídos del dataset original)
CASE_MALIGNO = {
    "features": [
        17.99, 10.38, 122.8, 1001, 0.1184, 0.2776, 0.3001, 0.1471, 0.2419, 0.07871,
        1.095, 0.9053, 8.589, 153.4, 0.006399, 0.04904, 0.05373, 0.01587, 0.03003,
        0.006193, 25.38, 17.33, 184.6, 2019, 0.1622, 0.6656, 0.7119, 0.2654, 0.4601,
        0.1189
    ]
}

CASE_BENIGNO = {
    "features": [
        12.32, 12.39, 78.85, 464.1, 0.1028, 0.06981, 0.03987, 0.037, 0.1959, 0.05955,
        0.3068, 0.3196, 2.217, 24.54, 0.0089, 0.0131, 0.018, 0.0098, 0.0184,
        0.0035, 15.11, 19.26, 99.7, 674.7, 0.1316, 0.1529, 0.1882, 0.0844, 0.2252,
        0.0731
    ]
}

print("🚀 Ejecutando pruebas automáticas de la API...\n")

# 1️⃣ Test GET /
try:
    r = requests.get(f"{BASE_URL}/")
    if r.status_code == 200:
        print("✅ GET / → funciona correctamente")
    else:
        print(f"❌ GET / → error {r.status_code}")
except Exception as e:
    print("❌ GET / → no se pudo conectar:", e)

# 2️⃣ Test POST /predict con caso Maligno
print("\n🔬 Probando caso MALIGNO con los siguientes datos:")
print(CASE_MALIGNO, "\n")
try:
    r = requests.post(f"{BASE_URL}/predict", json=CASE_MALIGNO)
    print("✅ POST /predict (Maligno) → respuesta:", r.json())
except Exception as e:
    print("❌ POST /predict (Maligno) → error:", e)

# 3️⃣ Test POST /predict con caso Benigno
print("\n🔬 Probando caso BENIGNO con los siguientes datos:")
print(CASE_BENIGNO, "\n")
try:
    r = requests.post(f"{BASE_URL}/predict", json=CASE_BENIGNO)
    print("✅ POST /predict (Benigno) → respuesta:", r.json())
except Exception as e:
    print("❌ POST /predict (Benigno) → error:", e)

# 4️⃣ Test POST /predict con datos inválidos
print("\n🔬 Probando caso INVÁLIDO:")
try:
    r = requests.post(f"{BASE_URL}/predict", json={"foo": "bar"})
    if r.status_code == 400:
        print("✅ POST /predict (datos inválidos) → retorna error 400 correctamente")
    else:
        print(f"❌ POST /predict (datos inválidos) → error {r.status_code}")
except Exception as e:
    print("❌ POST /predict (datos inválidos) → error:", e)