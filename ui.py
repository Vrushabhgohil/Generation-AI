import streamlit as st
import requests
import re
import time

# FastAPI base URL
API_BASE_URL = "https://generationai.streamlit.app/v1/generate"

# Function to extract description and code without BeautifulSoup
def extract_details(html_response: str) -> tuple:
    # Extract code using regex
    code_match = re.search(r'<code>(.*?)</code>', html_response, re.DOTALL)
    code_text = code_match.group(1).strip() if code_match else "No executable code found."
    
    # Get description by removing code section and HTML tags
    description = html_response
    description = re.sub(r'<code>.*?</code>', '', description, flags=re.DOTALL)
    description = re.sub(r'<[^>]+>', ' ', description)
    description = re.sub(r'\s+', ' ', description).strip()
    
    return description, code_text

# Function to show loading spinner
def show_loading():
    with st.spinner("Generating, please wait..."):
        time.sleep(1)  # Simulating a small delay

# Streamlit UI
st.title("Code Generator AI")

# Sidebar options
generation_type = st.sidebar.radio("Select what you want to generate", ["Code", "Document", "Story"])

if generation_type == "Code":
    language = st.selectbox("Select Language", ["Python", "JavaScript", "C++"])
    question = st.text_area("Enter your question")
    
    if st.button("Generate Code"):
        show_loading()
        try:
            response = requests.post(
                f"{API_BASE_URL}/generate-code", 
                json={"language": language, "question": question},
                timeout=15
            )
            if response.status_code == 200:
                result = response.json()
                generated_html = result["code"]  
                description, extracted_code = extract_details(generated_html)
                st.markdown(f"**Description:**\n\n{description}")
                st.code(extracted_code, language.lower())  
            else:
                st.error(f"Failed to generate code. Status code: {response.status_code}")
        except Exception as e:
            st.error(f"Error connecting to API: {str(e)}")

elif generation_type == "Document":
    document_topic = st.text_input("Enter Document Topic")
    word_count = st.number_input("Enter Word Count", min_value=50, max_value=5000, step=50)
    
    if st.button("Generate Document"):
        show_loading()
        try:
            response = requests.post(
                f"{API_BASE_URL}/generate-document", 
                json={"document_topic": document_topic, "word_count": word_count},
                timeout=15
            )
            if response.status_code == 200:
                result = response.json()
                st.text_area("Generated Document", result["document"], height=300)
            else:
                st.error(f"Failed to generate document. Status code: {response.status_code}")
        except Exception as e:
            st.error(f"Error connecting to API: {str(e)}")

elif generation_type == "Story":
    story_title = st.text_input("Enter Story Title")
    story_form = st.selectbox("Select Story Form", ["Short Story", "Poem", "Narrative"])
    
    if st.button("Generate Story"):
        show_loading()
        try:
            response = requests.post(
                f"{API_BASE_URL}/generate-story", 
                json={"story_title": story_title, "story_form": story_form},
                timeout=15
            )
            if response.status_code == 200:
                result = response.json()
                st.text_area("Generated Story", result["document"], height=300)
            else:
                st.error(f"Failed to generate story. Status code: {response.status_code}")
        except Exception as e:
            st.error(f"Error connecting to API: {str(e)}")