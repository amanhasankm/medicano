import sys
import os
import numpy as np
import pandas as pd
import streamlit as st
import joblib

# Add parent directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Load model and scaler
model_path = os.path.join(os.path.dirname(__file__), '..', 'pcos_model', 'pcos_model.pkl')
scaler_path = os.path.join(os.path.dirname(__file__), '..', 'pcos_model', 'scaler.pkl')

model = joblib.load(os.path.abspath(model_path))
scaler = joblib.load(os.path.abspath(scaler_path))

# ✅ Function defined before app()
def predict_pcos(features):
    columns = ['Age', 'BMI', 'Menstrual_Irregularity', 'Testosterone_Level(ng/dL)', 'Antral_Follicle_Count']
    df = pd.DataFrame(features, columns=columns)
    scaled = scaler.transform(df)
    prediction = model.predict(scaled)
    return prediction[0]

# ✅ Main app
def app():
    st.title("🩺 PCOS Prediction Tool")

    if 'started' not in st.session_state:
        st.session_state.started = False
    if 'show_retake' not in st.session_state:
        st.session_state.show_retake = False

    if not st.session_state.started:
        st.markdown("""
        ### 📋 What is this?
        This tool estimates your risk of PCOS (Polycystic Ovary Syndrome) using basic health parameters.

        ✅ Uses a trained machine learning model  
        ✅ Easy to use & instant prediction  
        ✅ No data is stored

        ### ℹ️ Parameters Explained:
        - **BMI (Body Mass Index):** A measure of body fat based on height and weight.  
          👉 [Use this online BMI calculator](https://www.calculator.net/bmi-calculator.html)
        
        - **Testosterone Level (ng/dL):**  
          A blood test used to measure levels of the male hormone. Normal range for women: **15–70 ng/dL**.

        - **Antral Follicle Count:**  
          Measured via ultrasound. Reflects ovarian egg reserve.  
          - Normal: 8–25 follicles  
          - Low (<5): Reduced ovarian reserve  
          - High (>25): May suggest PCOS

        > ⚠️ Please consult a gynecologist for medical diagnosis.
        """)

        if st.button("🚀 Start Assessment"):
            st.session_state.started = True
            st.rerun()

    if st.session_state.started:
        st.subheader("🧬 Enter Your Health Information")

        with st.form("pcos_form"):
            age = st.number_input("Age", min_value=10, max_value=55, value=25, help="Your current age in years")
            
            bmi = st.number_input(
                "BMI (Body Mass Index)",
                min_value=10.0, max_value=50.0, value=22.5, format="%.2f",
                help="A BMI of 18.5–24.9 is considered normal. Use a calculator if needed."
            )

            menstrual_irregularity = st.radio(
                "Do you experience irregular periods?",
                options=[1, 0],
                index=0,
                help="1 = Yes, periods are irregular; 0 = No, periods are regular."
            )

            testosterone = st.number_input(
                "Testosterone Level (ng/dL)",
                min_value=10.0, max_value=200.0, value=45.0,
                help="Measured via blood test. Normal range for women: 15–70 ng/dL."
            )

            follicle_count = st.number_input(
                "Antral Follicle Count (AFC)",
                min_value=1, max_value=50, value=12,
                help="Measured via ultrasound. Normal: 8–25 follicles."
            )

            submitted = st.form_submit_button("🔍 Predict")

            if submitted:
                if age <= 0 or bmi <= 0 or testosterone <= 0 or follicle_count <= 0:
                    st.warning("⚠️ Please enter valid values for all fields.")
                else:
                    features = np.array([[age, bmi, menstrual_irregularity, testosterone, follicle_count]])
                    result = predict_pcos(features)
                    st.session_state.show_retake = True

                    if result == 1:
                        st.markdown("""
                        <div style="background-color: #f8d7da; padding: 15px; border-radius: 8px; color: #721c24; font-size: 18px;">
                        ⚠️ <strong>High Risk of PCOS Detected</strong><br>
                        Please consult your doctor for further testing and diagnosis.
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown("""
                        <div style="background-color: #d4edda; padding: 15px; border-radius: 8px; color: #155724; font-size: 18px;">
                        ✅ <strong>Low Risk of PCOS</strong><br>
                        No immediate concerns detected. Stay healthy and keep monitoring.
                        </div>
                        """, unsafe_allow_html=True)

        # Retake button
        if st.session_state.show_retake:
            if st.button("🔁 Retake Assessment"):
                st.session_state.started = False
                st.session_state.show_retake = False
                st.rerun()

    # Styling
    st.markdown("""
    <style>
        .stNumberInput label, .stRadio label, .stMarkdown {
            font-size: 16px;
        }
        .stButton button {
            background-color: #007ACC;
            color: white;
            font-size: 18px;
            border-radius: 5px;
            padding: 0.5em 1.5em;
        }
        .stButton button:hover {
            background-color: #005F9E;
        }
    </style>
    """, unsafe_allow_html=True)
