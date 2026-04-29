import streamlit as st
import pandas as pd
import plotly.express as px
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))

from analysis import process_data
from calibration import train_model
from database import init_db, add_patient, get_patients

# -------- INIT --------
init_db()

# -------- LOGIN --------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("Physician Login")

    user = st.text_input("Username")
    pw = st.text_input("Password", type="password")

    if st.button("Login"):
        if authenticate(user, pw):
            st.session_state.logged_in = True
            st.success("Logged in")
            st.rerun()   # 🔥 IMPORTANT
        else:
            st.error("Invalid credentials")

    st.stop()

# -------- MAIN APP --------
st.title("Patient Monitoring System")

# -------- PATIENT MANAGEMENT --------
st.subheader("Patients")

new_patient = st.text_input("New Patient Name")

if st.button("Add Patient"):
    if new_patient.strip():
        add_patient(new_patient)
        st.success("Patient added")

patients = get_patients()
patient_names = [p[1] for p in patients] if patients else []

selected_patient = st.selectbox("Select Patient", patient_names) if patient_names else None

# -------- DATA UPLOAD --------
st.subheader("Upload Data")

uploaded_file = st.file_uploader("Upload OpenLog CSV", type=["csv", "txt"])

if uploaded_file:
    df = process_data(uploaded_file)

    st.success("Data processed")

    # -------- THRESHOLD --------
    threshold = st.slider("Threshold Angle (degrees)", 0.0, 15.0, 5.0)

    # -------- PLOT --------
    fig = px.line(
        df,
        x="time",
        y="angle",
        title="Angle vs Time"
    )

    fig.update_layout(
        xaxis_title="Time (ms)",
        yaxis_title="Angle (degrees)"
    )

    # Add threshold line
    fig.add_hline(
        y=threshold,
        line_dash="dash",
        annotation_text="Threshold",
        annotation_position="top right"
    )

    # Make line thicker (nicer visuals)
    fig.update_traces(line=dict(width=3))

    st.plotly_chart(fig)

    # -------- ALERTS --------
    alerts = df[df["angle"] > threshold]

    if not alerts.empty:
        st.error(f"⚠ {len(alerts)} points exceed threshold")

    # -------- TREND --------
    if df["trend"].iloc[-1] > 0:
        st.warning("⚠ Condition worsening (increasing trend)")
    else:
        st.success("Stable or improving trend")

    # -------- RAW DATA --------
    with st.expander("View Raw Data"):
        st.dataframe(df)
