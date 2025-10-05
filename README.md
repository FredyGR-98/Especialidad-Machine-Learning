# 🎗️ Clasificador de Cáncer de Mama — MLOps con Flask, Streamlit & Docker  

Un proyecto educativo de **Machine Learning aplicado a la salud** que permite predecir si un tumor es **benigno** o **maligno**, utilizando el dataset *Breast Cancer* de `scikit-learn`.  

Incluye:  
- 🧠 **Random Forest** entrenado en Python.  
- 🌐 **API Flask** para exponer el modelo como servicio REST.  
- 🎨 **Frontend en Streamlit** con ejemplos visuales y sliders interactivos.  
- 🐳 **Docker Compose** para levantar API + Frontend en contenedores.  
- ⚙️ **GitHub Actions (CI/CD)** para pruebas automáticas.  

---

## 📌 Descripción del Proyecto  

La finalidad es ofrecer una herramienta simple que, en base a **30 características clínicas** de un tumor, prediga si es **benigno** o **maligno**.  

Ejemplos de variables:  
- Radio, textura, perímetro y área promedio.  
- Suavidad, compacidad y concavidad.  
- Simetría y dimensión fractal.  

Predicciones posibles:  
- ✅ **Benigno**  
- ⚠️ **Maligno**  

---
## 📂 Estructura del Proyecto

```bash
breast_cancer_project/
📂 .github/
│   └── 📂 workflows/
│       └── ⚙️ ci-cd.yml          # Flujo de trabajo de CI/CD

📂 breast_cancer_app/
│   ├── 📂 model/
│   │   └── 📄 train_model.py     # Script de entrenamiento
│   ├── 📂 api/
│   │   └── 📄 api.py             # API Flask
│   ├── 📂 frontend/
│   │   └── 📄 frontend.py        # Frontend Streamlit

📂 tests/
│   └── 🧪 test_api.py            # Tests automatizados

📂 requirements/
│   ├── 📄 common.txt             # Dependencias comunes
│   ├── 📄 api.txt                # Dependencias de la API
│   ├── 📄 frontend.txt           # Dependencias del Frontend
│   └── 📄 dev.txt                # Dependencias de desarrollo

📂 artifacts/ (automático)
│   ├── 🤖 model.pkl              # Modelo entrenado
│   ├── 📄 feature_info.json      # Info de features
│   ├── 📄 model_metrics.json     # Métricas
│   └── 🖼️ *.png                  # Visualizaciones

📂 docker/
│   ├── 🐳 Dockerfile.api         # Dockerfile de la API
│   ├── 🐳 Dockerfile.frontend    # Dockerfile del Frontend
│   └── ⚙️ docker-compose.yml     # Orquestador de contenedores

⚙️ .dockerignore                  # Archivos a ignorar en Docker
📄 README.md                      # Documentación del proyecto
```
---

## 📦 Instalación y Requisitos

### 🔑 Prerrequisitos
Antes de comenzar, asegúrate de tener instalado:
- 🐍 **Python 3.10+** (probado con 3.11)  
- 📦 **pip** (administrador de paquetes de Python)  
- 🐳 **Docker + Docker Compose** (opcional, para ejecución contenerizada)  
- 🛠️ **Git** (para clonar y gestionar el repositorio)  

---

### ⚙️ Instalación Local

1️⃣ **Clonar el repositorio**
```bash
git clone https://github.com/<tu_usuario>/breast_cancer_project.git
cd breast_cancer_project
```
### 2️⃣ Crear entorno virtual (opcional pero recomendado)
```bash
py -m venv mlops-env            # Instalacion del entorno virtual
mlops-env\Scripts\activate      # Activa el entorno en Windows PowerShell
source mlops-env/bin/activate   # Activa el entorno en Linux/Mac
```
### 3️⃣ Instalar dependencias
```bash
Por separado:  
- `requirements/common.txt` → Librerías comunes para todo el proyecto (ej. pandas, numpy, joblib).  
- `requirements/api.txt` → Librerías necesarias para la API Flask.  
- `requirements/frontend.txt` → Librerías necesarias para el frontend en Streamlit.  

Ejecutar:  
```bash
pip install -r requirements/common.txt
pip install -r requirements/api.txt
pip install -r requirements/frontend.txt

