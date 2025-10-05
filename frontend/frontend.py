"""
===========================================================
📌 frontend.py — Interfaz en Streamlit
===========================================================

Este frontend consume la API Flask (api.py) y permite:
- Ver información general del proyecto
- Realizar predicciones (sliders y casos precargados)
- Visualizar métricas y gráficos del modelo

⚠️ IMPORTANTE:
Este proyecto es con fines EDUCATIVOS y no constituye diagnóstico médico.
===========================================================
"""
import os
import sys
from pathlib import Path
from typing import List

import requests
import streamlit as st
import plotly.graph_objects as go
import pandas as pd

# --- Paths / Imports opcionales ---
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

# FEATURE_TRANSLATIONS opcional
try:
    from utils.feature_names import FEATURE_TRANSLATIONS
except Exception:
    FEATURE_TRANSLATIONS = {}

# === Configuración ===
API_URL = os.environ.get("API_URL", "http://localhost:5000").rstrip("/")
st.set_page_config(page_title="Clasificador Cáncer de Mama", page_icon="🎀", layout="wide")

# === Estado global ===
if "dark_mode" not in st.session_state:
    st.session_state["dark_mode"] = False
if "active_page" not in st.session_state:
    st.session_state["active_page"] = "🏠 Contexto + EDA"
if "inputs" not in st.session_state:
    st.session_state["inputs"] = {}

# === Sidebar: navegación + modo ===
st.sidebar.markdown("## 📌 Navegación")
page = st.sidebar.radio(
    "Ir a:",
    ["🏠 Contexto + EDA", "⚙️ Modelo y Rendimiento", "🔮 Caso Práctico"],
    index=["🏠 Contexto + EDA", "⚙️ Modelo y Rendimiento", "🔮 Caso Práctico"].index(st.session_state["active_page"])
)
st.session_state["active_page"] = page

st.sidebar.markdown("---")
st.session_state["dark_mode"] = st.sidebar.toggle("🌙 Modo oscuro", value=st.session_state["dark_mode"])

# === CSS dinámico (light/dark) ===
if st.session_state["dark_mode"]:
    st.markdown("""
    <style>
    body { background-color: #121212; color: #f0f0f0; }
    .metric-card {
        background: #1e1e1e; padding: 1rem; border-radius: 10px;
        border-left: 5px solid #ec4899; margin: 0.5rem 0; color: #f0f0f0;
    }
    .success-box {
        background: #1b3c1b; padding: 1rem; border-radius: 10px;
        border: 1px solid #28a745; margin: 1rem 0; color: #d4edda;
    }
    .error-box {
        background: #3c1b1b; padding: 1rem; border-radius: 10px;
        border: 1px solid #f5c6cb; margin: 1rem 0; color: #f8d7da;
    }
    </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <style>
    body { background-color: #ffffff; color: #111111; }
    .metric-card {
        background: #f9f9f9; padding: 1rem; border-radius: 10px;
        border-left: 5px solid #ec4899; margin: 0.5rem 0; color: #111111;
    }
    .success-box {
        background: #d4edda; padding: 1rem; border-radius: 10px;
        border: 1px solid #28a745; margin: 1rem 0; color: #111111;
    }
    .error-box {
        background: #f8d7da; padding: 1rem; border-radius: 10px;
        border: 1px solid #721c24; margin: 1rem 0; color: #111111;
    }
    </style>
    """, unsafe_allow_html=True)

# === Utilidades de API ===
@st.cache_data(ttl=600, show_spinner=False)
def get_model_info():
    try:
        r = requests.get(f"{API_URL}/model/info", timeout=8)
        return r.json() if r.ok else None
    except Exception:
        return None

@st.cache_data(ttl=600, show_spinner=False)
def get_examples():
    try:
        r = requests.get(f"{API_URL}/examples", timeout=8)
        return r.json() if r.ok else {}
    except Exception:
        return {}

def predict_single(payload: dict):
    try:
        r = requests.post(f"{API_URL}/predict", json=payload, timeout=12)
        return r.ok, r.json()
    except Exception as e:
        return False, {"error": str(e)}

def viz_url(name: str) -> str:
    # Para endpoints normales, usa API_URL
    base = API_URL

    # Si estamos sirviendo imágenes, usar localhost (accesible desde el navegador)
    if "visualizations" in name or name.endswith(".png"):
        base = "http://localhost:5000"

    return f"{base}/visualizations/{name}"

# === Helper para imágenes con tema ===
def themed_viz(name: str) -> str:
    theme = "dark" if st.session_state["dark_mode"] else "light"
    return viz_url(f"{name}_{theme}.png")

# === Helpers de UI ===
def feature_display_name(f: str) -> str:
    return FEATURE_TRANSLATIONS.get(f, f.replace("mean ", "").replace("_", " ").title())

def to_table_3x10(features: List[str]) -> pd.DataFrame:
    disp = [feature_display_name(f) for f in features]
    while len(disp) % 3 != 0:
        disp.append("")
    rows = len(disp) // 3
    data = {"Columna 1": disp[0:rows], "Columna 2": disp[rows:2*rows], "Columna 3": disp[2*rows:3*rows]}
    return pd.DataFrame(data)

