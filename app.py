"""
===========================================================
📌 app.py — API para servir el modelo de predicción
===========================================================

Este archivo implementa una API usando Flask, la cual permite
realizar predicciones con el modelo previamente entrenado
y guardado en 'model.joblib'.

⚙️ Flujo general:
1. Se carga el modelo entrenado desde el archivo 'model.joblib'.
2. Se define un endpoint raíz `/` que retorna la interfaz HTML
   con sliders interactivos para ingresar características.
3. Se define un endpoint `/predict` que recibe datos en formato JSON.
4. Se validan los datos de entrada y se procesan con el modelo.
5. Se retorna la predicción correspondiente (benigno/maligno) en JSON.

✅ Importancia:
Sin este archivo, el modelo no podría “exponerse” al exterior.
Gracias a esta API, aplicaciones o usuarios externos pueden
enviar información y recibir respuestas automáticas del modelo.

🎯 Justificación de diseño:
- Se incluyó **validación de entrada** para asegurar que los datos
  enviados contengan el campo "features" y evitar fallos silenciosos.
- Se añadió **manejo de errores y logging** para mejorar la trazabilidad
  y depuración durante el desarrollo y despliegue.
- Se integró un **frontend en HTML** con sliders dinámicos para
  facilitar la interacción con el modelo de forma visual y práctica,
  lo que mejora la experiencia del usuario y hace más didáctico
  comprender cómo cambian las predicciones.
"""
# ==========================
# 📚 Importación de librerías
# ==========================
from flask import Flask, request, render_template, jsonify
import numpy as np
import joblib
import logging

# ==========================
# 📝 Configuración de logging
# ==========================
# Solo en consola, con formato más legible
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s — %(levelname)s — %(message)s",
    datefmt="%H:%M:%S"
)

# ==========================
# 🚀 Inicialización de la aplicación Flask
# ==========================
# Indicamos que las plantillas HTML estarán en la carpeta "templates"
app = Flask(__name__, template_folder="templates")

# ==========================
# 📦 Carga del modelo entrenado
# ==========================
# Se carga el modelo previamente serializado con joblib.
# Esto evita reentrenar el modelo cada vez que iniciamos la API.
model = joblib.load("model.joblib")

# Diccionario que traduce las clases numéricas a nombres más claros
CLASSES = {0: "malignant", 1: "benign"}


# ==========================
# 🌐 Ruta principal (GET /)
# ==========================
@app.route("/", methods=["GET"])
def home():
    """
    Página principal:
    Renderiza la interfaz `index.html` ubicada en la carpeta /templates.
    Aquí es donde se despliega la interfaz gráfica del usuario.
    """
    return render_template("index.html")


# ==========================
# 🔮 Ruta de predicción (POST /predict)
# ==========================
@app.route("/predict", methods=["POST"])
def predict():
    """
    Endpoint de predicción:
    - Recibe datos desde la interfaz o un cliente externo en formato JSON.
    - Valida que los datos sean correctos.
    - Ejecuta el modelo para generar la predicción.
    - Retorna la clase predicha en formato JSON.

    Ejemplo de entrada JSON:
    {
        "features": [13.0, 20.0, 80.0, 500.0, ..., 0.25, 0.07]
    }
    """
    try:
        # 1️⃣ Verificamos que se haya recibido un JSON válido
        data = request.json
        if not data or "features" not in data:
            return jsonify({"error": "⚠️ No se recibieron datos válidos"}), 400

        # 2️⃣ Convertimos los datos en un array de NumPy
        input_array = np.array(data["features"]).reshape(1, -1)

        # 3️⃣ Realizamos la predicción con el modelo cargado
        prediction = model.predict(input_array)[0]

        # 4️⃣ Obtenemos el nombre de la clase (benigno / maligno)
        class_name = CLASSES.get(int(prediction), "unknown")

        # 5️⃣ Retornamos el resultado en formato JSON
        return jsonify({
            "prediction": int(prediction),
            "class_name": class_name
        })

    except Exception as e:
        # ⚠️ Manejo de errores: en caso de fallar, devolvemos el error
        return jsonify({"error": str(e)}), 500


# ==========================
# ▶️ Ejecución de la aplicación
# ==========================
if __name__ == "__main__":
    # El host 0.0.0.0 permite que la API sea accesible en red local.
    # El modo debug=True facilita detectar errores durante desarrollo.
    app.run(host="0.0.0.0", port=5000, debug=True)