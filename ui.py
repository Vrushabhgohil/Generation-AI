import streamlit as st
import requests
from bs4 import BeautifulSoup

# FastAPI base URL
API_BASE_URL = "http://127.0.0.1:8000/v1/generate/generate-code"

# Function to extract description and code from the HTML response
def extract_details(html_response: str) -> tuple:
    soup = BeautifulSoup(html_response, "html.parser")

    # Extract all text except the <code> block as the description
    description_parts = []
    for element in soup.find_all(["p", "div"]):  # Get text from paragraphs and divs
        description_parts.append(element.get_text())

    description = "\n".join(description_parts).strip()

    # Extract only the code
    code_block = soup.find("code")
    code_text = code_block.text.strip() if code_block else "No executable code found."

    return description, code_text

# User input for language and question
language = st.selectbox("Select Language", ["Python", "JavaScript", "C++"])
question = st.text_area("Enter your question")

if st.button("Generate Code"):
    # API Request
    response = requests.post(API_BASE_URL, json={"language": language, "question": question})

    if response.status_code == 200:
        result = response.json()
        generated_html = result["code"]  

        # Extract description and code
        description, extracted_code = extract_details(generated_html)

        # Display description properly
        st.markdown(f"**Description:**\n\n{description}")

        # Display extracted code in a proper code block
        st.code(extracted_code, language.lower())  
    else:
        st.error("Failed to generate code. Please try again.")
