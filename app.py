import streamlit as st
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load API key
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-2.0-flash")

st.title("My Chatbot 🤖")

# Initialize memory
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Display previous messages
for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["text"])

# Input box
user_input = st.chat_input("Bol na bhai...")

if user_input:
    # Store user message
    st.session_state["messages"].append(
        {"role": "user", "text": user_input}
    )

    try:
        # Send only the latest message to Gemini
        response = model.generate_content(user_input)
        reply = response.text

        # Store assistant reply
        st.session_state["messages"].append(
            {"role": "assistant", "text": reply}
        )

        # Display reply
        with st.chat_message("assistant"):
            st.markdown(reply)

    except Exception as e:
        st.error(f"Error: {e}")
