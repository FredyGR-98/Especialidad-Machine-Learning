"""
===========================================================
patients_view.py
===========================================================

Vista operativa del predictor de cancer de mama.

Responsabilidades:
- Presentar el estado de los casos clinicos ya cargados.
- Permitir revisar pacientes previos y su evolucion.
- Permitir registrar un nuevo paciente con una nueva evaluacion.
- Ejecutar una prediccion previa antes de guardar.
- Persistir la evaluacion en la base de datos del sistema.
===========================================================
"""

from __future__ import annotations

from datetime import date
from html import escape
from textwrap import dedent

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from services.patient_service import PatientService
from services.prediction_service import PredictionService
from utils.feature_config import FEATURE_INPUT_CONFIG


class PatientsView:
    """
    Renderiza la seccion operativa del predictor clinico.
    """

    NEW_PATIENT_OPTION = "Nuevo paciente"

    FEATURE_GROUPS = {
        "Mediciones promedio": [
            "radius_mean",
            "texture_mean",
            "perimeter_mean",
            "area_mean",
            "smoothness_mean",
            "compactness_mean",
            "concavity_mean",
            "concave_points_mean",
            "symmetry_mean",
            "fractal_dimension_mean",
        ],
        "Errores estandar": [
            "radius_se",
            "texture_se",
            "perimeter_se",
            "area_se",
            "smoothness_se",
            "compactness_se",
            "concavity_se",
            "concave_points_se",
            "symmetry_se",
            "fractal_dimension_se",
        ],
        "Peor valor observado": [
            "radius_worst",
            "texture_worst",
            "perimeter_worst",
            "area_worst",
            "smoothness_worst",
            "compactness_worst",
            "concavity_worst",
            "concave_points_worst",
            "symmetry_worst",
            "fractal_dimension_worst",
        ],
    }

    FEATURE_FIELDS = [
        field_name
        for group in FEATURE_GROUPS.values()
        for field_name in group
    ]

    def __init__(self, api_client) -> None:
        self.patient_service = PatientService(api_client)
        self.prediction_service = PredictionService(api_client)

    def render(self) -> None:
        self._inject_styles()
        self._initialize_state()

        patients = self._load_patients()
        self._render_header(patients)
        self._render_case_source_banner(patients)

        mode = self._render_mode_selector()

        if mode == "Casos previos":
            selected_patient = self._render_existing_patient_flow(patients)
            current_signature = self._build_patient_signature(
                selected_patient,
                is_new_patient=False,
            )
        else:
            self._render_new_patient_flow()
            selected_patient = None
            current_signature = self._build_patient_signature(
                None,
                is_new_patient=True,
            )

        if st.session_state.get("prediction_context_signature") != current_signature:
            self._clear_prediction_state()

        st.session_state["prediction_context_signature"] = current_signature
        self._render_pending_prediction_result()

    def _render_html(self, html_content: str) -> None:
        st.markdown(dedent(html_content).strip(), unsafe_allow_html=True)

    def _inject_styles(self) -> None:
        self._render_html(
            """
            <style>
            .patients-hero {
                background: linear-gradient(135deg, #fff7fb 0%, #fdebf3 100%);
                border: 1px solid #f5c9d8;
                border-radius: 28px;
                padding: 30px 32px;
                margin-bottom: 1.2rem;
                box-shadow: 0 14px 34px rgba(231, 84, 128, 0.08);
            }

            .hero-eyebrow {
                color: #c2185b;
                font-size: 0.88rem;
                font-weight: 800;
                letter-spacing: 0.18em;
                text-transform: uppercase;
                margin-bottom: 0.9rem;
            }

            .patients-hero h1 {
                color: #c2185b;
                font-size: 2.55rem;
                font-weight: 800;
                line-height: 1.08;
                margin: 0 0 0.8rem 0;
            }

            .patients-hero p {
                color: #5d4c57;
                font-size: 1.02rem;
                line-height: 1.78;
                margin: 0 0 1rem 0;
            }

            .hero-tags {
                display: flex;
                flex-wrap: wrap;
                gap: 0.7rem;
            }

            .hero-tag {
                border: 1px solid #efbfd0;
                background: rgba(255, 255, 255, 0.88);
                color: #c2185b;
                border-radius: 999px;
                padding: 0.55rem 0.95rem;
                font-size: 0.92rem;
                font-weight: 700;
            }

            .soft-section {
                background: #ffffff;
                border: 1px solid #f2cad8;
                border-radius: 24px;
                padding: 22px 24px;
                margin-bottom: 1.1rem;
                box-shadow: 0 8px 22px rgba(231, 84, 128, 0.05);
            }

            .soft-section-title {
                color: #c2185b;
                font-size: 1.48rem;
                font-weight: 800;
                margin-bottom: 0.4rem;
            }

            .soft-section-subtitle {
                color: #6d5863;
                font-size: 0.97rem;
                line-height: 1.7;
            }

            .kpi-card {
                background: #ffffff;
                border: 1px solid #f3d2de;
                border-radius: 20px;
                padding: 18px 18px 16px 18px;
                min-height: 150px;
                box-shadow: 0 10px 22px rgba(231, 84, 128, 0.05);
            }

            .kpi-label {
                color: #54444d;
                font-size: 0.88rem;
                font-weight: 800;
                letter-spacing: 0.08em;
                text-transform: uppercase;
                margin-bottom: 0.7rem;
            }

            .kpi-value {
                color: #c2185b;
                font-size: 2.2rem;
                font-weight: 800;
                line-height: 1;
                margin-bottom: 0.75rem;
            }

            .kpi-description {
                color: #6b5661;
                font-size: 0.95rem;
                line-height: 1.65;
            }

            .summary-card {
                background: #fff9fc;
                border: 1px solid #f2d4df;
                border-radius: 20px;
                padding: 18px 20px;
                box-shadow: 0 8px 18px rgba(231, 84, 128, 0.04);
                min-height: 176px;
            }

            .summary-label {
                color: #7b6771;
                font-size: 0.88rem;
                margin-bottom: 0.28rem;
            }

            .summary-value {
                color: #4a3b47;
                font-size: 1.02rem;
                font-weight: 700;
                margin-bottom: 0.85rem;
                line-height: 1.38;
                word-break: break-word;
            }

            .result-box {
                background: linear-gradient(135deg, #fff7fb 0%, #fffafb 100%);
                border: 1px solid #f2cad8;
                border-radius: 24px;
                padding: 22px 24px;
                margin-top: 1.2rem;
                box-shadow: 0 10px 24px rgba(231, 84, 128, 0.06);
            }

            .result-title {
                color: #c2185b;
                font-size: 1.5rem;
                font-weight: 800;
                margin-bottom: 0.35rem;
            }

            .result-subtitle {
                color: #6d5863;
                font-size: 0.97rem;
                line-height: 1.7;
                margin-bottom: 1rem;
            }

            .soft-note {
                background: #fff3f8;
                border-left: 5px solid #e75480;
                border-radius: 14px;
                padding: 14px 16px;
                color: #5d4c57;
                line-height: 1.65;
                margin-top: 0.4rem;
            }

            .mode-banner {
                background: linear-gradient(135deg, #ffffff 0%, #fff7fb 100%);
                border: 1px solid #f3d2de;
                border-radius: 22px;
                padding: 18px 20px;
                margin-bottom: 1rem;
            }

            .mode-title {
                color: #c2185b;
                font-size: 1.18rem;
                font-weight: 800;
                margin-bottom: 0.3rem;
            }

            .mode-copy {
                color: #6d5863;
                line-height: 1.65;
            }

            .slider-group-title {
                color: #3f3138;
                font-size: 1.04rem;
                font-weight: 800;
                margin: 1rem 0 0.35rem 0;
            }

            .slider-group-copy {
                color: #75606a;
                font-size: 0.92rem;
                line-height: 1.55;
                margin-bottom: 0.75rem;
            }

            .history-caption {
                color: #7a6571;
                font-size: 0.9rem;
                line-height: 1.55;
                margin-top: 0.4rem;
            }

            div[data-testid="stMetric"] {
                background: #ffffff;
                border: 1px solid #f4cddd;
                border-radius: 18px;
                padding: 12px 12px;
                box-shadow: 0 8px 18px rgba(231, 84, 128, 0.05);
            }

            div[data-testid="stMetricLabel"] {
                color: #7a6571 !important;
                font-weight: 600 !important;
            }

            div[data-testid="stMetricValue"] {
                color: #c2185b !important;
                font-weight: 800 !important;
            }

            div[data-testid="stForm"] {
                background: #ffffff;
                border: 1px solid #f2cad8;
                border-radius: 22px;
                padding: 1rem 1rem 0.8rem 1rem;
                box-shadow: 0 8px 22px rgba(231, 84, 128, 0.04);
            }

            div[data-testid="stButton"] > button,
            div[data-testid="stFormSubmitButton"] > button {
                border-radius: 14px !important;
                border: none !important;
                background: linear-gradient(90deg, #e75480 0%, #d93d72 100%) !important;
                color: white !important;
                font-weight: 700 !important;
                padding: 0.68rem 1rem !important;
                box-shadow: 0 8px 18px rgba(231, 84, 128, 0.16);
            }

            div[data-testid="stRadio"] label,
            div[data-testid="stSelectbox"] label,
            div[data-testid="stDateInput"] label,
            div[data-testid="stNumberInput"] label,
            div[data-testid="stTextInput"] label,
            div[data-testid="stSlider"] label {
                color: #5d4c57 !important;
                font-weight: 600 !important;
            }

            .donut-caption {
                text-align: center;
                color: #7a6571;
                font-size: 0.92rem;
                margin-top: -0.3rem;
            }

            .measure-table-shell {
                border: 1px solid #f2cad8;
                border-radius: 20px;
                overflow: hidden;
                background: #fffafb;
                box-shadow: 0 8px 20px rgba(231, 84, 128, 0.04);
                margin-top: 0.35rem;
                margin-bottom: 0.8rem;
            }

            .measure-table {
                width: 100%;
                border-collapse: collapse;
                table-layout: fixed;
            }

            .measure-table thead th {
                background: linear-gradient(180deg, #d81b60 0%, #e75480 100%);
                color: #ffffff;
                text-align: left;
                font-size: 0.95rem;
                font-weight: 800;
                padding: 0.9rem 1rem;
                border-right: 1px solid rgba(255, 255, 255, 0.16);
            }

            .measure-table thead th:last-child {
                border-right: none;
            }

            .measure-table tbody td {
                padding: 0.9rem 1rem;
                border-top: 1px solid #f3d9e3;
                vertical-align: top;
                color: #4d3d47;
                line-height: 1.5;
                background: #fffafb;
            }

            .measure-table tbody tr:nth-child(even) td {
                background: #fff6fa;
            }

            .measure-col-variable {
                width: 27%;
                font-weight: 700;
                color: #40323a;
            }

            .measure-col-value {
                width: 18%;
                font-weight: 700;
                color: #c2185b;
            }

            .measure-col-reading {
                width: 55%;
            }
            </style>
            """
        )

    def _initialize_state(self) -> None:
        defaults = {
            "patients_pending_prediction": None,
            "patients_pending_patient": None,
            "patients_pending_measurement": None,
            "patients_pending_date": None,
            "prediction_context_signature": None,
            "patients_selected_patient_id": None,
            "records_refresh_nonce": 0,
        }

        for key, value in defaults.items():
            if key not in st.session_state:
                st.session_state[key] = value

    def _clear_prediction_state(self) -> None:
        st.session_state["patients_pending_prediction"] = None
        st.session_state["patients_pending_patient"] = None
        st.session_state["patients_pending_measurement"] = None
        st.session_state["patients_pending_date"] = None
        st.session_state["prediction_context_signature"] = None

    def _load_patients(self) -> list[dict]:
        try:
            response = self.patient_service.get_patients()
            return response.get("patients", [])
        except RuntimeError as exc:
            st.error(f"No fue posible cargar los casos clínicos: {exc}")
            return []

    def _render_header(self, patients: list[dict]) -> None:
        total_patients = len(patients)
        total_measurements = sum(int(patient.get("total_measurements", 0) or 0) for patient in patients)

        self._render_html(
            f"""
            <div class="patients-hero">
                <div class="hero-eyebrow">Operacion clinica</div>
                <h1>Predictor de Cancer de Mama</h1>
                <p>
                    Este modulo concentra la operacion del caso: permite revisar registros
                    previamente cargados desde la base clinica, observar la evolucion de
                    cada paciente y ejecutar una nueva evaluacion con apoyo del modelo de
                    Machine Learning antes de guardar el resultado.
                </p>
                <div class="hero-tags">
                    <div class="hero-tag">{total_patients} pacientes disponibles</div>
                    <div class="hero-tag">{total_measurements} evaluaciones registradas</div>
                    <div class="hero-tag">Modelo activo: Random Forest</div>
                </div>
            </div>
            """
        )

    def _render_case_source_banner(self, patients: list[dict]) -> None:
        total_measurements = sum(int(patient.get("total_measurements", 0) or 0) for patient in patients)

        col1, col2, col3 = st.columns(3)

        with col1:
            self._render_html(
                f"""
                <div class="kpi-card">
                    <div class="kpi-label">Base clinica activa</div>
                    <div class="kpi-value">{len(patients)}</div>
                    <div class="kpi-description">
                        Pacientes disponibles para revisar historiales, continuidad y nuevas evaluaciones.
                    </div>
                </div>
                """
            )

        with col2:
            self._render_html(
                f"""
                <div class="kpi-card">
                    <div class="kpi-label">Casos acumulados</div>
                    <div class="kpi-value">{total_measurements}</div>
                    <div class="kpi-description">
                        Registros clinicos ya persistidos en la base utilizada por el dashboard y la API.
                    </div>
                </div>
                """
            )

        with col3:
            self._render_html(
                """
                <div class="kpi-card">
                    <div class="kpi-label">Fuente de trabajo</div>
                    <div class="kpi-value">SQLite</div>
                    <div class="kpi-description">
                        Esta vista hoy trabaja sobre la base local del proyecto. Luego podemos sumar carga externa para reemplazar la demo.
                    </div>
                </div>
                """
            )

    def _render_mode_selector(self) -> str:
        self._render_html(
            """
            <div class="mode-banner">
                <div class="mode-title">Flujo de trabajo</div>
                <div class="mode-copy">
                    Elige si quieres analizar un caso ya registrado o iniciar la captura de un nuevo paciente.
                </div>
            </div>
            """
        )

        return st.radio(
            "Flujo de trabajo",
            options=["Casos previos", "Nuevo paciente"],
            horizontal=True,
            label_visibility="collapsed",
        )

    def _render_existing_patient_flow(self, patients: list[dict]) -> dict | None:
        selected_patient = self._render_patient_selector(patients)

        if not selected_patient:
            st.info("No hay un paciente seleccionado. Puedes cambiar al modo de nuevo paciente si quieres iniciar un caso.")
            return None

        self._render_patient_summary_card(selected_patient)
        self._render_patient_history(selected_patient)
        self._render_existing_patient_evaluation_form(selected_patient)
        return selected_patient

    def _render_new_patient_flow(self) -> None:
        self._render_new_patient_form()

    def _render_patient_selector(self, patients: list[dict]) -> dict | None:
        self._render_html(
            """
            <div class="soft-section">
                <div class="soft-section-title">Casos historicos de la clinica</div>
                <div class="soft-section-subtitle">
                    Selecciona un paciente ya cargado para revisar su evolucion y generar una nueva evaluacion comparativa.
                </div>
            </div>
            """
        )

        if not patients:
            st.warning("No se encontraron pacientes cargados en la base actual.")
            return None

        search_term = st.text_input(
            "Buscar paciente por nombre o RUT",
            placeholder="Ejemplo: Maria Gonzalez o 12.345.678-9",
        ).strip().lower()

        filtered_patients = [
            patient for patient in patients
            if not search_term
            or search_term in str(patient.get("full_name", "")).lower()
            or search_term in str(patient.get("rut", "")).lower()
        ]

        if not filtered_patients:
            st.info("No se encontraron coincidencias con la búsqueda actual.")
            return None

        patient_options = {}
        option_labels = []
        preferred_patient_id = st.session_state.get("patients_selected_patient_id")
        selected_index = 0

        for patient in filtered_patients:
            label = self._format_patient_option(patient)
            patient_options[label] = patient
            option_labels.append(label)

            if patient.get("patient_id") == preferred_patient_id:
                selected_index = len(option_labels) - 1

        selected_label = st.selectbox(
            "Seleccionar paciente",
            options=option_labels,
            index=selected_index,
            key="patients_selector",
        )

        selected_patient = patient_options[selected_label]
        st.session_state["patients_selected_patient_id"] = selected_patient.get("patient_id")
        return selected_patient

    def _render_patient_summary_card(self, patient: dict) -> None:
        self._render_html(
            """
            <div class="soft-section">
                <div class="soft-section-title">Ficha resumida del caso</div>
                <div class="soft-section-subtitle">
                    Esta ficha ayuda a contextualizar el caso actual antes de revisar historiales y repetir pruebas.
                </div>
            </div>
            """
        )

        total_measurements = patient.get("total_measurements", 0) or 0
        last_eval = patient.get("last_evaluation_date") or "Sin registros"

        rut = escape(str(patient.get("rut", "N/D")))
        full_name = escape(str(patient.get("full_name", "N/D")))
        sex = escape(str(patient.get("sex", "N/D")))
        age = escape(str(patient.get("age", "N/D")))
        total_measurements = escape(str(total_measurements))
        last_eval = escape(str(last_eval))

        col1, col2, col3 = st.columns(3)

        with col1:
            self._render_html(
                f"""
                <div class="summary-card">
                    <div class="summary-label">Paciente</div>
                    <div class="summary-value">{full_name}</div>
                    <div class="summary-label">Identificador</div>
                    <div class="summary-value">{rut}</div>
                </div>
                """
            )

        with col2:
            self._render_html(
                f"""
                <div class="summary-card">
                    <div class="summary-label">Edad</div>
                    <div class="summary-value">{age} años</div>
                    <div class="summary-label">Sexo</div>
                    <div class="summary-value">{sex}</div>
                </div>
                """
            )

        with col3:
            self._render_html(
                f"""
                <div class="summary-card">
                    <div class="summary-label">Evaluaciones acumuladas</div>
                    <div class="summary-value">{total_measurements}</div>
                    <div class="summary-label">Ultimo control</div>
                    <div class="summary-value">{last_eval}</div>
                </div>
                """
            )

    def _render_patient_history(self, patient: dict) -> None:
        self._render_html(
            """
            <div class="soft-section">
                <div class="soft-section-title">Evolucion del paciente</div>
                <div class="soft-section-subtitle">
                    Revisa controles anteriores, su clase estimada y el nivel de confianza antes de cargar una nueva evaluacion.
                </div>
            </div>
            """
        )

        patient_id = patient.get("patient_id")

        if not patient_id:
            st.warning("No se encontro el identificador del paciente.")
            return

        try:
            response = self.patient_service.get_patient_measurements(patient_id)
            measurements = response.get("measurements", [])
        except RuntimeError as exc:
            st.error(f"No fue posible cargar la evolucion del paciente: {exc}")
            return

        if not measurements:
            st.info("Este paciente aun no registra evaluaciones clinicas.")
            return

        measurement_options = {
            self._format_measurement_option(measurement): measurement
            for measurement in measurements
        }

        selected_measurement_label = st.selectbox(
            "Seleccionar evaluacion previa",
            options=list(measurement_options.keys()),
        )
        selected_measurement = measurement_options[selected_measurement_label]

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Fecha del control", selected_measurement.get("evaluation_date", "N/D"))
        with col2:
            st.metric("Clase estimada", selected_measurement.get("predicted_class", "N/D"))
        with col3:
            st.metric(
                "Confianza del modelo",
                self._format_percentage(selected_measurement.get("prediction_score")),
            )

        st.caption(
            "Usa este control como referencia para comparar nuevas mediciones del mismo caso."
        )

        with st.expander("Ver variables clinicas del control seleccionado"):
            history_tabs = st.tabs(list(self.FEATURE_GROUPS.keys()))

            for tab_index, (group_name, fields) in enumerate(self.FEATURE_GROUPS.items()):
                with history_tabs[tab_index]:
                    st.markdown(
                        f"<div class='slider-group-copy'>{self._group_description(group_name)}</div>",
                        unsafe_allow_html=True,
                    )
                    self._render_html(
                        self._build_measurement_group_table_html(selected_measurement, fields)
                    )

    def _render_existing_patient_evaluation_form(self, patient: dict) -> None:
        self._render_html(
            """
            <div class="soft-section">
                <div class="soft-section-title">Nuevo test sobre un caso previo</div>
                <div class="soft-section-subtitle">
                    Registra una nueva evaluacion clinica para este paciente y compara su lectura actual con el historial existente.
                </div>
            </div>
            """
        )

        with st.form("existing_patient_evaluation_form"):
            evaluation_date = st.date_input(
                "Fecha de evaluacion",
                value=date.today(),
            )

            measurement_data = self._render_measurement_inputs("existing")
            submitted = st.form_submit_button("Predecir caso actualizado")

        if submitted:
            self._handle_prediction_only(
                rut=patient.get("rut", ""),
                full_name=patient.get("full_name", ""),
                age=patient.get("age", 0),
                sex=patient.get("sex", ""),
                evaluation_date=evaluation_date.isoformat(),
                measurement_data=measurement_data,
                context_signature=self._build_patient_signature(
                    patient,
                    is_new_patient=False,
                ),
            )

    def _render_new_patient_form(self) -> None:
        self._render_html(
            """
            <div class="soft-section">
                <div class="soft-section-title">Ingreso de un nuevo caso</div>
                <div class="soft-section-subtitle">
                    Crea un paciente nuevo, captura sus variables clinicas y obtén una prediccion preliminar antes de persistir el registro.
                </div>
            </div>
            """
        )

        with st.form("new_patient_evaluation_form"):
            st.markdown("### Identificacion del paciente")

            col1, col2 = st.columns(2)
            with col1:
                rut = st.text_input("RUT")
                full_name = st.text_input("Nombre completo")
            with col2:
                age = st.number_input(
                    "Edad",
                    min_value=0,
                    max_value=120,
                    value=0,
                    step=1,
                )
                sex = st.selectbox(
                    "Sexo",
                    options=["F", "M", "Other"],
                    index=0,
                )

            evaluation_date = st.date_input(
                "Fecha de evaluacion",
                value=date.today(),
            )

            measurement_data = self._render_measurement_inputs("new")
            submitted = st.form_submit_button("Predecir nuevo caso")

        if submitted:
            self._handle_prediction_only(
                rut=rut,
                full_name=full_name,
                age=age,
                sex=sex,
                evaluation_date=evaluation_date.isoformat(),
                measurement_data=measurement_data,
                context_signature=self._build_patient_signature(
                    None,
                    is_new_patient=True,
                ),
            )

    def _render_measurement_inputs(self, form_prefix: str) -> dict:
        measurement_data: dict[str, float] = {}

        self._render_html(
            """
            <div class="soft-section" style="margin-top:0.8rem;">
                <div class="soft-section-title">Panel de variables clinicas</div>
                <div class="soft-section-subtitle">
                    Para una experiencia mas guiada se utilizan deslizadores por grupo de variables. Streamlit no ofrece slider vertical nativo, asi que este formato mantiene precision sin romper el diseño.
                </div>
            </div>
            """
        )

        tab_labels = list(self.FEATURE_GROUPS.keys())
        tabs = st.tabs(tab_labels)

        for tab_index, (group_name, fields) in enumerate(self.FEATURE_GROUPS.items()):
            with tabs[tab_index]:
                st.markdown(
                    f"<div class='slider-group-copy'>{self._group_description(group_name)}</div>",
                    unsafe_allow_html=True,
                )

                columns = st.columns(2, gap="large")

                for field_index, field_name in enumerate(fields):
                    metadata = FEATURE_INPUT_CONFIG.get(field_name, {})
                    label = metadata.get("label", self._format_field_label(field_name))
                    min_value = float(metadata.get("min", 0.0))
                    max_value = float(metadata.get("max", 100.0))
                    default_value = float(metadata.get("default", 0.0))
                    step_value = float(metadata.get("step", 0.01))
                    q1_value = metadata.get("q1")
                    q3_value = metadata.get("q3")

                    help_text = None
                    if q1_value is not None and q3_value is not None:
                        help_text = (
                            f"Rango observado: {min_value:.4f} a {max_value:.4f}. "
                            f"Zona tipica: {q1_value:.4f} a {q3_value:.4f}."
                        )

                    with columns[field_index % 2]:
                        measurement_data[field_name] = st.slider(
                            label=label,
                            min_value=min_value,
                            max_value=max_value,
                            value=default_value,
                            step=step_value,
                            help=help_text,
                            key=f"{form_prefix}_{field_name}_{field_index}",
                        )

        return measurement_data

    def _handle_prediction_only(
        self,
        rut: str,
        full_name: str,
        age: int,
        sex: str,
        evaluation_date: str,
        measurement_data: dict,
        context_signature: str,
    ) -> None:
        rut = str(rut).strip()
        full_name = str(full_name).strip()

        if not rut or not full_name:
            st.error("Debes ingresar RUT y nombre completo del paciente.")
            return

        patient_payload = {
            "rut": rut,
            "full_name": full_name,
            "age": int(age),
            "sex": sex,
        }

        try:
            response = self.prediction_service.predict(measurement_data)
        except RuntimeError as exc:
            st.error(f"No fue posible realizar la prediccion: {exc}")
            return

        st.session_state["patients_pending_prediction"] = response
        st.session_state["patients_pending_patient"] = patient_payload
        st.session_state["patients_pending_measurement"] = measurement_data
        st.session_state["patients_pending_date"] = evaluation_date
        st.session_state["prediction_context_signature"] = context_signature
        st.rerun()

    def _render_pending_prediction_result(self) -> None:
        prediction = st.session_state.get("patients_pending_prediction")

        if not prediction:
            return

        self._render_html(
            """
            <div class="result-box">
                <div class="result-title">Resultado del analisis actual</div>
                <div class="result-subtitle">
                    El modelo ya calculo la lectura del caso. Revisa la clase estimada, la confianza y la distribucion de probabilidades antes de confirmar el guardado.
                </div>
            </div>
            """
        )

        col1, col2, col3 = st.columns(3)

        probabilities = prediction.get("probability", [])
        benign_prob, malignant_prob = self._extract_class_probabilities(probabilities)
        confidence = max(benign_prob, malignant_prob)
        predicted_class = prediction.get("predicted_class", "N/D")
        model_version = prediction.get("model_version", "N/D")

        with col1:
            st.metric("Clase predicha", predicted_class)
        with col2:
            st.metric("Confianza", self._format_percentage(confidence))
        with col3:
            st.metric("Version del modelo", model_version)

        chart_col, info_col = st.columns([1.05, 0.95], gap="large")

        with chart_col:
            fig = self._build_risk_gauge_chart(
                malignant_prob=malignant_prob,
                predicted_class=predicted_class,
            )
            st.plotly_chart(fig, use_container_width=True)
            self._render_html(
                """
                <div class="donut-caption">
                    Indice de riesgo estimado segun la probabilidad de malignidad del caso
                </div>
                """
            )

        with info_col:
            st.metric("Probabilidad benigna", self._format_percentage(benign_prob))
            st.metric("Probabilidad maligna", self._format_percentage(malignant_prob))
            self._render_html(
                """
                <div class="soft-note">
                    Si confirmas el guardado, la evaluacion quedara disponible para el historial del paciente y para el dashboard clinico.
                </div>
                """
            )

            save_clicked = st.button(
                "Guardar evaluacion",
                key="save_pending_evaluation_button",
                type="primary",
            )

        if save_clicked:
            self._handle_save_pending_evaluation()

    def _handle_save_pending_evaluation(self) -> None:
        user_session = st.session_state.get("user")

        if not user_session:
            st.error("No se encontro la sesion del usuario autenticado.")
            return

        user_id = user_session.get("user_id")
        if user_id is None:
            st.error("No se encontro el identificador del usuario autenticado. Vuelve a iniciar sesion.")
            return

        patient_payload = st.session_state.get("patients_pending_patient")
        measurement_data = st.session_state.get("patients_pending_measurement")
        evaluation_date = st.session_state.get("patients_pending_date")

        if not patient_payload or not measurement_data or not evaluation_date:
            st.error("No se encontro una prediccion pendiente lista para guardar.")
            return

        try:
            response = self.prediction_service.predict_and_save(
                user_id=int(user_id),
                patient=patient_payload,
                measurement=measurement_data,
                evaluation_date=evaluation_date,
            )
        except RuntimeError as exc:
            st.error(f"No fue posible guardar la evaluacion: {exc}")
            return

        if response.get("success"):
            result = response.get("result", {})
            saved_patient = response.get("patient", {})

            st.success(response.get("message", "Evaluacion guardada correctamente."))

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Clase predicha", result.get("predicted_class", "N/D"))
            with col2:
                st.metric("Confianza", self._format_percentage(result.get("prediction_score")))
            with col3:
                st.metric("Modelo", result.get("model_version", "N/D"))

            st.session_state["patients_selected_patient_id"] = saved_patient.get("patient_id")
            st.session_state["records_refresh_nonce"] = st.session_state.get("records_refresh_nonce", 0) + 1
            self._clear_prediction_state()
            st.rerun()
            return

        st.error(
            response.get(
                "error",
                response.get("message", "No fue posible guardar la evaluacion."),
            )
        )

    def _build_risk_gauge_chart(
        self,
        malignant_prob: float,
        predicted_class: str,
    ) -> go.Figure:
        risk_score = round(malignant_prob * 100, 2)
        bar_color = "#e75480" if predicted_class == "Malignant" else "#7b3fc4"

        fig = go.Figure(
            go.Indicator(
                mode="gauge+number",
                value=risk_score,
                number={
                    "suffix": "%",
                    "font": {"size": 34, "color": "#3f3138"},
                },
                title={
                    "text": "Riesgo estimado",
                    "font": {"size": 22, "color": "#c2185b"},
                },
                gauge={
                    "axis": {
                        "range": [0, 100],
                        "tickwidth": 1,
                        "tickcolor": "#9a8a92",
                        "tickvals": [0, 25, 50, 75, 100],
                    },
                    "bar": {"color": bar_color, "thickness": 0.34},
                    "bgcolor": "white",
                    "borderwidth": 0,
                    "steps": [
                        {"range": [0, 35], "color": "#ffd9e5"},
                        {"range": [35, 65], "color": "#ffb5c9"},
                        {"range": [65, 100], "color": "#d8c1ff"},
                    ],
                    "threshold": {
                        "line": {"color": "#ff5a64", "width": 6},
                        "thickness": 0.78,
                        "value": risk_score,
                    },
                },
            )
        )

        fig.update_layout(
            margin=dict(t=40, b=10, l=20, r=20),
            height=320,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#4a3b47"),
        )
        return fig

    @staticmethod
    def _extract_class_probabilities(probabilities) -> tuple[float, float]:
        if not isinstance(probabilities, (list, tuple)) or len(probabilities) < 2:
            return 0.0, 0.0

        try:
            malignant_prob = float(probabilities[0])
            benign_prob = float(probabilities[1])
            total = benign_prob + malignant_prob

            if total > 0:
                benign_prob = benign_prob / total
                malignant_prob = malignant_prob / total

            return benign_prob, malignant_prob
        except (TypeError, ValueError):
            return 0.0, 0.0

    @staticmethod
    def _build_patient_signature(patient: dict | None, is_new_patient: bool) -> str:
        if is_new_patient:
            return "new_patient"

        if not patient:
            return "no_patient"

        return f"patient_{patient.get('patient_id', 'unknown')}"

    @staticmethod
    def _format_patient_option(patient: dict) -> str:
        full_name = patient.get("full_name", "Sin nombre")
        rut = patient.get("rut", "Sin RUT")
        measurements = patient.get("total_measurements", 0) or 0
        return f"{full_name} | {rut} | {measurements} evaluaciones"

    @staticmethod
    def _format_measurement_option(measurement: dict) -> str:
        evaluation_date = measurement.get("evaluation_date", "Sin fecha")
        predicted_class = measurement.get("predicted_class", "Sin resultado")
        measurement_id = measurement.get("measurement_id", "N/D")
        return f"{evaluation_date} | {predicted_class} | ID {measurement_id}"

    @staticmethod
    def _format_percentage(value) -> str:
        if value is None:
            return "N/D"

        try:
            return f"{float(value):.2%}"
        except (TypeError, ValueError):
            return str(value)

    @staticmethod
    def _format_field_label(field_name: str) -> str:
        return field_name.replace("_", " ").title()

    @staticmethod
    def _group_description(group_name: str) -> str:
        descriptions = {
            "Mediciones promedio": "Resume magnitud, forma y textura observadas en el comportamiento central del tumor.",
            "Errores estandar": "Muestra dispersion e inestabilidad de las mediciones, util para observar consistencia del caso.",
            "Peor valor observado": "Representa los valores mas extremos detectados y suele concentrar señales de mayor riesgo.",
        }
        return descriptions.get(group_name, "")

    def _build_measurement_group_table(
        self,
        measurement: dict,
        fields: list[str],
    ) -> pd.DataFrame:
        rows = [
            {
                "Variable": self._format_field_label(field_name),
                "Valor registrado": measurement.get(field_name, "N/D"),
                "Lectura": self._interpret_field_name(field_name),
            }
            for field_name in fields
        ]
        return pd.DataFrame(rows)

    def _build_measurement_group_table_html(
        self,
        measurement: dict,
        fields: list[str],
    ) -> str:
        rows_html = "".join(
            (
                "<tr>"
                f"<td class=\"measure-col-variable\">{escape(self._format_field_label(field_name))}</td>"
                f"<td class=\"measure-col-value\">{escape(str(measurement.get(field_name, 'N/D')))}</td>"
                f"<td class=\"measure-col-reading\">{escape(self._interpret_field_name(field_name))}</td>"
                "</tr>"
            )
            for field_name in fields
        )

        return dedent(
            f"""
            <div class="measure-table-shell">
                <table class="measure-table">
                    <thead>
                        <tr>
                            <th>Variable</th>
                            <th>Valor registrado</th>
                            <th>Lectura analitica</th>
                        </tr>
                    </thead>
                    <tbody>{rows_html}</tbody>
                </table>
            </div>
            """
        ).strip()

    @staticmethod
    def _interpret_field_name(field_name: str) -> str:
        interpretation_map = {
            "radius": "Tamaño radial de la lesion",
            "texture": "Variacion de intensidad superficial",
            "perimeter": "Extension del contorno",
            "area": "Magnitud total observada",
            "smoothness": "Regularidad de la superficie",
            "compactness": "Densidad y concentracion morfologica",
            "concavity": "Profundidad de zonas hundidas",
            "concave_points": "Cantidad de puntos concavos",
            "symmetry": "Equilibrio morfologico de la lesion",
            "fractal_dimension": "Complejidad del borde tumoral",
        }

        for key, description in interpretation_map.items():
            if key in field_name:
                return description

        return "Medicion clinica del modelo"
