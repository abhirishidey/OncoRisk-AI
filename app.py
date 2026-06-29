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
```python
# ---------------- HOME PAGE ----------------
if page == "Home":

    try:
        image = Image.open("hero.png")
        st.image(image, use_container_width=True)
    except:
        st.warning("Hero image not found.")

    st.markdown("""
    <div style='text-align:center; padding:20px;'>

        <h1 style='font-size:65px;
                   color:#38bdf8;
                   font-weight:800;'>
            🧬 OncoRisk AI
        </h1>

        <h3 style='color:#cbd5e1;'>
            Personalized Cancer Risk Assessment Platform
        </h3>

        <p style='font-size:20px;
                  color:#94a3b8;'>
            Developed by <b>Abhirishi Dey</b>
        </p>

    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.info("""
        ### 🧠 AI-Powered Prediction

        Advanced Machine Learning algorithms analyze lifestyle and demographic factors to estimate cancer risk.
        """)

    with col2:
        st.info("""
        ### 📊 Prediction History

        Securely review and track previous cancer risk assessments.
        """)

    with col3:
        st.info("""
        ### 🤖 OncoAssist Chatbot

        Interact with an AI-powered healthcare assistant for educational insights.
        """)

    st.markdown("---")

    st.info(
        "👈 Use the navigation panel on the left to access Risk Assessment, Prediction History, and OncoAssist."
    )

    st.markdown("""
    <div style='text-align:center; color:gray;'>
        <p>Integrating Artificial Intelligence and Healthcare for Personalized Risk Assessment</p>
    </div>
    """, unsafe_allow_html=True)
```


# ---------------- PREDICTION HISTORY PAGE ----------------
elif page == "Prediction History":

    st.title("📊 Prediction History")

    if len(st.session_state.history) == 0:
        st.info("No predictions have been made yet.")
    else:
        st.table(st.session_state.history)

# ---------------- HEALTH CHATBOT PAGE ----------------
elif page == "Health Chatbot":

    st.title("🤖 OncoAssist")
    st.caption("AI-powered healthcare assistant")

    # Create storage for conversation
    if "conversation_id" not in st.session_state:
        st.session_state.conversation_id = ""

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display previous chat history
    for msg in st.session_state.messages:

        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # Chat input (automatically clears after sending)
    user_query = st.chat_input(
        "Ask a healthcare-related question..."
    )

    if user_query:

        # Show user message immediately
        st.session_state.messages.append(
            {"role": "user", "content": user_query}
        )

        with st.chat_message("user"):
            st.write(user_query)

        API_KEY = "app-SO5ookGZ44xOm8k1qxJOrKJm"

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

            answer = result.get(
                "answer",
                "No answer received."
            )

            # Save assistant response
            st.session_state.messages.append(
                {"role": "assistant", "content": answer}
            )

            with st.chat_message("assistant"):
                st.write(answer)

        else:
            st.error(
                f"Error {response.status_code}: {response.text}"
            )

    st.markdown("---")

    # Clear chat button
    if st.button("🗑️ Clear Chat History"):

        st.session_state.messages = []
        st.session_state.conversation_id = ""
        st.rerun()

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
