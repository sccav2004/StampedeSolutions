import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))

import streamlit as st
import pandas as pd
from analysis import process_data
from calibration import train_model
from database import init_db, add_patient, get_patients
from auth import authenticate

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
        else:
            st.error("Invalid credentials")

    st.stop()

# -------- MAIN APP --------
st.title("Patient Monitoring System")

# -------- PATIENT MANAGEMENT --------
st.subheader("Patients")

new_patient = st.text_input("New Patient Name")

if st.button("Add Patient"):
    add_patient(new_patient)
    st.success("Patient added")

patients = get_patients()
patient_names = [p[1] for p in patients]

selected_patient = st.selectbox("Select Patient", patient_names)

# -------- CALIBRATION --------
st.subheader("Calibration")

cal_file = st.file_uploader("Upload Calibration CSV (diff, angle)", key="cal")

if cal_file:
    train_model(cal_file)
    st.success("Model trained!")

# -------- DATA UPLOAD --------
st.subheader("Upload Data")

uploaded_file = st.file_uploader("Upload OpenLog CSV", type=["csv", "txt"])

if uploaded_file:
    df = process_data(uploaded_file)

    st.success("Data processed")

    # -------- METRICS --------
    st.subheader("Analysis")

    st.line_chart(df["angle"])

    threshold = st.slider("Threshold Angle", 0.0, 90.0, 30.0)

    alerts = df[df["angle"] > threshold]

    if not alerts.empty:
        st.error(f"⚠ {len(alerts)} alerts")

    if df["trend"].iloc[-1] > 0:
        st.warning("Condition worsening")