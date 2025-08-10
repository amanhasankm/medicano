import streamlit as st
from PyPDF2 import PdfReader
import os
import requests

class ReportSummary:
    def __init__(self):
        self.api_key = os.getenv("AI71_API_KEY")

    def app(self):
        st.title("📄 Medical Report Summary (AI-Powered)")
        st.write("Upload your medical report or test results, and AI will give you a detailed, easy-to-understand explanation with suggestions.")

        uploaded_file = st.file_uploader("Upload Report", type=["pdf", "txt"])
        if uploaded_file is None:
            return

        file_type = uploaded_file.type
        st.success(f"✅ Uploaded: {uploaded_file.name}")

        # Extract text
        if file_type == "application/pdf":
            text = self.extract_text_from_pdf(uploaded_file)
        elif file_type.startswith("text/"):
            text = uploaded_file.read().decode("utf-8")
        else:
            st.error("❌ Unsupported file type.")
            return

        st.subheader("📄 Report Content:")
        st.text(text)

        # AI Summary
        st.subheader("🤖 AI Detailed Summary & Suggestions:")
        summary = self.generate_ai_summary(text)
        st.markdown(summary)

    def extract_text_from_pdf(self, file):
        text = ""
        try:
            reader = PdfReader(file)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        except Exception as e:
            st.error(f"Error reading PDF: {e}")
        return text.strip()

    def generate_ai_summary(self, text):
        """
        Uses AI71 Falcon-180B to create a detailed, user-friendly summary
        with clear suggestions for the patient.
        """
        url = "https://api.ai71.ai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "tiiuae/falcon-180b-chat",
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are a friendly and knowledgeable medical assistant. "
                        "Given a medical report, explain it in plain English that anyone can understand. "
                        "The summary should include:\n"
                        "1. A clear, non-technical explanation of the findings.\n"
                        "2. Possible causes or contributing factors.\n"
                        "3. Suggestions for lifestyle improvements.\n"
                        "4. Possible next steps or questions to ask a doctor.\n"
                        "Make it supportive, non-scary, and easy to follow."
                    )
                },
                {"role": "user", "content": f"Medical report:\n{text}"}
            ],
            "temperature": 0.6,
            "max_tokens": 1200
        }

        try:
            response = requests.post(url, headers=headers, json=payload)
            if response.status_code == 200:
                return response.json()["choices"][0]["message"]["content"]
            else:
                return f"⚠️ API request failed: {response.status_code} — {response.text}"
        except Exception as e:
            return f"⚠️ Error: {e}"