def gauge_confidence(value_pct: float, benign: bool) -> go.Figure:
    if st.session_state["dark_mode"]:
        color = "#39FF14" if benign else "#FF1493"  # neon
    else:
        color = "#00cc96" if benign else "#ff6b6b"  # pastel
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value_pct,
        title={'text': "Confianza (%)", 'font': {'size': 20}},
        gauge={'axis': {'range': [0, 100]}, 'bar': {'color': color, 'thickness': 0.3}}
    ))
    fig.update_layout(height=250, margin=dict(l=20, r=20, t=50, b=20))
    return fig

# === CONTEXTO + DATASET ===
if page == "🏠 Contexto + EDA":
    # --- Solo el título en bloque destacado ---
    st.markdown("""
    <div class="metric-card" style="
        padding: 1.2em;
        border-radius: 12px;
        margin-bottom: 1.5em;
        border-left: 6px solid #e83e8c;
    ">
        <h1 style="margin: 0; font-size: 2em; color: inherit;">
            🏠 Caso de Estudio: Cáncer de Mama (Dataset WBCD)
        </h1>
    </div>
    """, unsafe_allow_html=True)

    # --- Texto narrativo normal (como Interpretación) ---
    st.markdown("""
    💗 El **cáncer de mama** es una de las principales causas de morbilidad en mujeres a nivel mundial.  
    La **detección temprana** aumenta considerablemente las probabilidades de un tratamiento exitoso y la posibilidad de salvar vidas.  
    """)

    # --- Bloque dataset ---
    info = get_model_info()
    if info:
        st.markdown("## 📊 Sobre el Dataset")
        st.write("Utilizamos el **Wisconsin Breast Cancer (Diagnostic)** con un total de **569 muestras**:")

        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("Total de muestras", "569")
        with c2:
            st.metric("Benignos", "357")
        with c3:
            st.metric("Malignos", "212")

    # --- Tabla de variables agrupadas por tipo ---
    st.subheader("📋 Variables del dataset (agrupadas por tipo)")

    grouped_data = {
        "Promedios (mean)": [
            "Radio promedio", "Textura promedio", "Perímetro promedio", "Área promedio",
            "Suavidad promedio", "Compacidad promedio", "Concavidad promedio",
            "Puntos cóncavos promedio", "Simetría promedio", "Dimensión fractal promedio"
        ],
        "Error estándar (se)": [
            "Error en radio", "Error en textura", "Error en perímetro", "Error en área",
            "Error en suavidad", "Error en compacidad", "Error en concavidad",
            "Error en puntos cóncavos", "Error en simetría", "Error en dimensión fractal"
        ],
        "Peor caso (worst)": [
            "Radio peor caso", "Textura peor caso", "Perímetro peor caso", "Área peor caso",
            "Suavidad peor caso", "Compacidad peor caso", "Concavidad peor caso",
            "Puntos cóncavos peor caso", "Simetría peor caso", "Dimensión fractal peor caso"
        ]
    }

    df_grouped = pd.DataFrame(grouped_data)
    st.dataframe(df_grouped, use_container_width=True, hide_index=True)

    st.markdown("""
    📌 **Interpretación**  
    - Los valores **promedio (mean)** permiten caracterizar el comportamiento típico de cada célula.  
    - Los valores de **error estándar (se)** indican la variabilidad en la medición.  
    - Los valores de **peor caso (worst)** representan el escenario más extremo observado en la muestra.  

    Esto facilita distinguir tumores malignos (más irregulares, con mayor concavidad y área) de los benignos (más uniformes y suaves).
    """)

    # --- Mini EDA ---
    st.markdown("---")
    st.subheader("🔬 Mini EDA (visión general)")
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("**🔗 Matriz de correlación**")
        st.image(themed_viz("correlation_matrix"),
                 caption="Relación entre variables (Pearson)",
                 use_column_width=True)
    with col_b:
        st.markdown("**🔑 Top 10 variables más relevantes**")
        st.image(themed_viz("feature_importance"),
                 caption="Importancia de características (Top 10)",
                 use_column_width=True)

    # --- Descargo en tarjeta ---
    st.markdown("""
    <div class="metric-card">
        <strong>⚠️ Descargo:</strong> Este proyecto es con fines <em>educativos</em>.  
        No constituye diagnóstico médico ni reemplaza la evaluación de un profesional de la salud.
    </div>
    """, unsafe_allow_html=True)

