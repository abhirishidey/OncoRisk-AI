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

    # Home Page
if page == "Home":

    st.title("🏠 Welcome to OncoRisk AI")

    st.write("""
    OncoRisk AI is an AI-powered cancer risk assessment platform.

    This application estimates an individual's cancer risk
    based on lifestyle and demographic factors.

    Navigate to 'Risk Assessment' from the sidebar to begin.
    """)


# Health Chatbot Page
if page == "Health Chatbot":

    st.title("🤖 OncoAssist Chatbot")

    question = st.text_input(
        "Ask a health-related question:"
    )

    if st.button("Ask"):

        q = question.lower()

        if "smoking" in q:
            st.success(
                "Smoking is a major risk factor for several cancers."
            )

        elif "exercise" in q:
            st.success(
                "Regular physical activity may reduce cancer risk."
            )

        elif "alcohol" in q:
            st.success(
                "Excessive alcohol consumption can increase cancer risk."
            )

        elif "family" in q:
            st.success(
                "Family history can influence cancer susceptibility."
            )

        else:
            st.info(
                "Please consult a healthcare professional for personalized advice."
            )


# About Project Page
# About Project Page
if page == "About Project":

    st.title("📘 About Project")

    st.write("""
### Developer Profile

I am **Abhirishi Dey**, a fourth-year Integrated B.Tech-M.Tech student in Biotechnology with a strong interest in **Artificial Intelligence, Data Science, Bioinformatics, and Precision Medicine**.

### About OncoRisk AI

**OncoRisk AI** is an AI-powered Cancer Risk Assessment Platform developed to estimate an individual's potential cancer risk based on key demographic and lifestyle-related factors, including:

- Age
- Smoking Habits
- Alcohol Consumption
- Body Mass Index (BMI)
- Family History of Cancer
- Physical Activity Levels

This project was developed as an **end-to-end Machine Learning application**, encompassing synthetic dataset generation, data preprocessing, model development, risk prediction, and deployment through an interactive web interface.

The primary objective of this project is to integrate concepts from **Biotechnology and Artificial Intelligence** to develop a practical healthcare solution while strengthening expertise in predictive analytics and machine learning.

### Technologies Used

- Python
- NumPy
- Scikit-learn
- Streamlit
- Joblib
- Git & GitHub

### Project Objective

To create an accessible, educational, and awareness-oriented platform that demonstrates the potential application of Artificial Intelligence in personalized healthcare and cancer risk assessment.

**Note:** This application is intended solely for educational and awareness purposes and should not be used for clinical diagnosis.
    """)


# How It Works Page
if page == "How It Works":

    st.title("⚙️ How It Works")

    st.write("""
    1. User enters lifestyle information.

    2. The Machine Learning model analyzes the information.

    3. The model predicts cancer risk.

    4. The application displays:
       - Low Risk
       - Moderate Risk
       - High Risk
    """)


# Disclaimer Page
if page == "Disclaimer":

    st.title("⚠️ Disclaimer")

    st.warning("""
    This application is intended only for educational purposes.

    It is NOT a medical diagnostic tool.

    Please consult healthcare professionals for medical advice.
    """)
