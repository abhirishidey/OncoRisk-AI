import streamlit as st

st.set_page_config(
    page_title="OncoRisk AI",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

import joblib
import numpy as np
import requests
# Load trained model
model = joblib.load("cancer_model.pkl")

# Create prediction history
if "history" not in st.session_state:
    st.session_state.history = []

# Sidebar Navigation
page = st.sidebar.selectbox(
    "Navigation",
    [
        "Home",
        "Risk Assessment",
        "Prediction History",
        "Health Chatbot",
        "About Project",
        "How It Works",
        "Disclaimer"
    ]
)

# ---------------- HOME PAGE ----------------
if page == "Home":

    st.title("🧬 Welcome to OncoRisk AI")

    st.markdown("""
    ## Personalized Cancer Risk Assessment Platform

    OncoRisk AI is an Artificial Intelligence-powered healthcare application designed to estimate an individual's potential cancer risk based on demographic and lifestyle-related factors.

    ### Key Features
    ✅ AI-based Risk Assessment  
    ✅ Personalized User Profiles  
    ✅ Prediction History Tracking  
    ✅ Interactive Health Chatbot  
    ✅ Educational Healthcare Insights  

    Navigate to the **Risk Assessment** page from the sidebar to begin your assessment.
    """)

# ---------------- RISK ASSESSMENT PAGE ----------------
elif page == "Risk Assessment":

    st.title("🧬 OncoRisk AI: Personalized Cancer Risk Assessment Platform")
    st.caption("Developed by Abhirishi Dey")

    st.write(
        "Enter your lifestyle details below to estimate your cancer risk."
    )

    # Name Input
    name = st.text_input("Enter Your Name")

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
    smoking_num = 1 if smoking == "Yes" else 0
    alcohol_num = 1 if alcohol == "Yes" else 0
    family_num = 1 if family == "Yes" else 0

    if activity == "Low":
        activity_num = 0
    elif activity == "Moderate":
        activity_num = 1
    else:
        activity_num = 2

    # Prediction Button
    if st.button("Assess Risk"):

        if name.strip() == "":
            st.warning("Please enter your name.")
        else:

            data = np.array([
                [age, smoking_num, alcohol_num,
                 family_num, bmi, activity_num]
            ])

            prediction = model.predict(data)

            # Risk Label
            if prediction[0] == 0:
                risk_label = "Low Risk"
            elif prediction[0] == 1:
                risk_label = "Moderate Risk"
            else:
                risk_label = "High Risk"

            # Save Prediction History
            st.session_state.history.append({
                "Name": name,
                "Age": age,
                "Smoking": smoking,
                "Alcohol": alcohol,
                "BMI": bmi,
                "Risk": risk_label
            })

            # Display Result
            if prediction[0] == 0:
                st.success(
                    f"🟢 {name}, your estimated cancer risk is: LOW"
                )
                st.write(
                    "Maintain a healthy lifestyle and regular health check-ups."
                )

            elif prediction[0] == 1:
                st.warning(
                    f"🟠 {name}, your estimated cancer risk is: MODERATE"
                )
                st.write(
                    "Consider improving lifestyle habits and consulting healthcare professionals regularly."
                )

            else:
                st.error(
                    f"🔴 {name}, your estimated cancer risk is: HIGH"
                )
                st.write(
                    "It is recommended to consult a healthcare professional for personalized screening advice."
                )

    st.markdown("---")

    st.info(
        "Disclaimer: This application is intended for educational purposes only and should not be considered a medical diagnosis."
    )

# ---------------- PREDICTION HISTORY PAGE ----------------
elif page == "Prediction History":

    st.title("📊 Prediction History")

    if len(st.session_state.history) == 0:
        st.info("No predictions have been made yet.")
    else:
        st.table(st.session_state.history)

# ---------------- HEALTH CHATBOT PAGE ----------------
elif page == "🤖 Health Chatbot":

    st.title("🤖 OncoAssist")

    # Create conversation storage
    if "conversation_id" not in st.session_state:
        st.session_state.conversation_id = ""

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    user_query = st.text_input(
        "Ask a healthcare-related question:"
    )

    if st.button("Ask"):

        if user_query:

            API_KEY = "app-cLSVgkouuMoxkDvK7AP6oAVB"

            url = "https://api.dify.ai/v1/chat-messages"

            headers = {
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            }

            payload = {
                "inputs": {},
                "query": user_query,
                "response_mode": "blocking",
                "conversation_id": st.session_state.conversation_id,
                "user": "streamlit-user"
            }

            response = requests.post(
                url,
                headers=headers,
                json=payload
            )

            if response.status_code == 200:

                result = response.json()

                # Save conversation ID
                st.session_state.conversation_id = result.get(
                    "conversation_id", ""
                )

                answer = result["answer"]

                # Save history
                st.session_state.chat_history.append(
                    ("You", user_query)
                )

                st.session_state.chat_history.append(
                    ("OncoAssist", answer)
                )

            else:
                st.error(response.text)

    # Display full chat history
    st.markdown("---")

    for sender, message in st.session_state.chat_history:

        if sender == "You":
            st.chat_message("user").write(message)

        else:
            st.chat_message("assistant").write(message)
# ---------------- ABOUT PROJECT PAGE ----------------
elif page == "About Project":

    st.title("📘 About Project")

    st.write("""
### Developer Profile

I am **Abhirishi Dey**, a fourth-year Integrated B.Tech-M.Tech student in Biotechnology with a strong interest in Artificial Intelligence, Data Science, Bioinformatics, and Precision Medicine.

### About OncoRisk AI

**OncoRisk AI** is an AI-powered Cancer Risk Assessment Platform developed to estimate an individual's potential cancer risk based on key demographic and lifestyle-related factors, including:

- Age
- Smoking Habits
- Alcohol Consumption
- Body Mass Index (BMI)
- Family History of Cancer
- Physical Activity Levels

This project was developed as an end-to-end Machine Learning application, encompassing synthetic dataset generation, data preprocessing, model development, risk prediction, and deployment through an interactive web interface.

### Technologies Used

- Python
- NumPy
- Scikit-learn
- Streamlit
- Joblib
- Git & GitHub

### Project Objective

To create an accessible, educational, and awareness-oriented platform demonstrating the application of Artificial Intelligence in personalized healthcare and cancer risk assessment.
    """)

# ---------------- HOW IT WORKS PAGE ----------------
elif page == "How It Works":

    st.title("⚙️ How It Works")

    st.write("""
1. User enters demographic and lifestyle information.

2. The Machine Learning model analyzes the information.

3. The trained model predicts the estimated cancer risk.

4. The application categorizes users into:
   - Low Risk
   - Moderate Risk
   - High Risk

5. Personalized recommendations are displayed.
    """)

# ---------------- DISCLAIMER PAGE ----------------
elif page == "Disclaimer":

    st.title("⚠️ Disclaimer")

    st.warning("""
This application is intended solely for educational and awareness purposes.

It is NOT a medical diagnostic tool and should not be used as a substitute for professional medical advice, diagnosis, or treatment.

Users are strongly encouraged to consult qualified healthcare professionals for personalized medical guidance.
    """)
