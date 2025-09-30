# 🎗️ Clasificador de Cáncer de Mama con Flask + Docker  

Un proyecto de **Machine Learning aplicado a la salud** que permite predecir si un tumor es **benigno** o **maligno**, utilizando un modelo entrenado sobre el dataset de *Breast Cancer* de `scikit-learn`.  

Incluye:  
- 🧠 **Modelo predictivo** entrenado con Random Forest.  
- 🌐 **API Flask** para exponer el modelo vía REST.  
- 🎨 **Frontend en HTML** con sliders interactivos y ejemplos precargados.  
- 🧪 **Pruebas automáticas** para validar los endpoints.  
- 🐳 **Dockerfile** para garantizar portabilidad en cualquier entorno.  

---

## 📌 Descripción del Proyecto  

La finalidad de este proyecto es ofrecer una herramienta simple que permita predecir, en base a 30 características clínicas de un tumor, si es **benigno** o **maligno**.  

📊 El dataset utilizado proviene de `scikit-learn` e incluye variables como:  
- Radio promedio  
- Textura promedio  
- Perímetro promedio  
- Área promedio  
- Suavidad, compacidad y concavidad  
- Simetría y dimensión fractal  
- Entre otras mediciones clínicas derivadas  

Estas características se ingresan en el sistema y el modelo devuelve una predicción interpretada como:  
- ✅ **Benigno**  
- 🔎 **Maligno**  

---

## 📂 Estructura del Proyecto  

breast-cancer-mlops/
├── app.py              # API Flask (rutas / y /predict)
├── train_model.py      # Script de entrenamiento (Random Forest)
├── test_api.py         # Pruebas automáticas de la API
├── index.html          # Interfaz web con sliders interactivos
├── requirements.txt    # Dependencias necesarias
├── Dockerfile          # Contenerización del proyecto
├── model.joblib        # Modelo entrenado y serializado
└── README.md           # Documentación del proyecto

---

## ⚡ Instalación y Requisitos  

### Prerrequisitos  
- Python 3.8+  
- pip  
- Docker (opcional, para ejecución contenerizada)  

### 1️⃣ Clonar el repositorio  
```bash
git clone <url-del-repositorio>
cd breast-cancer-mlops
```
### 2️⃣ Instalar dependencias 
```bash
pip install -r requirements.txt
```

---

## 🚀 Uso del Sistema  
### 1. Entrenar el modelo  
```bash
py train_model.py
```
### 2. Ejecutar la API Flask
```bash
python app.py

```

---
## 🧪 Pruebas Automáticas  
Antes de interactuar con el frontend, se recomienda **probar la API** para corroborar que el servicio responde correctamente.  

Ejecutar:  
```bash
python test_api.py
```
Este script valida:
✔️ Respuesta del endpoint raíz / (salud del servicio)
✔️ Predicción para casos maligno y benigno
✔️ Manejo de errores con JSON inválido

---

## 🎨 Frontend Interactivo (HTML)

Abrir en el navegador:
http://127.0.0.1:5000/

El sistema despliega una interfaz en HTML con las siguientes características:
🎚️ Sliders dinámicos para las 30 variables del modelo.
📌 Ejemplos precargados (Maligno / Benigno) para comprobar rápidamente el sistema.
✅ Resultados visuales en pantalla con mensajes claros según la predicción.
Esto permite una interacción más dinámica e intuitiva en comparación con las pruebas manuales.

---

## 🐳 Ejecución con Docker
# 1. Construir la imagen
```bash
docker build -t breast-cancer-api-modular:latest .
```
# 2. Ejecutar el contenedor
```bash
docker run -d -p 5000:5000 --name breast-cancer-container breast-cancer-api-modular:latest
```

---

## ✍️ Autoría  

📌 Este proyecto corresponde a la **Evaluación Modular** del programa **Talento Digital – Kibernum**.  

- 👤 **Autor:** Fredy Geraldo Rivera  