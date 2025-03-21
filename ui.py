import streamlit as st
import requests

# FastAPI base URL
API_BASE_URL = "http://127.0.0.1:8000/v1/generate/generate-code"

# User input for language and question
language = st.selectbox("Select Language", ["Python", "JavaScript", "C++"])
question = st.text_area("Enter your question")

if st.button("Generate Code"):
    # API Request
    response = requests.post(API_BASE_URL, json={"language": language, "question": question})

    if response.status_code == 200:
        result = response.json()
        generated_html = result["code"]  

        # Display HTML output
        st.markdown(generated_html, unsafe_allow_html=True)
    else:
        st.error("Failed to generate code. Please try again.")
