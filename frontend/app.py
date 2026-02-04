
import streamlit as st
import requests
import pandas as pd

BACKEND_URL = "https://smartops-backend-dt2f.onrender.com"

def safe_post(url, data):
    try:
        r = requests.post(url, data=data, timeout=30)

        # Backend down / cold start
        if r.status_code != 200:
            return None, f"Server error ({r.status_code}). Please try again."

        # Try parsing JSON safely
        try:
            return r.json(), None
        except Exception:
            return None, "Backend is starting up. Please wait 10–20 seconds and try again."

    except requests.exceptions.RequestException:
        return None, "Cannot connect to backend. Please try again."

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if not st.session_state.logged_in:
    st.title("Login")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Login"):
            data, error = safe_post(
                f"{BACKEND_URL}/login/",
                {"email": email, "password": password}
            )

            if error:
                st.warning(error)
            elif data.get("success"):
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Invalid credentials")

    with col2:
        if st.button("Register"):
            data, error = safe_post(
                f"{BACKEND_URL}/register/",
                {"email": email, "password": password}
            )

            if error:
                st.warning(error)
            elif "error" in data:
                st.error(data["error"])
            else:
                st.success("Registered successfully. Please login.")

    st.stop()


st.set_page_config(page_title="SmartOps AI", layout="wide")



st.title("📊 SmartOps AI - Business Data to Decisions")

# Model selection
model_choice = st.selection(
    "Choose ML Model",
    options=[
        "random_forest",
        "logistic",
        "linear"
    ]
)



uploaded_file = st.file_uploader("Upload your business CSV file", type=["csv"])

if uploaded_file:
    with st.spinner("Processing data with AI..."):
        files = {"file": uploaded_file}
        data = {"model_choice": model_choice}
        response = requests.post(f"{BACKEND_URL}/upload/", files=files, data=data)

    # Safety check
    if response.status_code != 200:
        st.error("Backend error occurred")
        st.text(response.text)
        st.stop()

    result = response.json()

    # Dataset info
    st.success("File processed successfully")

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Rows", result["rows"])
    with col2:
        st.metric("Columns", len(result["columns"]))

    # Model results
    st.write("### 🤖 AI Model Result")
    st.json(result["model_result"])

    # Feature importance chart
    st.write("### 📈 Feature Importance")
    fi = result["model_result"]["feature_importance"]
    fi_df = pd.DataFrame(
        list(fi.items()), columns=["Feature", "Importance"]
    ).set_index("Feature")
    st.bar_chart(fi_df)

    # Business insight
    st.write("### 🧠 AI Business Insight")
    st.info(result["model_result"]["insight"])

    # Report download (HTTP, not filesystem)
    st.write("### 📄 Download Business Report")
    st.markdown(
        f"[⬇️ Click here to download the report]({BACKEND_URL}/download-report/)",
        unsafe_allow_html=True
    )
