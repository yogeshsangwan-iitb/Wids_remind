import streamlit as st
from google import genai
from google.genai import types
from dotenv import load_dotenv
import time
import os

# ---------------- CONFIG ----------------
st.set_page_config(page_title="TimeBot", layout="centered")
load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
MODEL_NAME = "gemini-2.5-flash-lite"

# ---------------- SAFE AI CALL ----------------
def safe_generate(prompt):
    for _ in range(3):
        try:
            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=[types.Content(role="user", parts=[types.Part(text=prompt)])]
            )
            return response.text
        except:
            time.sleep(2)
    return "⚠️ AI service is busy. Try again shortly."

# ---------------- SESSION STATE ----------------
if "chat" not in st.session_state:
    st.session_state.chat = []

if "pending_queries" not in st.session_state:
    st.session_state.pending_queries = []

if "quiz_question" not in st.session_state:
    st.session_state.quiz_question = None

# ---------------- UI ----------------
st.title("⏱️ TimeBot")

for msg in st.session_state.chat:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Ask something...")

# ---------------- HANDLE USER INPUT ----------------
if user_input:
    current_time = time.time()

    st.session_state.chat.append({"role": "user", "content": user_input})

    st.session_state.pending_queries.append({
        "text": user_input,
        "time": current_time
    })

    reply = safe_generate(user_input)

    st.session_state.chat.append({"role": "assistant", "content": reply})

    with st.chat_message("user"):
        st.markdown(user_input)
    with st.chat_message("assistant"):
        st.markdown(reply)

# ---------------- TIME CHECK ----------------
current_time = time.time()

for item in st.session_state.pending_queries:
    if current_time - item["time"] >= 10 and st.session_state.quiz_question is None:
        quiz_prompt = (
            "Create a short conceptual quiz question from this topic. "
            "Do NOT include the answer.\n\n"
            f"Topic: {item['text']}"
        )

        st.session_state.quiz_question = safe_generate(quiz_prompt)

        st.session_state.pending_queries.remove(item)
        break

# ---------------- SHOW QUIZ ----------------
if st.session_state.quiz_question:
    st.divider()
    st.subheader("🧪 Quiz Time!")
    st.markdown(st.session_state.quiz_question)

    user_answer = st.text_input("Your answer:")

    if st.button("Submit Answer"):
        eval_prompt = (
            f"Question: {st.session_state.quiz_question}\n"
            f"Student Answer: {user_answer}\n\n"
            "Reply with 'Correct' or 'Incorrect' and a short explanation."
        )

        evaluation = safe_generate(eval_prompt)

        st.markdown("### 🧠 Evaluation")
        st.markdown(evaluation)

        st.session_state.quiz_question = None
