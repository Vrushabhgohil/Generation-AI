import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/chat/"

st.title("💬 AI Chatbot")
st.write("Powered by GPT-4o and FastAPI")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# User input
user_input = st.chat_input("Ask something...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    # Send request to FastAPI (Fix: Send JSON correctly)
    try:
        response = requests.post(API_URL, json={"prompt": user_input})
        bot_response = response.json().get("response", "Sorry, something went wrong.")
    except Exception as e:
        bot_response = "Error connecting to the server."

    # Display bot response
    st.session_state.messages.append({"role": "assistant", "content": bot_response})
    with st.chat_message("assistant"):
        st.write(bot_response)
