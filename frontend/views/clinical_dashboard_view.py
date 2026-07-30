"""
Vista de análisis exploratorio clínico.
Presenta una lectura descriptiva de los registros clínicos almacenados
en la base de datos, complementando el dashboard ejecutivo en Power BI.
"""

from __future__ import annotations

from dataclasses import dataclass
from html import escape
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

from utils.theme import APP_THEME


@dataclass
class DashboardColors:
    """
    Paleta visual inspirada en la temática de cáncer de mama.
    """
    primary: str = APP_THEME["primary"]
    primary_dark: str = APP_THEME["primary_dark"]
    benign: str = APP_THEME["class_benign"]
    malignant: str = APP_THEME["class_malignant"]
    soft_bg: str = APP_THEME["surface_alt"]
    border: str = APP_THEME["border"]
    text: str = APP_THEME["text"]


class ClinicalDashboardView:
    """
    Renderiza la sección de análisis exploratorio clínico.
    """

    def __init__(self, api_client) -> None:
        self.api_client = api_client
        self.colors = DashboardColors()
        self.base_dir = Path(__file__).resolve().parents[2]
        self.power_bi_path = self.base_dir / "powerbi" / "breast_cancer_dashboard.pbix"

    def render(self) -> None:
        """
        Renderiza el contenido visual de la vista.
        """
        self._inject_css()
        st.title("Dashboard Clínico")

        st.markdown(
            """
            <div class="info-banner">
                Esta vista quedó enfocada en una lectura clínica rápida. Aquí solo se
                comparan variables clave entre casos benignos y malignos mediante boxplots,
                mientras que el análisis ejecutivo completo se consulta en el dashboard externo.
            </div>
            """,
            unsafe_allow_html=True,
        )

        df = self._load_dashboard_data()

        if df.empty:
            st.info("No hay datos clínicos disponibles para construir la vista.")
            return

        df = self._prepare_dataframe(df)

        if df.empty:
            st.warning("No se encontraron registros válidos para renderizar la vista.")
            return

        total_patients = int(df["patient_id"].nunique())
        total_evaluations = int(len(df))
        malignant_cases = int((df["predicted_class"] == "Malignant").sum())
        pct_malignant = (malignant_cases / total_evaluations * 100) if total_evaluations else 0.0

        top_kpi1, top_kpi2, top_kpi3 = st.columns(3, gap="small")

        with top_kpi1:
            self._metric_card("PACIENTES", total_patients)

        with top_kpi2:
            self._metric_card("EVALUACIONES", total_evaluations)

        with top_kpi3:
            self._metric_card("RIESGO MALIGNO", f"{pct_malignant:.1f}%")

        st.markdown("### Comparación rápida entre grupos")
        st.caption(
            f"{malignant_cases} evaluaciones fueron clasificadas como malignas. Los boxplots ayudan a ver si una variable tiende a concentrarse más alto o más dispersa en uno de los dos grupos."
        )

        row_1_col1, row_1_col2 = st.columns(2, gap="large")
        row_2_col1, row_2_col2 = st.columns(2, gap="large")

        with row_1_col1:
            self._render_boxplot_radius(df)
            self._render_chart_help(
                "Radio medio",
                "Si el grupo maligno presenta medianas más altas o más dispersión, el tamaño tumoral tiende a asociarse con mayor severidad del caso."
            )

        with row_1_col2:
            self._render_boxplot_texture(df)
            self._render_chart_help(
                "Textura media",
                "Diferencias en textura pueden sugerir cambios en la heterogeneidad del tejido. Mayor dispersión en malignos suele reflejar casos menos uniformes."
            )

        with row_2_col1:
            self._render_boxplot_area(df)
            self._render_chart_help(
                "Área media",
                "Un área media más alta en casos malignos sugiere lesiones más extensas. También conviene observar valores atípicos por posible riesgo elevado."
            )

        with row_2_col2:
            self._render_boxplot_smoothness(df)
            self._render_chart_help(
                "Suavidad media",
                "La suavidad muestra qué tan regular es la superficie observada. Cambios sostenidos entre grupos pueden ayudar a separar casos benignos y malignos."
            )

        st.markdown("### Dashboard ejecutivo")
        st.caption(
            "Para visualizar mejor los datos, puedes revisar el siguiente dashboard interactivo."
        )
        self._render_power_bi_link()

    # =====================================================
    # CARGA Y PREPARACIÓN DE DATOS
    # =====================================================

    def _load_dashboard_data(self) -> pd.DataFrame:
        """
        Construye el dataset unificando:
        - listado de pacientes
        - historial de mediciones por paciente
        """
        rows: list[dict] = []

        try:
            patients_response = self.api_client.get_patients()
            patients = patients_response.get("patients", [])
        except Exception as exc:
            st.error(f"No fue posible obtener pacientes desde la API: {exc}")
            return pd.DataFrame()

        for patient in patients:
            patient_id = patient.get("patient_id")

            if patient_id is None:
                continue

            try:
                history_response = self.api_client.get_patient_measurements(patient_id)
                measurements = history_response.get("measurements", [])
                patient_info = history_response.get("patient", patient)
            except Exception:
                # Si un paciente falla, no se cae toda la vista.
                continue

            for measurement in measurements:
                row = dict(measurement)

                row["patient_id"] = patient_info.get("patient_id", patient_id)
                row["age"] = patient_info.get("age")
                row["sex"] = patient_info.get("sex")
                row["full_name"] = patient_info.get("full_name")
                row["rut"] = patient_info.get("rut")

                rows.append(row)

        return pd.DataFrame(rows)

    def _prepare_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Limpia y tipifica columnas necesarias para el análisis.
        """
        df = df.copy()

        numeric_cols = [
            "patient_id",
            "age",
            "radius_mean",
            "texture_mean",
            "area_mean",
            "smoothness_mean",
            "prediction_score",
        ]

        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")
            else:
                df[col] = None

        if "evaluation_date" not in df.columns:
            df["evaluation_date"] = pd.NaT

        df["evaluation_date"] = pd.to_datetime(df["evaluation_date"], errors="coerce")
        df = df[df["evaluation_date"].notna()].copy()

        if "predicted_class" not in df.columns:
            df["predicted_class"] = "Unknown"

        df["predicted_class"] = (
            df["predicted_class"]
            .astype(str)
            .str.strip()
            .str.title()
        )

        return df

    def _metric_card(self, title: str, value) -> None:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-title">{title}</div>
                <div class="kpi-value">{value}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    def _render_chart_help(self, label: str, text: str) -> None:
        st.markdown(
            f"""
            <div class="viz-help">
                <div class="viz-help-chip">Como leer el {label}</div>
                <div class="viz-help-tooltip">{text}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # =====================================================
    # VISUALES: BOXPLOTS
    # =====================================================

    def _render_boxplot_radius(self, df: pd.DataFrame) -> None:
        st.markdown("<div class='chart-title'>Boxplot de radio medio por clasificación</div>", unsafe_allow_html=True)

        plot_df = df[df["predicted_class"].isin(["Benign", "Malignant"])].dropna(
            subset=["predicted_class", "radius_mean"]
        )

        fig = px.box(
            plot_df,
            x="predicted_class",
            y="radius_mean",
            color="predicted_class",
            points="outliers",
            color_discrete_map={
                "Benign": self.colors.benign,
                "Malignant": self.colors.malignant,
            },
        )

        fig.update_layout(
            xaxis_title="Clasificación",
            yaxis_title="Radio medio",
            margin=dict(t=10, b=10, l=10, r=10),
            paper_bgcolor="white",
            height=360,
            showlegend=False,
        )

        st.plotly_chart(fig, use_container_width=True)

    def _render_boxplot_texture(self, df: pd.DataFrame) -> None:
        st.markdown("<div class='chart-title'>Boxplot de textura media por clasificación</div>", unsafe_allow_html=True)

        plot_df = df[df["predicted_class"].isin(["Benign", "Malignant"])].dropna(
            subset=["predicted_class", "texture_mean"]
        )

        fig = px.box(
            plot_df,
            x="predicted_class",
            y="texture_mean",
            color="predicted_class",
            points="outliers",
            color_discrete_map={
                "Benign": self.colors.benign,
                "Malignant": self.colors.malignant,
            },
        )

        fig.update_layout(
            xaxis_title="Clasificación",
            yaxis_title="Textura media",
            margin=dict(t=10, b=10, l=10, r=10),
            paper_bgcolor="white",
            height=360,
            showlegend=False,
        )

        st.plotly_chart(fig, use_container_width=True)

    def _render_boxplot_area(self, df: pd.DataFrame) -> None:
        st.markdown("<div class='chart-title'>Boxplot de área media por clasificación</div>", unsafe_allow_html=True)

        plot_df = df[df["predicted_class"].isin(["Benign", "Malignant"])].dropna(
            subset=["predicted_class", "area_mean"]
        )

        fig = px.box(
            plot_df,
            x="predicted_class",
            y="area_mean",
            color="predicted_class",
            points="outliers",
            color_discrete_map={
                "Benign": self.colors.benign,
                "Malignant": self.colors.malignant,
            },
        )

        fig.update_layout(
            xaxis_title="Clasificación",
            yaxis_title="Área media",
            margin=dict(t=10, b=10, l=10, r=10),
            paper_bgcolor="white",
            height=360,
            showlegend=False,
        )

        st.plotly_chart(fig, use_container_width=True)

    def _render_boxplot_smoothness(self, df: pd.DataFrame) -> None:
        st.markdown("<div class='chart-title'>Boxplot de suavidad media por clasificación</div>", unsafe_allow_html=True)

        plot_df = df[df["predicted_class"].isin(["Benign", "Malignant"])].dropna(
            subset=["predicted_class", "smoothness_mean"]
        )

        fig = px.box(
            plot_df,
            x="predicted_class",
            y="smoothness_mean",
            color="predicted_class",
            points="outliers",
            color_discrete_map={
                "Benign": self.colors.benign,
                "Malignant": self.colors.malignant,
            },
        )

        fig.update_layout(
            xaxis_title="Clasificación",
            yaxis_title="Suavidad media",
            margin=dict(t=10, b=10, l=10, r=10),
            paper_bgcolor="white",
            height=360,
            showlegend=False,
        )

        st.plotly_chart(fig, use_container_width=True)

    # =====================================================
    # POWER BI
    # =====================================================

    def _render_power_bi_link(self) -> None:
        power_bi_url = self.power_bi_path.resolve().as_uri()
        power_bi_label = escape(str(self.power_bi_path))

        st.markdown(
            f"""
            <div class="powerbi-box">
                Este dashboard permite explorar los registros con una vista más ejecutiva,
                interactiva y orientada a segmentaciones, tendencias y seguimiento clínico.
                <br><br>
                <a href="{power_bi_url}" target="_blank" class="powerbi-link">
                    Visualizar dashboard ejecutivo
                </a>
                <div style="margin-top:0.85rem; color:{self.colors.text}; font-size:0.9rem;">
                    Archivo local asociado: {power_bi_label}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # =====================================================
    # ESTILO
    # =====================================================

    def _inject_css(self) -> None:
        st.markdown(
            f"""
            <style>
            .kpi-card {{
                background: {self.colors.soft_bg};
                border: 1px solid {self.colors.border};
                border-radius: 14px;
                padding: 0.8rem 1rem;
                text-align: center;
                min-height: 120px;
                display: flex;
                flex-direction: column;
                justify-content: center;
                box-shadow: 0 1px 3px rgba(0,0,0,0.06);
            }}

            .kpi-title {{
                color: {self.colors.primary};
                font-size: 1.15rem;
                font-weight: 800;
                margin-bottom: 0.3rem;
            }}

            .kpi-value {{
                color: {self.colors.primary_dark};
                font-size: 2.4rem;
                font-weight: 800;
                line-height: 1.1;
            }}

            .chart-title {{
                color: {self.colors.primary};
                font-size: 1.1rem;
                font-weight: 800;
                margin-bottom: 0.35rem;
                margin-top: 0.35rem;
            }}

            .info-banner {{
                background: #fff7fa;
                border-left: 6px solid {self.colors.primary};
                padding: 1rem 1.2rem;
                border-radius: 12px;
                margin-bottom: 1rem;
                color: {self.colors.text};
                line-height: 1.6;
            }}

            .section-note {{
                background: #fff7fa;
                border: 1px solid {self.colors.border};
                border-radius: 10px;
                padding: 0.7rem 0.9rem;
                margin-top: 0.5rem;
                color: {self.colors.text};
                font-size: 0.93rem;
                line-height: 1.5;
            }}

            .viz-help {{
                position: relative;
                display: inline-flex;
                flex-direction: column;
                align-items: flex-start;
                margin-top: 0.45rem;
                margin-bottom: 0.35rem;
            }}

            .viz-help-chip {{
                display: inline-flex;
                align-items: center;
                gap: 0.35rem;
                padding: 0.5rem 0.9rem;
                border-radius: 999px;
                border: 1px solid {self.colors.border};
                background: #fff7fa;
                color: {self.colors.primary};
                font-size: 0.9rem;
                font-weight: 700;
                cursor: default;
                box-shadow: 0 6px 14px rgba(231, 84, 128, 0.08);
            }}

            .viz-help-tooltip {{
                opacity: 0;
                pointer-events: none;
                transform: translateY(6px);
                transition: opacity 0.2s ease, transform 0.2s ease;
                position: absolute;
                top: calc(100% + 0.45rem);
                left: 0;
                min-width: 260px;
                max-width: 420px;
                background: #fffafb;
                border: 1px solid {self.colors.border};
                border-radius: 14px;
                padding: 0.8rem 0.95rem;
                color: {self.colors.text};
                line-height: 1.55;
                box-shadow: 0 12px 24px rgba(0,0,0,0.08);
                z-index: 20;
            }}

            .viz-help:hover .viz-help-tooltip {{
                opacity: 1;
                transform: translateY(0);
            }}

            .powerbi-box {{
                background: {self.colors.soft_bg};
                border: 1px solid {self.colors.border};
                border-radius: 14px;
                padding: 1rem 1.2rem;
                color: {self.colors.text};
                line-height: 1.6;
                margin-top: 0.5rem;
            }}

            .powerbi-link {{
                display: inline-block;
                background: {self.colors.primary};
                color: white !important;
                text-decoration: none;
                padding: 0.65rem 1rem;
                border-radius: 10px;
                font-weight: 700;
            }}
            </style>
            """,
            unsafe_allow_html=True,
        )
