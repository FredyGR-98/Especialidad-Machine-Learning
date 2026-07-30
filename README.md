# Breast Cancer MLOps Platform

![CI](https://github.com/FredyGR-98/detector-cancer-mama-mlops/actions/workflows/deploy.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.11-blue.svg)
![Docker](https://img.shields.io/badge/docker-ready-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

Plataforma demostrativa orientada a prediccion clinica, registro de evaluaciones y analitica aplicada para cancer de mama. El proyecto integra un modelo de machine learning entrenado con variables morfologicas, una API Flask para inferencia, una interfaz en Streamlit para uso operativo y una capa de visualizacion en Power BI conectada a SQLite como fuente persistente.

Este repositorio fue reorganizado para presentarse como una pieza de portafolio tecnico en analisis de datos, machine learning aplicado y MLOps. No corresponde a un sistema medico validado ni debe utilizarse para diagnostico real.

## Resumen ejecutivo

El caso parte del dataset `Wisconsin Breast Cancer Diagnostic` y lo transforma en una solucion end-to-end con cuatro capas:

- entrenamiento y serializacion del modelo
- servicio de prediccion mediante API REST
- captura y seguimiento de registros clinicos en una interfaz Streamlit
- visualizacion ejecutiva de la informacion historica en Power BI

La aplicacion permite simular un flujo realista donde un usuario registra un caso, ejecuta una prediccion, guarda el resultado en SQLite y luego analiza el comportamiento agregado de los casos desde un dashboard externo.

## Problema abordado

El objetivo del proyecto es demostrar como un problema clasico de clasificacion binaria puede escalarse a una solucion mas cercana a un entorno aplicado. En lugar de quedarse en un notebook o en un script de entrenamiento, el repositorio busca responder tres preguntas practicas:

- como exponer el modelo para ser consumido por una interfaz
- como persistir las predicciones y generar historial clinico
- como reutilizar esos registros para una capa de analitica y monitoreo

## Solucion propuesta

La plataforma se apoya en 30 variables clinicas numericas derivadas de mediciones celulares. El modelo clasifica cada caso como `Benign` o `Malignant`, devuelve probabilidades por clase y almacena el resultado junto con los datos del paciente y la fecha de evaluacion.

Sobre esa base se construyeron dos experiencias complementarias:

- un predictor clinico en Streamlit para el ingreso de pacientes, comparacion de controles y ejecucion de nuevas predicciones
- un dashboard en Power BI orientado a lectura ejecutiva, segmentacion por edad, seguimiento temporal y analisis visual de los diagnosticos registrados

## Arquitectura del proyecto

```text
Frontend Streamlit
        |
        v
API Flask /predict-and-save
        |
        v
SQLite (patients, clinical_measurements, system_users)
        |
        +--> Power BI Dashboard
        |
        +--> Scripts de carga sintetica

Modelo entrenado -> artifacts/model/model.pkl
Metricas y visualizaciones -> artifacts/info + artifacts/visualizations
```

Flujo principal:

1. `model/train_model.py` entrena el modelo y genera artefactos.
2. `api/api.py` carga el modelo y expone endpoints de prediccion.
3. `frontend/app.py` consume la API y permite registrar casos.
4. `database/breast_cancer_clinical.db` almacena pacientes y evaluaciones.
5. `powerbi/breast_cancer_dashboard.pbix` consume la base SQLite por ODBC para construir la lectura ejecutiva.

## Stack tecnico

- Python 3.11
- scikit-learn
- pandas
- Flask
- Streamlit
- SQLite
- Power BI
- Docker
- pytest
- GitHub Actions

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

## Experiencia del proyecto

### Predictor clinico

La interfaz Streamlit fue reorganizada para presentar el caso de forma mas profesional y menos academica. Actualmente incluye:

- pantalla inicial con contexto del problema
- vista de analisis del modelo y sus metricas
- modulo de pacientes con historial y nuevos controles
- KPI visual de riesgo en la prediccion
- persistencia del resultado en SQLite

Espacio para video demostrativo del predictor:

`[Agregar video o GIF del flujo de prediccion en Streamlit]`

### Dashboard clinico en Power BI

El dashboard se conecto a SQLite mediante ODBC para leer la misma base que alimenta la aplicacion. La vista ejecutiva actual resume:

- distribucion de diagnosticos estimados
- evolucion mensual de evaluaciones clinicas
- casos detectados por grupo etario
- relacion entre radio medio y textura media por diagnostico
- concentracion de evaluaciones por grupo etario
- mapa de calor por edad y clasificacion

Espacio para video demostrativo del dashboard:

`[Agregar video o GIF de navegacion del dashboard en Power BI]`

## Fuente de datos

El caso utiliza el dataset `Wisconsin Breast Cancer Diagnostic`, disponible en `sklearn.datasets.load_breast_cancer`. El conjunto original contiene 569 registros y 30 atributos numericos relacionados con:

- tamano y geometria del tumor
- textura y superficie
- forma e irregularidad
- medidas promedio, error estandar y peor valor observado

Sobre ese dataset base se construyo una capa de persistencia clinica local para simular historial de pacientes, controles repetidos y consumo posterior desde un dashboard.

## Estructura del repositorio

```text
breast-cancer-mlops/
├── .github/
│   └── workflows/
│       └── deploy.yml
├── api/
│   └── api.py
├── artifacts/
│   ├── info/
│   ├── model/
│   └── visualizations/
├── database/
│   ├── breast_cancer_clinical.db
│   ├── db_manager.py
│   ├── schema.sql
│   └── seed_data.sql
├── docker/
│   ├── docker-compose.yml
│   ├── Dockerfile.api
│   └── Dockerfile.frontend
├── frontend/
│   ├── app.py
│   ├── components/
│   ├── services/
│   ├── utils/
│   └── views/
├── model/
│   └── train_model.py
├── powerbi/
│   ├── breast_cancer_dashboard.pbix
│   └── dashboard_redesign_plan.md
├── requirements/
│   ├── api.txt
│   ├── common.txt
│   ├── dev.txt
│   └── frontend.txt
├── scripts/
│   ├── init_db.py
│   └── seed_demo_patients.py
├── tests/
│   └── test_api.py
└── README.md
```

## Instalacion local

```bash
git clone https://github.com/<tu-usuario>/breast-cancer-mlops.git
cd breast-cancer-mlops
py -m venv .venv
.venv\Scripts\activate
pip install -r requirements/dev.txt
```

## Ejecucion local

### 1. Entrenar el modelo

```bash
python model/train_model.py
```

Esto regenera:

- `artifacts/model/model.pkl`
- `artifacts/info/model_metrics.json`
- `artifacts/info/feature_info.json`
- visualizaciones en `artifacts/visualizations/`

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

## Dashboard en Power BI

El archivo del dashboard se encuentra en:

- [breast_cancer_dashboard.pbix](C:\Users\fredy\Desktop\Talento Digital\Modulo 10\Evaluacion Modular\breast-cancer-mlops\powerbi\breast_cancer_dashboard.pbix)

Para conectarlo a la base SQLite:

1. Instalar un driver ODBC para SQLite.
2. Crear un DSN apuntando a:
   - [breast_cancer_clinical.db](C:\Users\fredy\Desktop\Talento Digital\Modulo 10\Evaluacion Modular\breast-cancer-mlops\database\breast_cancer_clinical.db)
3. Abrir el `.pbix`.
4. Actualizar el modelo desde Power BI.

Esto permite que el dashboard lea directamente los registros almacenados por la app y por los scripts de carga sintetica.

## Endpoints principales

- `GET /health`
- `GET /model/info`
- `GET /examples`
- `POST /predict`
- `POST /predict-and-save`
- `POST /predict/batch`
- `POST /login`
- `GET /patients`

## Pruebas

```bash
python -m pytest -v tests/
```

Cobertura actual enfocada en:

- disponibilidad de endpoints
- validacion de payloads
- respuesta de prediccion
- contrato base de la API

## CI

El workflow `.github/workflows/deploy.yml` ejecuta:

1. instalacion de dependencias
2. entrenamiento del modelo
3. inicializacion de la base
4. ejecucion de pruebas automatizadas

## Valor como proyecto de portafolio

Este proyecto busca mostrar capacidad para:

- transformar un modelo supervisado en una solucion utilizable
- disenar una interfaz de consumo con narrativa de negocio
- persistir y reutilizar predicciones en una base de datos
- conectar una capa operativa con una capa analitica
- organizar un repositorio con foco en reproducibilidad y presentacion profesional

## Limitaciones

- el dataset clinico original es de uso academico y no representa operacion hospitalaria real
- la autenticacion es demostrativa
- los registros persistidos en SQLite son simulados para fines de visualizacion y testing
- no existe validacion clinica ni aprobacion para uso medico

## Proximas mejoras sugeridas

- agregar comparacion formal entre varios modelos
- incorporar versionado de artefactos y trazabilidad de entrenamiento
- ampliar pruebas de integracion entre frontend, API y base de datos
- documentar el EDA en un notebook o reporte separado
- publicar videos demo del predictor y del dashboard

## Autor

Fredy Geraldo Rivera

Proyecto desarrollado inicialmente como evaluacion modular y luego refactorizado para elevar su calidad tecnica, claridad narrativa y valor de portafolio.
