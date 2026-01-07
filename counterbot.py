import streamlit as st
from google import genai
from google.genai import types
from dotenv import load_dotenv
import random
import os
import time

st.set_page_config(page_title="CounterBot", layout="centered")
load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
MODEL_NAME = "gemini-2.5-flash-lite"

def safe_generate(prompt):
    for _ in range(3):  # retry 3 times
        try:
            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=[types.Content(role="user", parts=[types.Part(text=prompt)])]
            )
            return response.text
        except Exception:
            time.sleep(2)
    return "The AI service is currently overloaded. Please try again in a moment."

if "chat" not in st.session_state:
    st.session_state.chat = []

if "counter" not in st.session_state:
    st.session_state.counter = 0

if "last_five" not in st.session_state:
    st.session_state.last_five = []

if "quiz_question" not in st.session_state:
    st.session_state.quiz_question = None

# ---------------- UI ----------------
st.title("The CounterBot")

for msg in st.session_state.chat:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("kuch toh kaho7...")

# ---------------- MAIN LOGIC ----------------
if user_input:
    st.session_state.chat.append({"role": "user", "content": user_input})

    st.session_state.counter += 1
    st.session_state.last_five.append(user_input)

    if len(st.session_state.last_five) > 5:
        st.session_state.last_five.pop(0)

    reply = safe_generate(user_input)

    st.session_state.chat.append({"role": "assistant", "content": reply})

    with st.chat_message("user"):
        st.markdown(user_input)
    with st.chat_message("assistant"):
        st.markdown(reply)

    # ---------------- QUIZ TRIGGER ----------------
    if st.session_state.counter == 5:
        chosen_topic = random.choice(st.session_state.last_five)

        quiz_prompt = (
            "Create a short conceptual quiz question from this topic. "
            "Do NOT include the answer.\n\n"
            f"Topic: {chosen_topic}"
        )

        st.session_state.quiz_question = safe_generate(quiz_prompt)

        st.session_state.counter = 0
        st.session_state.last_five = []

# ---------------- SHOW QUIZ ----------------
if st.session_state.quiz_question:
    st.divider()
    st.subheader("Quiz Time!")
    st.markdown(st.session_state.quiz_question)

    user_answer = st.text_input("Your answer:")

    if st.button("Submit Answer"):
        eval_prompt = (
            f"Question: {st.session_state.quiz_question}\n"
            f"Student Answer: {user_answer}\n\n"
            "Reply with 'Correct' or 'Incorrect' and a short explanation."
        )

        evaluation = safe_generate(eval_prompt)

        st.markdown("### Evaluation")
        st.markdown(evaluation)

        st.session_state.quiz_question = None
