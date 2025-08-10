import streamlit as st
from ai71 import AI71
import os
from dotenv import load_dotenv

def chatbot_ui():
    load_dotenv()

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    AI71_API_KEY = os.getenv("AI71_API_KEY")
    if not AI71_API_KEY:
        st.error("❌ AI71 API key not found. Please set AI71_API_KEY in your .env file.")
        return

    client = AI71(AI71_API_KEY)

    st.markdown('<div class="chatbot-container">', unsafe_allow_html=True)
    st.markdown('<div class="chatbot-header">💬 Ask Medicano</div>', unsafe_allow_html=True)

    user_input = st.text_input("Your question:", key="chat_input", placeholder="Ask about symptoms, health advice...")

    if st.button("Send", key="chat_send"):
        if user_input.strip():
            # Save user message
            st.session_state.chat_history.append({"role": "user", "content": user_input})

            # Send to AI71 Falcon model
            response = client.chat.completions.create(
                model="tiiuae/falcon-180b-chat",
                messages=st.session_state.chat_history
            )

            ai_reply = response.choices[0].message["content"]
            st.session_state.chat_history.append({"role": "assistant", "content": ai_reply})

    # Display conversation
    for msg in st.session_state.chat_history:
        role = "🧑‍⚕️ You" if msg["role"] == "user" else "🤖 Medicano"
        st.markdown(f"**{role}:** {msg['content']}")

    st.markdown('</div>', unsafe_allow_html=True)