```
## Opción rápida (instala todas las dependencias de una sola vez con dev.txt):
```bash
pip install -r requirements/dev.txt
```
📌 dev.txt incluye en cascada:
```bash
common.txt
   ├─ api.txt
   └─ frontend.txt
```
---

## 🚀 Uso del Sistema

### 🔧 Entrenar el modelo
Si aún no tienes los artefactos (`model.pkl`, métricas, visualizaciones), ejecútalo una vez:
```bash
python train_model.py
```
Esto generará en la carpeta artifacts/:
- 📂 model/ → Modelo entrenado en formato .pkl.
- 📂 info/ → Información de métricas, features y casos de ejemplo.
- 📂 visualizations/ → Gráficas del modelo (matriz de confusión, curva ROC, etc.).

### 2. Ejecutar la API en modo local
```bash
py api/api.py
```
- ✔️ Disponible en: http://127.0.0.1:5000

> ⚠️ **Nota importante:**  
> Este enlace es solo para **verificar que la API está corriendo** y que responde correctamente.  
> La **interfaz interactiva** está en el **frontend (Streamlit)**, descrita más abajo.

Endpoints principales:
- /health → Verificar estado de la API.
- /model/info → Información del modelo y métricas.
- /examples → Casos de ejemplo.
- /predict → Predicción individual (POST JSON).
- /visualizations/<archivo> → Acceder a gráficas generadas.
---

## 🧪 Pruebas Automáticas  
Antes de interactuar con el frontend, se recomienda **probar la API** para corroborar que el servicio responde correctamente.  
```bash
python test_api.py
```
Este script valida:
- ✔️ Respuesta del endpoint raíz / (salud del servicio)
- ✔️ Predicción para casos maligno y benigno
- ✔️ Manejo de errores con JSON inválido

---

### 🎨 Frontend interactivo (Streamlit)
```bash
streamlit run frontend.py
```
- ✔️ Disponible en: http://127.0.0.1:8501

Aquí podrás interactuar con el modelo de manera visual e intuitiva:
- 🎚️ Sliders dinámicos para ajustar las variables del tumor.
- 🟢 Ejemplo Benigno y 🔴 Ejemplo Maligno precargados para probar rápidamente.
- 📊 Resultados visuales con gauge de confianza, curva ROC y matriz de confusión.

> 🌙 Modo oscuro opcional para una experiencia más atractiva.

---

## 🐳 Ejecución con Docker
Para levantar tanto la **API** como el **Frontend** en contenedores, simplemente ejecuta:
```bash
docker-compose up --build
```
Accede a los servicios en tu navegador:
- API → http://localhost:5000
- Frontend → http://localhost:8501

> 📌 Esto asegura que el sistema funcione de forma consistente sin importar el entorno.


---

### ⚙️ CI/CD con GitHub Actions
```markdown
## ⚙️ CI/CD con GitHub Actions

Este proyecto incluye un flujo de **integración continua (CI)** definido en  
`.github/workflows/deploy.yml`.

Cada vez que haces *push* o *pull request* hacia `main`, se ejecuta automáticamente:

1. 📥 **Checkout del repositorio**  
2. 🐍 **Configuración del entorno Python**  
3. 📦 **Instalación de dependencias**  
4. 🧠 **Entrenamiento del modelo (`train_model.py`)**  
5. 🚀 **Ejecución de la API en background**  
6. 🧪 **Pruebas automáticas con Pytest**

✅ Esto garantiza que el código esté siempre probado y listo para usarse.  

--- 

## ✍️ Autoría  

📌 Este proyecto corresponde a la **Evaluación Modular** del programa **Talento Digital – Kibernum**.  

- 👤 **Autor:** Fredy Geraldo Rivera  