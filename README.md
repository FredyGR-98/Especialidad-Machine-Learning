# 🎗️ Clasificador de Cáncer de Mama — MLOps con Flask, Docker & GitHub Actions  

Un proyecto de **Machine Learning aplicado a la salud** que permite predecir si un tumor es **benigno** o **maligno**, utilizando el dataset *Breast Cancer* de `scikit-learn`.  

Incluye:  
- 🧠 **Modelo predictivo** entrenado con Random Forest.  
- 🌐 **API Flask** que expone el modelo como servicio REST.  
- 🎨 **Frontend HTML** con sliders interactivos y ejemplos precargados.  
- 🧪 **Pruebas automáticas** para validar endpoints.  
- 🐳 **Dockerfile** para portabilidad en cualquier entorno.  
- ⚙️ **GitHub Actions** para integración continua (CI/CD).  
- 🚫 **.gitignore** para mantener el repo limpio y ordenado.  

---

## 📌 Descripción del Proyecto  

La finalidad de este proyecto es ofrecer una herramienta simple que, en base a 30 características clínicas de un tumor, prediga si es **benigno** o **maligno**.  

📊 El dataset utilizado proviene de `scikit-learn` e incluye variables como:  
- Radio, textura, perímetro y área promedio  
- Suavidad, compacidad y concavidad  
- Simetría y dimensión fractal  
- Entre otras mediciones clínicas derivadas  

Predicciones posibles:  
- ✅ **Benigno**  
- 🔎 **Maligno**  

---

## 📂 Estructura del Proyecto  

breast-cancer-mlops/
├── .github/workflows/   # CI/CD con GitHub Actions
│   └── deploy.yml
├── templates/           # Frontend HTML
│   └── index.html
├── .gitignore           # Exclusión de archivos innecesarios
├── app.py               # API Flask (rutas / y /predict)
├── train_model.py       # Entrenamiento del modelo
├── test_api.py          # Pruebas automáticas de la API
├── requirements.txt     # Dependencias necesarias
├── Dockerfile           # Contenerización
├── model.joblib         # Modelo entrenado y serializado
└── README.md            # Documentación del proyecto


---

## ⚡ Instalación y Requisitos  

### Prerrequisitos  
- Python 3.10+ (probado con 3.13.5)  
- pip  
- Docker (opcional, para ejecución contenerizada)  
- GitHub Actions habilitado (para CI/CD)  

### 1️⃣ Clonar el repositorio  
```bash
git clone <url-del-repositorio>
cd breast-cancer-mlops
```
### 2️⃣ Crear entorno virtual (opcional pero recomendado)
```bash
py -m venv mlops-env
mlops-env\Scripts\activate   # En Windows PowerShell
```
### 3️⃣ Instalar dependencias
```bash
pip install -r requirements.txt
```

---

## 🚀 Uso del Sistema  
### 1. Entrenar el modelo  
```bash
py train_model.py
```
✔️ Esto generará model.joblib en el directorio raíz.

### 2. Ejecutar la API Flask
```bash
python app.py
```
✔️ Disponible en http://127.0.0.1:5000

---

## 🧪 Pruebas Automáticas  
Antes de interactuar con el frontend, se recomienda **probar la API** para corroborar que el servicio responde correctamente.  
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
- 🎚️ Sliders dinámicos para las 30 variables del modelo.
- 📌 Ejemplos precargados (Maligno / Benigno) para comprobar rápidamente el sistema.
- ✅ Resultados visuales en pantalla con mensajes claros según la predicción.
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

## ⚙️ CI/CD con GitHub Actions  

Cada vez que haces *push* al repositorio, se ejecuta automáticamente un flujo de trabajo definido en `.github/workflows/deploy.yml`.  

Este flujo realiza las siguientes tareas:  
1. 🛠️ **Checkout** del código más reciente.  
2. 📦 **Instalación** de dependencias desde `requirements.txt`.  
3. 🧠 **Entrenamiento** del modelo (`train_model.py`).  
4. ✅ **Ejecución de pruebas** (`test_api.py`).  

Esto asegura:  
- Que el proyecto siempre se mantenga en buen estado.  
- Que las pruebas se ejecuten de forma automática.  
- Que el despliegue sea más fácil y confiable.  

---

## ✍️ Autoría  

📌 Este proyecto corresponde a la **Evaluación Modular** del programa **Talento Digital – Kibernum**.  

- 👤 **Autor:** Fredy Geraldo Rivera  