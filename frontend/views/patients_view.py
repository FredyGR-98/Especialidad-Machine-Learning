"""
===========================================================
patients_view.py
===========================================================

Vista del módulo de pacientes.

Responsabilidades:
- Seleccionar pacientes registrados desde una lista.
- Permitir registrar un paciente nuevo.
- Mostrar datos básicos del paciente seleccionado.
- Mostrar historial clínico por fechas.
- Permitir registrar una nueva evaluación clínica.
- Ejecutar predicción previa sin guardar.
- Guardar el nuevo registro solo tras confirmación del usuario.

Esta vista cumple el rol operativo principal del sistema.
===========================================================
"""

from datetime import date
from html import escape
from textwrap import dedent

import plotly.graph_objects as go
import streamlit as st

from services.patient_service import PatientService
from services.prediction_service import PredictionService
from utils.feature_config import FEATURE_INPUT_CONFIG


class PatientsView:
    """
    Renderiza la sección operativa de pacientes y evaluaciones.
    """

    NEW_PATIENT_OPTION = "➕ Ingresar nuevo paciente"

    FEATURE_FIELDS = [
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
    ]

    def __init__(self, api_client) -> None:
        self.patient_service = PatientService(api_client)
        self.prediction_service = PredictionService(api_client)

    def render(self) -> None:
        """
        Renderiza el contenido principal de la vista de pacientes.
        """
        self._inject_styles()
        self._initialize_state()
        self._render_header()

        selected_patient = self._render_patient_selector()
        is_new_patient = selected_patient is None

        current_patient_signature = self._build_patient_signature(
            selected_patient,
            is_new_patient
        )

        if st.session_state.get("prediction_context_signature") != current_patient_signature:
            self._clear_prediction_state()

        if not is_new_patient:
            self._render_patient_summary_card(selected_patient)
            self._render_patient_history(selected_patient)
            self._render_existing_patient_evaluation_form(selected_patient)
        else:
            self._render_new_patient_form()

        self._render_pending_prediction_result()

    def _render_html(self, html_content: str) -> None:
        """
        Renderiza HTML limpiando indentación para evitar que Streamlit/Markdown
        interprete fragmentos como bloques de código.
        """
        st.markdown(dedent(html_content).strip(), unsafe_allow_html=True)

    def _inject_styles(self) -> None:
        """
        Inyecta estilos visuales locales para la vista.
        """
        self._render_html(
            """
            <style>
            .patients-hero {
                background: linear-gradient(135deg, #fff6fa 0%, #fdebf3 100%);
                border: 1px solid #f6c7d7;
                border-radius: 26px;
                padding: 28px 30px;
                margin-bottom: 1.4rem;
                box-shadow: 0 10px 28px rgba(231, 84, 128, 0.07);
            }

            .patients-hero h1 {
                color: #c2185b;
                font-size: 2.35rem;
                font-weight: 800;
                margin: 0 0 0.55rem 0;
                line-height: 1.15;
            }

            .patients-hero p {
                color: #5d4c57;
                font-size: 1rem;
                line-height: 1.75;
                margin: 0;
            }

            .soft-section {
                background: #ffffff;
                border: 1px solid #f3c9d9;
                border-radius: 24px;
                padding: 22px 24px;
                margin-bottom: 1.2rem;
                box-shadow: 0 8px 22px rgba(231, 84, 128, 0.05);
            }

            .soft-section-title {
                color: #c2185b;
                font-size: 1.55rem;
                font-weight: 800;
                margin-bottom: 0.35rem;
            }

            .soft-section-subtitle {
                color: #6d5863;
                font-size: 0.98rem;
                line-height: 1.65;
            }

            .summary-card {
                background: #fff9fc;
                border: 1px solid #f4d4e1;
                border-radius: 20px;
                padding: 18px 20px;
                box-shadow: 0 7px 18px rgba(231, 84, 128, 0.04);
                min-height: 170px;
            }

            .summary-label {
                color: #7b6771;
                font-size: 0.9rem;
                margin-bottom: 0.25rem;
            }

            .summary-value {
                color: #4a3b47;
                font-size: 1.02rem;
                font-weight: 700;
                margin-bottom: 0.9rem;
                line-height: 1.35;
                word-break: break-word;
            }

            .result-box {
                background: linear-gradient(135deg, #fff6fa 0%, #fffafb 100%);
                border: 1px solid #f3c9d9;
                border-radius: 24px;
                padding: 22px 24px;
                margin-top: 1.2rem;
                box-shadow: 0 10px 26px rgba(231, 84, 128, 0.06);
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
                line-height: 1.65;
                margin-bottom: 1rem;
            }

            .soft-note {
                background: #fff4f8;
                border-left: 5px solid #e75480;
                border-radius: 14px;
                padding: 14px 16px;
                color: #5d4c57;
                line-height: 1.65;
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

            div[data-testid="stSelectbox"] label,
            div[data-testid="stDateInput"] label,
            div[data-testid="stNumberInput"] label,
            div[data-testid="stTextInput"] label {
                color: #5d4c57 !important;
                font-weight: 600 !important;
            }

            div[data-testid="stForm"] {
                background: #ffffff;
                border: 1px solid #f3c9d9;
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

            div[data-testid="stButton"] > button:hover,
            div[data-testid="stFormSubmitButton"] > button:hover {
                filter: brightness(1.03);
            }

            .donut-caption {
                text-align: center;
                color: #7a6571;
                font-size: 0.92rem;
                margin-top: -0.3rem;
            }
            </style>
            """
        )

    def _render_header(self) -> None:
        """
        Renderiza el encabezado principal de la vista.
        """
        self._render_html(
            """
            <div class="patients-hero">
                <h1>Gestión de Pacientes</h1>
                <p>
                    En esta sección puedes seleccionar pacientes registrados,
                    revisar su historial clínico, ingresar nuevas evaluaciones
                    y ejecutar una predicción previa antes de guardar el resultado
                    en la base de datos.
                </p>
            </div>
            """
        )

    def _initialize_state(self) -> None:
        """
        Inicializa las claves de sesión necesarias para la vista.
        """
        defaults = {
            "patients_pending_prediction": None,
            "patients_pending_patient": None,
            "patients_pending_measurement": None,
            "patients_pending_date": None,
            "prediction_context_signature": None,
        }

        for key, value in defaults.items():
            if key not in st.session_state:
                st.session_state[key] = value

    def _clear_prediction_state(self) -> None:
        """
        Limpia la predicción pendiente almacenada en sesión.
        """
        st.session_state["patients_pending_prediction"] = None
        st.session_state["patients_pending_patient"] = None
        st.session_state["patients_pending_measurement"] = None
        st.session_state["patients_pending_date"] = None
        st.session_state["prediction_context_signature"] = None

    def _render_patient_selector(self) -> dict | None:
        """
        Renderiza el selector principal de paciente.

        Returns:
            dict | None: Paciente seleccionado o None si se eligió
            la opción de nuevo paciente.
        """
        self._render_html(
            """
            <div class="soft-section">
                <div class="soft-section-title">Selección de paciente</div>
                <div class="soft-section-subtitle">
                    Puedes trabajar con un paciente ya registrado o ingresar uno nuevo.
                </div>
            </div>
            """
        )

        try:
            response = self.patient_service.get_patients()
            patients = response.get("patients", [])
        except RuntimeError as exc:
            st.error(f"No fue posible cargar pacientes: {exc}")
            return None

        patient_options = {self.NEW_PATIENT_OPTION: None}

        for patient in patients:
            label = self._format_patient_option(patient)
            patient_options[label] = patient

        selected_label = st.selectbox(
            "Seleccionar paciente",
            options=list(patient_options.keys()),
        )

        return patient_options[selected_label]

    def _render_patient_summary_card(self, patient: dict) -> None:
        """
        Renderiza la ficha resumen del paciente seleccionado.
        """
        self._render_html(
            """
            <div class="soft-section">
                <div class="soft-section-title">Resumen del paciente</div>
                <div class="soft-section-subtitle">
                    Datos básicos del paciente actualmente seleccionado.
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
                    <div class="summary-label">RUT</div>
                    <div class="summary-value">{rut}</div>
                    <div class="summary-label">Nombre completo</div>
                    <div class="summary-value">{full_name}</div>
                </div>
                """
            )

        with col2:
            self._render_html(
                f"""
                <div class="summary-card">
                    <div class="summary-label">Sexo</div>
                    <div class="summary-value">{sex}</div>
                    <div class="summary-label">Edad</div>
                    <div class="summary-value">{age}</div>
                </div>
                """
            )

        with col3:
            self._render_html(
                f"""
                <div class="summary-card">
                    <div class="summary-label">Evaluaciones registradas</div>
                    <div class="summary-value">{total_measurements}</div>
                    <div class="summary-label">Última evaluación</div>
                    <div class="summary-value">{last_eval}</div>
                </div>
                """
            )

    def _render_patient_history(self, patient: dict) -> None:
        """
        Renderiza el historial clínico del paciente seleccionado.
        """
        self._render_html(
            """
            <div class="soft-section">
                <div class="soft-section-title">Historial clínico</div>
                <div class="soft-section-subtitle">
                    Revisa evaluaciones previas y consulta el detalle de sus variables.
                </div>
            </div>
            """
        )

        patient_id = patient.get("patient_id")

        if not patient_id:
            st.warning("No se encontró el identificador del paciente.")
            return

        try:
            response = self.patient_service.get_patient_measurements(patient_id)
            measurements = response.get("measurements", [])
        except RuntimeError as exc:
            st.error(f"No fue posible cargar el historial clínico: {exc}")
            return

        if not measurements:
            st.info("Este paciente aún no registra evaluaciones clínicas.")
            return

        measurement_options = {
            self._format_measurement_option(measurement): measurement
            for measurement in measurements
        }

        selected_measurement_label = st.selectbox(
            "Seleccionar evaluación por fecha",
            options=list(measurement_options.keys()),
        )

        selected_measurement = measurement_options[selected_measurement_label]

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Fecha evaluación",
                selected_measurement.get("evaluation_date", "N/D"),
            )
        with col2:
            st.metric(
                "Clase predicha",
                selected_measurement.get("predicted_class", "N/D"),
            )
        with col3:
            score = selected_measurement.get("prediction_score")
            st.metric("Confianza", self._format_percentage(score))

        with st.expander("Ver variables clínicas registradas"):
            for field in self.FEATURE_FIELDS:
                value = selected_measurement.get(field, "N/D")
                st.write(f"**{self._format_field_label(field)}:** {value}")

    def _render_existing_patient_evaluation_form(self, patient: dict) -> None:
        """
        Renderiza el formulario de nueva evaluación para un paciente existente.
        """
        self._render_html(
            """
            <div class="soft-section">
                <div class="soft-section-title">Nueva evaluación clínica</div>
                <div class="soft-section-subtitle">
                    Se registrará una nueva evaluación para el paciente seleccionado.
                </div>
            </div>
            """
        )

        with st.form("existing_patient_evaluation_form"):
            evaluation_date = st.date_input(
                "Fecha de evaluación",
                value=date.today(),
            )

            st.markdown("### Variables clínicas")
            measurement_data = self._render_measurement_inputs("existing")

            submitted = st.form_submit_button("Predecir")

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
                    is_new_patient=False
                ),
            )

    def _render_new_patient_form(self) -> None:
        """
        Renderiza el formulario completo para registrar un paciente nuevo.
        """
        self._render_html(
            """
            <div class="soft-section">
                <div class="soft-section-title">Nuevo paciente y primera evaluación</div>
                <div class="soft-section-subtitle">
                    Completa los datos del nuevo paciente y luego realiza una predicción
                    previa antes de guardar.
                </div>
            </div>
            """
        )

        with st.form("new_patient_evaluation_form"):
            st.markdown("### Datos del paciente")

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
                    options=["F", "M"],
                    index=0,
                )

            evaluation_date = st.date_input(
                "Fecha de evaluación",
                value=date.today(),
            )

            st.markdown("### Variables clínicas")
            measurement_data = self._render_measurement_inputs("new")

            submitted = st.form_submit_button("Predecir")

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
                    is_new_patient=True
                ),
            )

    def _render_measurement_inputs(self, form_prefix: str) -> dict:
        """
        Renderiza los inputs de las 30 variables clínicas.
        """
        measurement_data = {}
        columns = st.columns(3)

        for index, field in enumerate(self.FEATURE_FIELDS):
            metadata = FEATURE_INPUT_CONFIG.get(field, {})

            label = metadata.get("label", self._format_field_label(field))
            min_value = float(metadata.get("min", 0.0))
            max_value = float(metadata.get("max", 100.0))
            default_value = float(metadata.get("default", 0.0))
            step_value = float(metadata.get("step", 0.01))
            q1_value = metadata.get("q1")
            q3_value = metadata.get("q3")

            help_text = None
            if q1_value is not None and q3_value is not None:
                help_text = (
                    f"Rango observado: {min_value:.4f} a {max_value:.4f} | "
                    f"Zona típica: {q1_value:.4f} a {q3_value:.4f}"
                )

            with columns[index % 3]:
                measurement_data[field] = st.number_input(
                    label=label,
                    min_value=min_value,
                    max_value=max_value,
                    value=default_value,
                    step=step_value,
                    format="%.5f",
                    help=help_text,
                    key=f"{form_prefix}_{field}_{index}",
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
        """
        Ejecuta una predicción preliminar sin guardar en base de datos.
        """
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
            st.error(f"No fue posible realizar la predicción: {exc}")
            return

        st.session_state["patients_pending_prediction"] = response
        st.session_state["patients_pending_patient"] = patient_payload
        st.session_state["patients_pending_measurement"] = measurement_data
        st.session_state["patients_pending_date"] = evaluation_date
        st.session_state["prediction_context_signature"] = context_signature

        st.rerun()

    def _render_pending_prediction_result(self) -> None:
        """
        Muestra el resultado de una predicción pendiente y habilita
        el botón para guardar la evaluación.
        """
        prediction = st.session_state.get("patients_pending_prediction")

        if not prediction:
            return

        self._render_html(
            """
            <div class="result-box">
                <div class="result-title">Resultado de la predicción</div>
                <div class="result-subtitle">
                    La predicción ya fue calculada. A continuación puedes revisar
                    la clase estimada, su nivel de confianza y la distribución
                    de probabilidades antes de guardar la evaluación.
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
            st.metric("Modelo", model_version)

        chart_col, info_col = st.columns([1.1, 1])

        with chart_col:
            fig = self._build_probability_donut_chart(
                benign_prob=benign_prob,
                malignant_prob=malignant_prob,
            )
            st.plotly_chart(fig, use_container_width=True)
            self._render_html(
                """
                <div class='donut-caption'>
                    Distribución estimada de probabilidad diagnóstica
                </div>
                """
            )

        with info_col:
            st.metric("Probabilidad benigno", self._format_percentage(benign_prob))
            st.metric("Probabilidad maligno", self._format_percentage(malignant_prob))

            self._render_html(
                """
                <div class="soft-note">
                    Revisa el resultado antes de confirmar el guardado. Esta acción
                    registrará la evaluación clínica y su predicción en la base de datos.
                </div>
                """
            )

            save_clicked = st.button(
                "Guardar evaluación",
                key="save_pending_evaluation_button",
                type="primary",
            )

        if save_clicked:
            self._handle_save_pending_evaluation()

    def _handle_save_pending_evaluation(self) -> None:
        """
        Guarda una evaluación previamente predicha.
        """
        user_session = st.session_state.get("user")

        if not user_session:
            st.error("No se encontró la sesión del usuario autenticado.")
            return

        user_id = user_session.get("user_id")

        if user_id is None:
            st.error(
                "No se encontró el identificador del usuario autenticado. "
                "Vuelve a iniciar sesión."
            )
            return

        patient_payload = st.session_state.get("patients_pending_patient")
        measurement_data = st.session_state.get("patients_pending_measurement")
        evaluation_date = st.session_state.get("patients_pending_date")

        if not patient_payload or not measurement_data or not evaluation_date:
            st.error("No se encontró una predicción pendiente lista para guardar.")
            return

        try:
            response = self.prediction_service.predict_and_save(
                user_id=int(user_id),
                patient=patient_payload,
                measurement=measurement_data,
                evaluation_date=evaluation_date,
            )
        except RuntimeError as exc:
            st.error(f"No fue posible guardar la evaluación: {exc}")
            return

        if response.get("success"):
            result = response.get("result", {})

            st.success(response.get("message", "Evaluación guardada correctamente."))

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("Clase predicha", result.get("predicted_class", "N/D"))
            with col2:
                st.metric(
                    "Confianza",
                    self._format_percentage(result.get("prediction_score")),
                )
            with col3:
                st.metric("Modelo", result.get("model_version", "N/D"))

            self._clear_prediction_state()
            st.rerun()
            return

        st.error(
            response.get(
                "error",
                response.get("message", "No fue posible guardar la evaluación.")
            )
        )

    def _build_probability_donut_chart(
        self,
        benign_prob: float,
        malignant_prob: float,
    ) -> go.Figure:
        """
        Construye el donut chart de probabilidades.
        """
        fig = go.Figure(
            data=[
                go.Pie(
                    labels=["Benigno", "Maligno"],
                    values=[benign_prob, malignant_prob],
                    hole=0.62,
                    marker=dict(colors=["#f8bbd0", "#e75480"]),
                    textinfo="percent",
                    hovertemplate="%{label}: %{percent}<extra></extra>",
                )
            ]
        )

        fig.update_layout(
            margin=dict(t=10, b=10, l=10, r=10),
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.15,
                xanchor="center",
                x=0.5,
            ),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#4a3b47"),
        )

        return fig

    @staticmethod
    def _extract_class_probabilities(probabilities) -> tuple[float, float]:
        """
        Extrae probabilidades de benigno y maligno desde la respuesta.

        Se asume el orden clásico del dataset de sklearn:
        [malignant, benign].
        """
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
        """
        Construye una firma simple del contexto actual de paciente.
        """
        if is_new_patient:
            return "new_patient"

        if not patient:
            return "no_patient"

        return f"patient_{patient.get('patient_id', 'unknown')}"

    @staticmethod
    def _format_patient_option(patient: dict) -> str:
        """
        Construye una etiqueta legible para el selectbox de pacientes.
        """
        full_name = patient.get("full_name", "Sin nombre")
        rut = patient.get("rut", "Sin RUT")
        return f"{full_name} | {rut}"

    @staticmethod
    def _format_measurement_option(measurement: dict) -> str:
        """
        Construye una etiqueta legible para el selectbox de historial.
        """
        evaluation_date = measurement.get("evaluation_date", "Sin fecha")
        predicted_class = measurement.get("predicted_class", "Sin resultado")
        measurement_id = measurement.get("measurement_id", "N/D")
        return f"{evaluation_date} | {predicted_class} | ID {measurement_id}"

    @staticmethod
    def _format_percentage(value) -> str:
        """
        Formatea un valor numérico como porcentaje.
        """
        if value is None:
            return "N/D"

        try:
            return f"{float(value):.2%}"
        except (TypeError, ValueError):
            return str(value)

    @staticmethod
    def _format_field_label(field_name: str) -> str:
        """
        Convierte el nombre interno de una variable a una etiqueta
        más legible para la interfaz.
        """
        return field_name.replace("_", " ").title()