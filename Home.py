import streamlit as st
import time

# Import sub-feature apps
from PCOS.pcospredicter.pcos_predicter import app as PCOSApp
from PCOS.Diet_Plan_Generator.dietplanner import app as DP
from PCOS.PCOS_Type_Classifier.classifier import app as PCOSTypeClassifier
from RPPG.app import app as RPPGApp
from DiabetesChecker import app as DiabetesCheckerApp
from ReportSummary.app import ReportSummary  # <-- Import Report Summary feature

class Homes:
    @staticmethod
    def app():
        if "selected_feature" not in st.session_state:
            st.session_state.selected_feature = None
        if "pcos_subfeature" not in st.session_state:
            st.session_state.pcos_subfeature = None

        # Back to Home Button
        if st.session_state.selected_feature:
            if st.button("🔙 Back to Home", key="top_back_button"):
                st.session_state.selected_feature = None
                st.session_state.pcos_subfeature = None
                st.rerun()

        # Header Styling
        st.markdown("""
        <style>
        .header-container {
            background: linear-gradient(135deg, #003366, #006699);
            border-radius: 10px;
            padding: 30px 20px;
            text-align: center;
            margin-bottom: 30px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        }
        .header-container h1 { color: white; font-size: 60px; margin-bottom: 10px; }
        .header-container h2 { color: #e0e0e0; font-size: 22px; }
        .stButton button {
            width: 100%; height: 80px; font-size: 24px;
            background-color: #006699; color: white;
            border-radius: 10px; border: none;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        }
        .stButton button:hover {
            background-color: #004466;
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
        }
        </style>
        """, unsafe_allow_html=True)

        # Header Content
        st.markdown("""
        <div class="header-container">
            <h1>Medicano</h1>
            <h2>A Smart Medical Assistant</h2>
        </div>
        """, unsafe_allow_html=True)

        # Selected Feature Logic
        if st.session_state.selected_feature == "PCOS":
            st.subheader("💊 PCOS Tools")

            # PCOS Info Card
            st.markdown("""
            <div style="background-color: #f9f9f9; padding: 20px; border-left: 6px solid #006699; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); margin-bottom: 25px;">
                <h3 style="color:#003366;">What is PCOS?</h3>
                <p>Polycystic Ovary Syndrome (PCOS) is a common hormonal disorder affecting women of reproductive age.</p>
                <ul>
                    <li><strong>Symptoms:</strong> Acne, weight gain, irregular periods.</li>
                    <li><strong>Risks:</strong> Infertility, diabetes, heart disease.</li>
                    <li><strong>Management:</strong> Diet, exercise, medication.</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

            # PCOS Sub-feature Buttons
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🧬 PCOS Predictor"):
                    st.session_state.pcos_subfeature = "predictor"
                    st.rerun()
                if st.button("🔍 PCOS Type Classifier"):
                    st.session_state.pcos_subfeature = "type_classifier"
                    st.rerun()
            with col2:
                if st.button("🥗 Diet Plan Generator"):
                    st.session_state.pcos_subfeature = "diet"
                    st.rerun()

            if st.session_state.pcos_subfeature == "predictor":
                with st.spinner("Loading PCOS Predictor..."):
                    time.sleep(1)
                    PCOSApp()
            elif st.session_state.pcos_subfeature == "diet":
                with st.spinner("Loading Diet Plan Generator..."):
                    time.sleep(1)
                    DP()
            elif st.session_state.pcos_subfeature == "type_classifier":
                with st.spinner("Loading PCOS Type Classifier..."):
                    time.sleep(1)
                    PCOSTypeClassifier()

        elif st.session_state.selected_feature == "RPPG":
            with st.spinner("Loading RPPG..."):
                time.sleep(1.5)
                RPPGApp()

        elif st.session_state.selected_feature == "Diabetes":
            with st.spinner("Loading Diabetes Checker..."):
                time.sleep(1.5)
                DiabetesCheckerApp()

        elif st.session_state.selected_feature == "ReportSummary":
            with st.spinner("Loading Report Summary..."):
                time.sleep(1)
                ReportSummary().app()

        else:
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🩺 RPPG"):
                    st.session_state.selected_feature = "RPPG"
                    st.rerun()
                if st.button("🩸 Diabetes Check"):
                    st.session_state.selected_feature = "Diabetes"
                    st.rerun()
            with col2:
                if st.button("🧬 PCOS Management"):
                    st.session_state.selected_feature = "PCOS"
                    st.rerun()
                if st.button("📄 Report Summary"):
                    st.session_state.selected_feature = "ReportSummary"
                    st.rerun()
