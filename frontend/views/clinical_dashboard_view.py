"""
Vista de dashboard clínico.
Replica del dashboard diseñado en Power BI, renderizada en Streamlit.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st


@dataclass
class DashboardColors:
    """
    Paleta visual inspirada en la temática de cáncer de mama.
    """
    primary: str = "#C2185B"
    primary_dark: str = "#880E4F"
    benign: str = "#E9A3C9"
    malignant: str = "#E75480"
    soft_bg: str = "#FCE4EC"
    border: str = "#F8BBD0"
    text: str = "#4A4A4A"


class ClinicalDashboardView:
    """
    Renderiza la sección de dashboard clínico.
    """

    def __init__(self, api_client) -> None:
        """
        Inicializa la vista de dashboard clínico.

        Args:
            api_client: Cliente base para comunicación con la API.
        """
        self.api_client = api_client
        self.colors = DashboardColors()

    def render(self) -> None:
        """
        Renderiza el contenido visual de la vista.
        """
        st.title("Dashboard Clínico")

        df = self._load_dashboard_data()

        if df.empty:
            st.info("No hay datos clínicos disponibles para construir el dashboard.")
            return

        df = self._prepare_dataframe(df)

        if df.empty:
            st.warning("No se encontraron registros válidos para renderizar el dashboard.")
            return

        self._inject_css()

        years = sorted(df["year"].dropna().unique().tolist())

        top_filter, top_kpi1, top_kpi2, top_kpi3, top_kpi4 = st.columns(
            [0.95, 1.35, 1.35, 1.35, 1.45],
            gap="small"
        )

        with top_filter:
            selected_years = self._render_year_filter(years)

        if selected_years:
            df = df[df["year"].isin(selected_years)].copy()

        if df.empty:
            st.info("No hay registros para el año seleccionado.")
            return

        total_patients = int(df["patient_id"].nunique())
        total_evaluations = int(len(df))
        malignant_cases = int((df["predicted_class"] == "Malignant").sum())
        pct_malignant = (malignant_cases / total_evaluations * 100) if total_evaluations else 0.0

        with top_kpi1:
            self._metric_card("PACIENTES", total_patients)

        with top_kpi2:
            self._metric_card("EVALUACIONES", total_evaluations)

        with top_kpi3:
            self._metric_card("CASOS MALIGNOS", malignant_cases)

        with top_kpi4:
            self._metric_card("% CASOS MALIGNOS", f"{pct_malignant:.2f}%")

        row_1_left, row_1_mid, row_1_right = st.columns([1.05, 1.35, 1.85], gap="large")

        with row_1_left:
            self._render_diagnosis_distribution(df)

        with row_1_mid:
            self._render_monthly_followup(df)

        with row_1_right:
            self._render_key_influencers(df)

        row_2_left, row_2_mid, row_2_right = st.columns([1.1, 1.1, 1.8], gap="large")

        with row_2_left:
            self._render_scatter(df)

        with row_2_mid:
            self._render_age_distribution(df)

        with row_2_right:
            self._render_dashboard_signature()

    # =====================================================
    # CARGA Y PREPARACIÓN DE DATOS
    # =====================================================

    def _load_dashboard_data(self) -> pd.DataFrame:
        """
        Construye el dataset del dashboard unificando:
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
                # Si un paciente falla, no botamos todo el dashboard.
                continue

            for measurement in measurements:
                row = dict(measurement)

                # Complementamos con datos del paciente.
                row["patient_id"] = patient_info.get("patient_id", patient_id)
                row["age"] = patient_info.get("age")
                row["sex"] = patient_info.get("sex")
                row["full_name"] = patient_info.get("full_name")
                row["rut"] = patient_info.get("rut")

                rows.append(row)

        return pd.DataFrame(rows)

    def _prepare_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Limpia y tipifica columnas necesarias para el dashboard.
        """
        df = df.copy()

        numeric_cols = [
            "patient_id",
            "age",
            "radius_mean",
            "texture_mean",
            "area_mean",
            "smoothness_mean",
            "compactness_mean",
            "concavity_mean",
            "symmetry_mean",
            "prediction_score",
        ]

        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")
            else:
                df[col] = np.nan

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

        df["year"] = df["evaluation_date"].dt.year
        df["month_start"] = df["evaluation_date"].dt.to_period("M").dt.to_timestamp()

        return df

    # =====================================================
    # HELPERS DE UI
    # =====================================================

    def _render_year_filter(self, years: list[int]) -> list[int]:
        """
        Renderiza filtro de año.
        """
        with st.container(border=True):
            st.markdown(
                f"<div style='color:{self.colors.primary}; font-weight:800; font-size:1.1rem;'>Año</div>",
                unsafe_allow_html=True,
            )

            selected_years = st.multiselect(
                label="Año",
                options=years,
                default=years,
                label_visibility="collapsed",
            )

        return selected_years

    def _metric_card(self, title: str, value) -> None:
        """
        Renderiza tarjeta KPI estilizada.
        """
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-title">{title}</div>
                <div class="kpi-value">{value}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # =====================================================
    # VISUALES
    # =====================================================

    def _render_diagnosis_distribution(self, df: pd.DataFrame) -> None:
        """
        Donut chart Benign vs Malignant.
        """
        st.markdown(
            "<div class='chart-title'>Distribución de diagnósticos</div>",
            unsafe_allow_html=True,
        )

        counts = (
            df["predicted_class"]
            .value_counts()
            .rename_axis("Predicción")
            .reset_index(name="Casos")
        )

        fig = px.pie(
            counts,
            names="Predicción",
            values="Casos",
            hole=0.55,
            color="Predicción",
            color_discrete_map={
                "Benign": self.colors.benign,
                "Malignant": self.colors.malignant,
            },
        )

        fig.update_traces(
            textposition="outside",
            textinfo="value+percent",
            marker=dict(line=dict(color="white", width=2)),
        )

        fig.update_layout(
            legend_title_text="Predicción",
            margin=dict(t=10, b=10, l=10, r=10),
            paper_bgcolor="white",
            height=340,
        )

        st.plotly_chart(fig, use_container_width=True)

    def _render_monthly_followup(self, df: pd.DataFrame) -> None:
        """
        Gráfico de línea mensual.
        """
        st.markdown(
            "<div class='chart-title'>Seguimiento mensual de evaluaciones de cáncer de mama</div>",
            unsafe_allow_html=True,
        )

        monthly = (
            df.groupby("month_start", as_index=False)
            .size()
            .rename(columns={"size": "Evaluaciones"})
        )

        fig = px.line(
            monthly,
            x="month_start",
            y="Evaluaciones",
            markers=True,
        )

        fig.update_traces(
            line=dict(color=self.colors.benign, width=4),
            marker=dict(size=9, color=self.colors.malignant),
        )

        fig.update_layout(
            xaxis_title="Mes",
            yaxis_title="Número de evaluaciones",
            margin=dict(t=10, b=10, l=10, r=10),
            paper_bgcolor="white",
            height=340,
        )

        st.plotly_chart(fig, use_container_width=True)

    def _render_scatter(self, df: pd.DataFrame) -> None:
        """
        Scatter de radio medio vs textura media.
        """
        st.markdown(
            "<div class='chart-title'>Relación entre radio y textura del tumor</div>",
            unsafe_allow_html=True,
        )

        plot_df = df.dropna(subset=["radius_mean", "texture_mean"]).copy()

        fig = px.scatter(
            plot_df,
            x="radius_mean",
            y="texture_mean",
            color="predicted_class",
            color_discrete_map={
                "Benign": self.colors.benign,
                "Malignant": self.colors.malignant,
            },
            opacity=0.82,
        )

        fig.update_traces(
            marker=dict(
                size=10,
                line=dict(width=0.5, color="white")
            )
        )

        fig.update_layout(
            xaxis_title="Radio medio del tumor",
            yaxis_title="Textura media del tumor",
            legend_title_text="Predicción",
            margin=dict(t=10, b=10, l=10, r=10),
            paper_bgcolor="white",
            height=350,
        )

        st.plotly_chart(fig, use_container_width=True)

    def _render_age_distribution(self, df: pd.DataFrame) -> None:
        """
        Histograma de edad por predicción.
        """
        st.markdown(
            "<div class='chart-title'>Distribución de pacientes por edad</div>",
            unsafe_allow_html=True,
        )

        hist_df = df.dropna(subset=["age"]).copy()

        fig = px.histogram(
            hist_df,
            x="age",
            color="predicted_class",
            nbins=10,
            barmode="group",
            color_discrete_map={
                "Benign": self.colors.benign,
                "Malignant": self.colors.malignant,
            },
        )

        fig.update_layout(
            xaxis_title="Edad del paciente",
            yaxis_title="Número de pacientes",
            legend_title_text="Predicción",
            margin=dict(t=10, b=10, l=10, r=10),
            paper_bgcolor="white",
            height=320,
        )

        st.plotly_chart(fig, use_container_width=True)

    def _render_key_influencers(self, df: pd.DataFrame) -> None:
        """
        Aproximación del panel de influenciadores clave.
        """
        st.markdown(
            "<div class='chart-title'>Elementos influyentes clave</div>",
            unsafe_allow_html=True,
        )

        features = [
            "area_mean",
            "concavity_mean",
            "texture_mean",
            "smoothness_mean",
            "radius_mean",
            "compactness_mean",
            "symmetry_mean",
        ]

        working = df[df["predicted_class"].isin(["Benign", "Malignant"])].copy()
        benign = working[working["predicted_class"] == "Benign"]
        malignant = working[working["predicted_class"] == "Malignant"]

        rows = []

        for col in features:
            s_b = pd.to_numeric(benign[col], errors="coerce").dropna()
            s_m = pd.to_numeric(malignant[col], errors="coerce").dropna()

            if len(s_b) < 2 or len(s_m) < 2:
                continue

            mean_b = s_b.mean()
            mean_m = s_m.mean()
            pooled_std = np.sqrt((s_b.var(ddof=1) + s_m.var(ddof=1)) / 2)

            if pooled_std == 0 or np.isnan(pooled_std):
                continue

            effect = (mean_m - mean_b) / pooled_std

            rows.append(
                {
                    "feature": col,
                    "effect": effect,
                    "impact": abs(effect),
                }
            )

        infl = pd.DataFrame(rows)

        if infl.empty:
            st.info("No hay datos suficientes para calcular influenciadores.")
            return

        infl = infl.sort_values("impact", ascending=False).head(7)

        st.markdown(
            f"""
            <div style="background:{self.colors.soft_bg}; padding:1rem; border-radius:12px; border:1px solid {self.colors.border};">
                <div style="font-size:1rem; color:{self.colors.text}; margin-bottom:0.8rem;">
                    Qué influye en <b>predicted_class</b> para ser <b>Malignant</b>
                </div>
            """,
            unsafe_allow_html=True,
        )

        max_impact = infl["impact"].max()

        for _, row in infl.iterrows():
            label = row["feature"].replace("_mean", "").replace("_", " ").title()
            ratio = 1 + row["impact"] * 2.2
            width_pct = 20 + (row["impact"] / max_impact) * 70

            st.markdown(
                f"""
                <div style="margin-bottom:1rem;">
                    <div style="display:flex; justify-content:space-between; gap:1rem;">
                        <div style="width:70%; color:{self.colors.text}; font-size:0.95rem;">
                            {label} sube
                        </div>
                        <div style="width:30%; text-align:right; color:{self.colors.primary_dark}; font-weight:700;">
                            {ratio:.2f}x
                        </div>
                    </div>
                    <div style="margin-top:0.35rem; background:#f6d7e5; border-radius:999px; height:14px; overflow:hidden;">
                        <div style="width:{width_pct:.1f}%; background:{self.colors.benign}; height:14px; border-radius:999px;"></div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown("</div>", unsafe_allow_html=True)

    def _render_dashboard_signature(self) -> None:
        """
        Firma visual inferior del dashboard.
        """
        st.markdown(
            f"""
            <div style="margin-top:1rem; padding-top:0.6rem; border-top:2px solid {self.colors.border};">
                <div style="font-size:2rem; font-weight:800; color:{self.colors.primary};">
                    Breast Cancer Diagnostic Analysis Dashboard
                </div>
                <div style="font-size:0.95rem; color:{self.colors.primary_dark}; margin-top:0.2rem;">
                    Machine Learning Model Insights
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # =====================================================
    # ESTILO
    # =====================================================

    def _inject_css(self) -> None:
        """
        Inyecta estilos globales para la vista.
        """
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
                font-size: 1.35rem;
                font-weight: 800;
                margin-bottom: 0.3rem;
            }}

            .kpi-value {{
                color: {self.colors.primary_dark};
                font-size: 3rem;
                font-weight: 800;
                line-height: 1.1;
            }}

            .chart-title {{
                color: {self.colors.primary};
                font-size: 1.15rem;
                font-weight: 800;
                margin-bottom: 0.35rem;
                margin-top: 0.35rem;
            }}
            </style>
            """,
            unsafe_allow_html=True,
        )