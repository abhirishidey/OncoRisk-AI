import streamlit as st
import joblib
import numpy as np

# Load trained model
model = joblib.load("cancer_model.pkl")

# App title
st.title("🧬 OncoRisk AI: Personalized Cancer Risk Assessment Platform")
st.caption("Developed by Abhirishi Dey")


st.write(
    "Enter your lifestyle details below to estimate your cancer risk."
)

# User Inputs
age = st.slider("Age", 20, 80, 30)

smoking = st.selectbox(
    "Do you smoke?",
    ["No", "Yes"]
)

alcohol = st.selectbox(
    "Do you consume alcohol regularly?",
    ["No", "Yes"]
)

family = st.selectbox(
    "Do you have a family history of cancer?",
    ["No", "Yes"]
)

bmi = st.slider("BMI", 18.0, 40.0, 24.0)

activity = st.selectbox(
    "Physical Activity Level",
    ["Low", "Moderate", "High"]
)

# Convert text to numbers
smoking = 1 if smoking == "Yes" else 0
alcohol = 1 if alcohol == "Yes" else 0
family = 1 if family == "Yes" else 0

if activity == "Low":
    activity = 0
elif activity == "Moderate":
    activity = 1
else:
    activity = 2

# Prediction button
if st.button("Assess Risk"):

    data = np.array([
        [age, smoking, alcohol, family, bmi, activity]
    ])

    prediction = model.predict(data)

    if prediction[0] == 0:
        st.success("🟢 Estimated Risk: LOW")
        st.write("Maintain a healthy lifestyle and regular health check-ups.")

    elif prediction[0] == 1:
        st.warning("🟠 Estimated Risk: MODERATE")
        st.write("Consider improving lifestyle habits and consulting healthcare professionals regularly.")

    else:
        st.error("🔴 Estimated Risk: HIGH")
        st.write("It is recommended to consult a healthcare professional for personalized screening advice.")

st.markdown("---")

st.info(
    "Disclaimer: This application is for educational purposes only and is not intended for medical diagnosis."
)