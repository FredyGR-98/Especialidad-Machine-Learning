# Breast Cancer MLOps Platform

![CI](https://github.com/FredyGR-98/detector-cancer-mama-mlops/actions/workflows/deploy.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.11-blue.svg)
![Docker](https://img.shields.io/badge/docker-ready-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![scikit-learn](https://img.shields.io/badge/scikit--learn-model-orange.svg)
![Flask](https://img.shields.io/badge/flask-api-black.svg)
![Streamlit](https://img.shields.io/badge/streamlit-frontend-red.svg)
![SQLite](https://img.shields.io/badge/sqlite-local_db-003B57.svg)
![Power BI](https://img.shields.io/badge/power_bi-dashboard-F2C811.svg)

Plataforma demostrativa orientada a la prediccion de cancer de mama a partir de variables clinicas, con foco en estimar si un tumor presenta un comportamiento `Benigno` o `Maligno`. El proyecto integra entrenamiento de modelo, API Flask, interfaz en Streamlit, persistencia en SQLite y visualizacion ejecutiva en Power BI.

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

## Resultados del modelo

| Indicador | Valor |
| --- | --- |
| Accuracy | `94.74%` |
| F1-score | `95.83%` |
| ROC AUC | `0.9937` |
| Algoritmo | `Random Forest Classifier` |
| Tipo de problema | `Clasificacion binaria` |
| Clases estimadas | `Malignant` / `Benign` |
| Variables de entrada | `30` |

## Estructura del repositorio

```text
📦 breast-cancer-mlops
├── 📁 .github
│   └── 📁 workflows
│       └── deploy.yml                    # Pipeline de validacion
├── 📁 api
│   └── api.py                            # API Flask para prediccion y guardado
├── 📁 artifacts
│   ├── 📁 info
│   │   ├── example_cases.json            # Casos de ejemplo
│   │   ├── feature_info.json             # Metadata del modelo
│   │   └── model_metrics.json            # Metricas exportadas
│   ├── 📁 model
│   │   └── model.pkl                     # Modelo serializado
│   └── 📁 visualizations
│       ├── confusion_matrix.png          # Matriz de confusion
│       ├── correlation_matrix.png        # Correlaciones del entrenamiento
│       ├── feature_importance.png        # Variables mas influyentes
│       └── roc_curve.png                 # Curva ROC
├── 📁 database
│   ├── breast_cancer_clinical.db         # Base SQLite principal
│   ├── db_manager.py                     # Acceso a datos
│   ├── schema.sql                        # Estructura inicial
│   └── seed_data.sql                     # Datos base
├── 📁 docker                             # Archivos de contenedorizacion
├── 📁 frontend
│   ├── 📁 components                     # Componentes visuales reutilizables
│   ├── 📁 services                       # Consumo de API
│   ├── 📁 utils                          # Helpers, tema y configuracion
│   ├── 📁 views                          # Vistas principales del sistema
│   └── app.py                            # Punto de entrada de Streamlit
├── 📁 model
│   └── train_model.py                    # Entrenamiento del clasificador
├── 📁 powerbi
│   ├── breast_cancer_dashboard.pbix      # Dashboard local en Power BI
│   └── dashboard_redesign_plan.md        # Notas de rediseño
├── 📁 requirements                       # Dependencias por entorno
├── 📁 scripts
│   ├── init_db.py                        # Inicializacion de la base
│   └── seed_demo_patients.py             # Carga de pacientes sinteticos
├── 📁 tests
│   └── test_api.py                       # Validaciones principales
└── README.md                             # Documentacion del proyecto
```

## Experiencia del proyecto

### Predictor clinico

La interfaz Streamlit fue reorganizada para presentar el proyecto como una solucion demostrativa mas profesional. Actualmente incluye:

- vista inicial con contexto del caso
- analisis del modelo y lectura de metricas
- modulo de pacientes con historial de controles
- formulario de nueva evaluacion y prediccion
- persistencia del resultado en SQLite

> Nota
> El predictor se apoya en el dataset `Wisconsin Breast Cancer Diagnostic` como base de entrenamiento y en registros sinteticos persistidos en `SQLite` para simular un historial clinico reutilizable.

Video demostrativo del predictor:

- [Ver demostracion del predictor clinico de cancer de mama](https://youtu.be/kQWZsZmppgw)

### Dashboard clinico en Power BI

El dashboard consume la misma base SQLite que alimenta la aplicacion y se conecta de forma local mediante ODBC. La vista actual resume:

- distribucion de diagnosticos estimados
- evolucion mensual de evaluaciones clinicas
- casos detectados por grupo etario
- relacion entre radio medio y textura media por diagnostico
- concentracion de evaluaciones por grupo etario
- mapa de calor por edad y clasificacion

Video demostrativo del dashboard:

- [Ver demostracion del dashboard clinico en Power BI](https://youtu.be/xWs-Tn3vvto)

## Instalacion local

```bash
git clone https://github.com/FredyGR-98/detector-cancer-mama-mlops.git
cd breast-cancer-mlops
py -m venv .venv
.venv\Scripts\activate
pip install -r requirements/dev.txt
```

Para mantener una lectura mas ordenada, los pasos se separan entre el flujo del predictor local y la conexion del dashboard.

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

`GET /health` `GET /model/info` `GET /examples` `POST /predict` `POST /predict-and-save` `POST /predict/batch` `POST /login` `GET /patients`

## Autor

Fredy Geraldo Rivera

Proyecto desarrollado para simular un entorno de trabajo mas realista, conectando un modelo de clasificacion de cancer de mama con una capa de prediccion, persistencia local y visualizacion analitica orientada a portafolio.
