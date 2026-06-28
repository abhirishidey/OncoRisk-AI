import streamlit as st
import joblib
import numpy as np

# Load trained model
model = joblib.load("cancer_model.pkl")
# Create prediction history
if "history" not in st.session_state:
    st.session_state.history = []
# Sidebar Navigation    
page = st.sidebar.selectbox(
    "Navigation",
    ["Home",    
     "Risk Assessment",
     "Prediction History",
     "Health Chatbot",
     "How It Works",
     "About Project",
     "Disclaimer"]
)

# App title
# Risk Assessment Page
# Risk Assessment Page
if page == "Risk Assessment":

    st.title("🧬 OncoRisk AI: Personalized Cancer Risk Assessment Platform")
    st.caption("Developed by Abhirishi Dey")

    st.write(
        "Enter your lifestyle details below to estimate your cancer risk."
    )

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

    smoking = 1 if smoking == "Yes" else 0
    alcohol = 1 if alcohol == "Yes" else 0
    family = 1 if family == "Yes" else 0

    if activity == "Low":
        activity = 0
    elif activity == "Moderate":
        activity = 1
    else:
        activity = 2

    if st.button("Assess Risk"):

        data = np.array([
            [age, smoking, alcohol, family, bmi, activity]
        ])

        prediction = model.predict(data)

        if prediction[0] == 0:
            risk_label = "Low Risk"
        elif prediction[0] == 1:
            risk_label = "Moderate Risk"
        else:
            risk_label = "High Risk"

        st.session_state.history.append({
            "Age": age,
            "Smoking": "Yes" if smoking == 1 else "No",
            "Alcohol": "Yes" if alcohol == 1 else "No",
            "BMI": bmi,
            "Risk": risk_label
        })

        if prediction[0] == 0:
            st.success("🟢 Estimated Risk: LOW")
        elif prediction[0] == 1:
            st.warning("🟠 Estimated Risk: MODERATE")
        else:
            st.error("🔴 Estimated Risk: HIGH")

    st.markdown("---")
    st.info(
        "Disclaimer: This application is for educational purposes only and is not intended for medical diagnosis."
    )

if page == "Prediction History":

    st.header("📊 Prediction History")

    if len(st.session_state.history) == 0:
        st.info("No predictions have been made yet.")

    else:
        st.table(st.session_state.history)
