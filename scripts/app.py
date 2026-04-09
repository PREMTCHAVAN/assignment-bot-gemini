import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# ------------------ CONFIG ------------------
st.set_page_config(
    page_title="Assignment Assistant",
    page_icon="📚",
    layout="wide"
)

# ------------------ LOAD ENV ------------------
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("❌ API key not found. Check your .env file.")
    st.stop()

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-flash-lite-latest")

# ------------------ SIDEBAR ------------------
with st.sidebar:
    st.title("⚙️ Settings")

    mode = st.selectbox(
        "Select Mode",
        ["Assignment", "Simple", "Detailed"]
    )

    st.markdown("---")

    st.markdown("### 📘 About")
    st.write("AI-powered Assignment Assistant")
    st.write("Built with Gemini API")

# ------------------ AGENT ------------------
def agent(user_input, mode):
    if mode == "Simple":
        style = "Explain in a very simple and short way."
    elif mode == "Detailed":
        style = "Explain in detail with depth and clarity."
    else:
        style = """
Answer in this format:
1. Definition
2. Explanation
3. Example
4. Conclusion
"""

    prompt = f"""
You are a Computer Engineering assignment assistant.

{style}

Keep answers clean, structured, and easy to understand.

Question: {user_input}
"""
    return prompt

# ------------------ HEADER ------------------
st.markdown("# 📚 Assignment Assistant Bot")
st.caption("🚀 Your AI-powered study companion")

# ------------------ SESSION ------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ------------------ WELCOME ------------------
if not st.session_state.messages:
    st.info("👋 Ask me anything related to your assignments ")

# ------------------ CHAT HISTORY ------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ------------------ INPUT ------------------
user_input = st.chat_input("Type your assignment question here...")

# ------------------ RESPONSE ------------------
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Thinking... 🤖"):
            try:
                prompt = agent(user_input, mode)
                response = model.generate_content(prompt)
                answer = response.text

            except Exception:
                answer = "⚠️ Rate limit reached. Please wait a few seconds and try again."

            st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})