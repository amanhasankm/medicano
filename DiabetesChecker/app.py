import streamlit as st
import joblib
import numpy as np
import os

# Load model once at startup
MODEL_PATH = os.path.join(os.path.dirname(__file__), "diabetes_pipeline.joblib")
if not os.path.exists(MODEL_PATH):
    st.error("Model file not found. Please run train_diabetes.py first.")
    st.stop()

model = joblib.load(MODEL_PATH)

def app():
    st.title("🩸 Diabetes Risk Checker (ML Powered)")
    st.markdown("### Enter your health metrics:")

    pregnancies = st.number_input("Pregnancies", 0, 20, 1)
    glucose = st.number_input("Glucose Level", 0, 300, 110)
    blood_pressure = st.number_input("Blood Pressure", 0, 180, 70)
    skin_thickness = st.number_input("Skin Thickness", 0, 100, 20)
    insulin = st.number_input("Insulin Level", 0, 900, 85)
    bmi = st.number_input("BMI", 0.0, 70.0, 24.0)
    diabetes_pedigree = st.number_input("Diabetes Pedigree Function", 0.0, 2.5, 0.5)
    age = st.number_input("Age", 1, 100, 30)

    if st.button("🔍 Predict"):
        # Prepare input in the right shape
        features = np.array([[pregnancies, glucose, blood_pressure, skin_thickness,
                              insulin, bmi, diabetes_pedigree, age]])
        
        prediction = model.predict(features)[0]
        probability = model.predict_proba(features)[0][1]  # Probability of diabetes

        if prediction == 1:
            st.error(f"⚠️ You may be at risk of diabetes. Probability: {probability:.2%}")
        else:
            st.success(f"✅ You are likely not diabetic. Probability: {probability:.2%}")

