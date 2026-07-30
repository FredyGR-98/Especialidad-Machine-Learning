# Breast Cancer MLOps Platform

![CI](https://github.com/FredyGR-98/detector-cancer-mama-mlops/actions/workflows/deploy.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.11-blue.svg)
![Docker](https://img.shields.io/badge/docker-ready-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

Plataforma demostrativa orientada a la prediccion de cancer de mama a partir de variables clinicas, con foco en determinar si un tumor presenta un comportamiento `Benigno` o `Maligno`. El proyecto integra entrenamiento de modelo, API Flask, interfaz en Streamlit, persistencia en SQLite y visualizacion ejecutiva en Power BI.

Este repositorio fue reorganizado para presentarse como una pieza de portafolio tecnico en analisis de datos, machine learning aplicado y MLOps. No corresponde a un sistema medico validado ni debe utilizarse para diagnostico clinico real.

## A considerar

El proyecto fue construido para simular un flujo de trabajo mas cercano a un entorno aplicado que a un ejercicio aislado de modelado:

- el modelo recibe 30 variables clinicas y predice si el caso corresponde a un tumor benigno o maligno
- la prediccion puede registrarse junto con los datos del paciente y la fecha de evaluacion
- la informacion se almacena en una base de datos local `SQLite`
- el dashboard en Power BI se conecta a esa base mediante `ODBC` para reutilizar los registros historicos

En conjunto, el caso permite mostrar una cadena completa de trabajo entre inferencia, persistencia y analitica.

## Problema y respuesta del proyecto

| Problema detectado | Respuesta implementada |
| --- | --- |
| Un modelo de clasificacion por si solo no refleja un caso aplicado | Se construyo un predictor con API e interfaz para simular uso operativo |
| Las predicciones se perderian si no existiera persistencia | Se incorporo una base SQLite para registrar pacientes y evaluaciones |
| Un modelo sin seguimiento historico aporta poco a nivel ejecutivo | Se conecto Power BI a la base local por ODBC para analizar los registros |
| Un proyecto academico suele verse desconectado de una capa de consumo | Se integraron frontend, API, base de datos y dashboard en un mismo flujo |

## Stack tecnico

- Python 3.11
- scikit-learn
- pandas
- Flask
- Streamlit
- SQLite
- Power BI
- Docker

## Resultados del modelo

Metricas generadas a partir del entrenamiento actual:

- Accuracy: `94.74%`
- F1-score: `95.83%`
- ROC AUC: `0.9937`

Modelo actual:

- algoritmo: `Random Forest Classifier`
- tipo de problema: clasificacion binaria
- clases estimadas: `Malignant` y `Benign`
- variables de entrada: `30`

## Estructura del repositorio

```text
breast-cancer-mlops/
├── .github/                  # workflow de integracion continua
├── api/                      # API Flask para prediccion y persistencia
├── artifacts/                # modelo entrenado, metricas y visualizaciones
├── database/                 # base SQLite, esquema y gestor de acceso
├── docker/                   # archivos para ejecucion contenerizada
├── frontend/                 # aplicacion Streamlit y vistas del sistema
├── model/                    # script de entrenamiento del modelo
├── powerbi/                  # dashboard PBIX y notas de rediseño
├── requirements/             # dependencias separadas por capa
├── scripts/                  # inicializacion de base y carga sintetica
├── tests/                    # pruebas automatizadas principales
└── README.md                 # documentacion del proyecto
```

## Experiencia del proyecto

### Predictor clinico

La interfaz Streamlit fue reorganizada para presentar el proyecto como una solucion demostrativa mas profesional. Actualmente incluye:

- vista inicial con contexto del caso
- analisis del modelo y lectura de metricas
- modulo de pacientes con historial de controles
- formulario de nueva evaluacion y prediccion
- persistencia del resultado en SQLite

Nota:
El predictor se apoya en el dataset `Wisconsin Breast Cancer Diagnostic` como base para el entrenamiento del modelo y en registros sinteticos almacenados en SQLite para simular un historial clinico reutilizable.

Espacio para video demostrativo del predictor:

`[Agregar video o GIF del flujo de prediccion en Streamlit]`

### Dashboard clinico en Power BI

El dashboard consume la misma base SQLite que alimenta la aplicacion y se conecta de forma local mediante ODBC. La vista actual resume:

- distribucion de diagnosticos estimados
- evolucion mensual de evaluaciones clinicas
- casos detectados por grupo etario
- relacion entre radio medio y textura media por diagnostico
- concentracion de evaluaciones por grupo etario
- mapa de calor por edad y clasificacion

Espacio para video demostrativo del dashboard:

`[Agregar video o GIF de navegacion del dashboard en Power BI]`

## Instalacion local

```bash
git clone https://github.com/FredyGR-98/detector-cancer-mama-mlops.git
cd breast-cancer-mlops
py -m venv .venv
.venv\Scripts\activate
pip install -r requirements/dev.txt
```

En GitHub Markdown no existen tabs nativos como en una documentacion web, pero si puedes simular una separacion limpia usando bloques desplegables. Por eso el flujo se divide asi:

<details>
<summary><strong>Flujo 1: predictor local</strong></summary>

### 1. Entrenar el modelo

```bash
python model/train_model.py
```

### 2. Inicializar la base de datos

```bash
python scripts/init_db.py
```

### 3. Poblar la base con datos sinteticos

Carga base:

```bash
.\mlops-env\Scripts\python.exe scripts\seed_demo_patients.py
```

Carga ampliada para historico entre 2020 y 2026:

```bash
.\mlops-env\Scripts\python.exe scripts\seed_demo_patients.py --patients 54 --evaluations 4 --start-year 2020 --end-year 2026
```

Carga enfocada en un tramo etario especifico:

```bash
.\mlops-env\Scripts\python.exe scripts\seed_demo_patients.py --patients 20 --evaluations 3 --start-year 2020 --end-year 2026 --min-age 18 --max-age 29
```

### 4. Levantar la API

```bash
python api/api.py
```

API disponible en:

- `http://127.0.0.1:5000`

### 5. Levantar el frontend

```bash
streamlit run frontend/app.py
```

Frontend disponible en:

- `http://127.0.0.1:8501`

</details>

<details>
<summary><strong>Flujo 2: dashboard local en Power BI</strong></summary>

### 1. Instalar un driver ODBC para SQLite

Referencia de descarga:

- [SQLite ODBC Driver](https://www.ch-werner.de/sqliteodbc/)

### 2. Crear un DSN apuntando a la base local

Archivo de base utilizado por el proyecto:

- [breast_cancer_clinical.db](C:\Users\fredy\Desktop\Talento Digital\Modulo 10\Evaluacion Modular\breast-cancer-mlops\database\breast_cancer_clinical.db)

### 3. Abrir el dashboard

Archivo del dashboard:

- [breast_cancer_dashboard.pbix](C:\Users\fredy\Desktop\Talento Digital\Modulo 10\Evaluacion Modular\breast-cancer-mlops\powerbi\breast_cancer_dashboard.pbix)

### 4. Actualizar el modelo en Power BI

Con esto el dashboard deberia leer los nuevos registros guardados por la app y por los scripts de carga sintetica.

</details>

## Endpoints principales

- `GET /health`
- `GET /model/info`
- `GET /examples`
- `POST /predict`
- `POST /predict-and-save`
- `POST /predict/batch`
- `POST /login`
- `GET /patients`

## Autor

Fredy Geraldo Rivera

Proyecto desarrollado para simular un entorno de trabajo mas realista, conectando un modelo de clasificacion de cancer de mama con una capa de prediccion, persistencia local y visualizacion analitica orientada a portafolio.