# 2) MODELO Y RENDIMIENTO
elif page == "⚙️ Modelo y Rendimiento":
    st.title("⚙️ Modelo y Rendimiento")
    st.markdown("""
    🤖 **Algoritmo:** Random Forest.  
    🎯 **Objetivo:** clasificar tumores en **benignos** o **malignos**.
    """)

    info = get_model_info()
    if info and "metrics" in info:
        m = info["metrics"]
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("Accuracy (test)", f"{m.get('accuracy', 0): .2%}")
        with c2:
            st.metric("F1-Score", f"{m.get('f1_score', 0): .2%}")
        with c3:
            st.metric("ROC-AUC", f"{m.get('roc_auc', 0): .3f}")

        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**📊 Matriz de Confusión**")
            st.image(themed_viz("confusion_matrix"), use_column_width=True)
        with col2:
            st.markdown("**📈 Curva ROC**")
            st.image(themed_viz("roc_curve"), use_column_width=True)

        # --- Bloque de interpretación (adaptado a light/dark) ---
        st.markdown("""
        <div class="metric-card">
            <strong>📝 Interpretación de Resultados</strong><br><br>
            El modelo entrenado logra distinguir con gran precisión entre <b>tumores benignos</b> y <b>malignos</b>:<br><br>
            🔹 <b>39 casos</b> fueron clasificados correctamente como <b>benignos</b> (verdaderos positivos).<br>
            🔹 <b>69 casos</b> fueron clasificados correctamente como <b>malignos</b> (verdaderos negativos).<br>
            🔹 Solo se observaron <b>6 errores en total</b> (3 benignos predichos como malignos y 3 malignos predichos como benignos).<br><br>
            📊 La <b>Curva ROC</b> confirma este rendimiento: el área bajo la curva (<b>AUC = 0.994</b>) refleja una capacidad predictiva sobresaliente, cercana al 100%.<br><br>
            ✅ En conclusión, el modelo es altamente confiable para identificar casos de cáncer de mama, aunque —como todo modelo— no está exento de un pequeño margen de error.
        </div>
        """, unsafe_allow_html=True)


# 3) CASO PRÁCTICO
elif page == "🔮 Caso Práctico":
    st.title("🔮 Caso Práctico de Análisis")

    examples = get_examples()
    col_p1, col_p2 = st.columns(2)
    if col_p1.button("🟢 Cargar ejemplo Benigno"):
        st.session_state["inputs"] = examples.get("benign_case", {})
    if col_p2.button("🔴 Cargar ejemplo Maligno"):
        st.session_state["inputs"] = examples.get("malignant_case", {})

    st.markdown("---")
    st.subheader("🎛️ Ajusta manualmente las variables")
    info = get_model_info()
    if info:
        features = info.get("features", [])
        with st.form("form_prediccion"):
            cols = st.columns(3)
            inputs = {}
            for i, f in enumerate(features):
                label = feature_display_name(f)
                default_val = float(st.session_state["inputs"].get(f, 10.0))
                col = cols[i % 3]
                with col:
                    inputs[f] = st.slider(label, min_value=0.0, max_value=30.0,
                                          value=default_val, step=0.1, key=f"slider_{f}")

            submitted = st.form_submit_button("🔍 Predecir")
            if submitted:
                st.session_state["inputs"] = inputs
                ok, result = predict_single(inputs)
                st.markdown("---")
                st.subheader("📋 Resultado")

                if not ok:
                    st.error(f"Error en la predicción: {result.get('error', 'desconocido')}")
                else:
                    pred = result.get("prediction", 0)
                    proba = result.get("probability", [0, 0])
                    conf_pct = max(proba) * 100 if proba else 0.0

                    if pred == 0:
                        st.markdown('<div class="success-box"><h3>✅ Tumor Benigno</h3></div>', unsafe_allow_html=True)
                        st.plotly_chart(gauge_confidence(conf_pct, benign=True), use_container_width=True)
                    else:
                        st.markdown('<div class="error-box"><h3>⚠️ Tumor Maligno</h3></div>', unsafe_allow_html=True)
                        st.plotly_chart(gauge_confidence(conf_pct, benign=False), use_container_width=True)

                    # Barra comparativa de probabilidades
                    try:
                        p0 = float(proba[0]) * 100
                        p1 = float(proba[1]) * 100
                        if st.session_state["dark_mode"]:
                            bar_colors = ['#39FF14', '#FF1493']  # neon
                        else:
                            bar_colors = ['#51cf66', '#ff6b6b']  # pastel
                        bar = go.Figure(go.Bar(x=["Benigno", "Maligno"], y=[p0, p1],
                                               marker_color=bar_colors))
                        bar.update_layout(height=260, margin=dict(l=20, r=20, t=30, b=40),
                                          yaxis_title="Probabilidad (%)")
                        st.plotly_chart(bar, use_container_width=True)
                    except Exception:
                        pass

    st.markdown("---")
    st.markdown("""
    <div class="metric-card">
        <strong>⚠️ Nota:</strong> Esta predicción es educativa. 
        Para cualquier caso real, consulta siempre a un profesional médico.
    </div>
    """, unsafe_allow_html=True)

# === Footer ===
st.markdown("---")
f1, f2, f3 = st.columns(3)
with f1: st.caption("📊 Dataset: Wisconsin Breast Cancer (UCI)")
with f2: st.caption("🤖 Modelo: Random Forest")
with f3: st.caption("🎀 Proyecto educativo de apoyo")