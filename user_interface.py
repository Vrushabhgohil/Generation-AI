import streamlit as st
import requests
import json
from bs4 import BeautifulSoup
import re
from difflib import get_close_matches

st.set_page_config(page_title="Content Generator", page_icon="✨", layout="wide")

st.title("Multi-Content Generator")
st.markdown("Generate code, documents, or stories with AI assistance.")

# Programming languages list for suggestions and spell correction
COMMON_LANGUAGES = [
    "Python", "JavaScript", "Java", "C++", "C#", "PHP", "Ruby", "Go", "Swift", "Kotlin", 
    "TypeScript", "Rust", "Scala", "Perl", "R", "Dart", "Bash", "PowerShell", "SQL", 
    "HTML", "CSS", "SCSS", "Shell", "Objective-C", "Lua", "Matlab", "Assembly"
]

# Common story forms
STORY_FORMS = [
    "Short Story", "Novel", "Poem", "Fairy Tale", "Fable", "Science Fiction", 
    "Fantasy", "Horror", "Mystery", "Romance", "Historical Fiction", "Flash Fiction"
]

# API endpoints
API_BASE_URL = "http://localhost:8000/v1/generate"  # Update with your actual API base URL
API_ENDPOINTS = {
    "code": f"{API_BASE_URL}/generate-code",
    "document": f"{API_BASE_URL}/generate-document",
    "story": f"{API_BASE_URL}/generate-story"
}

def suggest_language(input_lang):
    """Suggest a correct language name if misspelled"""
    if not input_lang:
        return None
    
    # Convert both input and options to lowercase for matching
    input_lang_lower = input_lang.lower()
    options_lower = [lang.lower() for lang in COMMON_LANGUAGES]
    
    # Check if input is already a valid language
    if input_lang_lower in options_lower:
        return COMMON_LANGUAGES[options_lower.index(input_lang_lower)]
    
    # Find close matches
    matches = get_close_matches(input_lang_lower, options_lower, n=1, cutoff=0.6)
    if matches:
        return COMMON_LANGUAGES[options_lower.index(matches[0])]
    
    return input_lang  # Return original if no suggestions

def extract_code_from_markdown(content):
    """Extract code blocks from markdown content"""
    # Find code blocks in markdown format
    pattern = r'```(?:\w+)?\n([\s\S]*?)\n```'
    matches = re.findall(pattern, content)
    
    if matches:
        return '\n\n'.join(matches)
    return None

def clean_html_response(html_content):
    """Extract the description, code block, and conclusion from HTML content."""
    try:
        # First, check if response is a markdown code block and handle it
        markdown_code = extract_code_from_markdown(html_content)
        if markdown_code:
            # Try to find HTML structure inside markdown
            soup = BeautifulSoup(markdown_code, 'html.parser')
            if soup.find('h1') or soup.find('h2') or soup.find('p') or soup.find('pre'):
                # Process as HTML
                html_content = markdown_code
            else:
                # Just a code block, create structure
                return {
                    "description": "Generated code:",
                    "code": markdown_code,
                    "conclusion": "Code generation complete."
                }
                
        # Use BeautifulSoup to parse the HTML
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Find the sections
        description = ""
        code = ""
        conclusion = ""
        
        # Extract description - multiple patterns
        description_patterns = [
            # Look for h1/h2/h3 with "description" and get next paragraph
            lambda s: s.find(['h1', 'h2', 'h3'], string=re.compile('description', re.I)),
            # Look for p after "description" text
            lambda s: s.find(string=re.compile('description:', re.I)),
            # First paragraph as fallback
            lambda s: s.find('p')
        ]
        
        for pattern in description_patterns:
            element = pattern(soup)
            if element:
                if element.name == 'p':
                    description = element.text.strip()
                    break
                elif element.name in ['h1', 'h2', 'h3']:
                    next_p = element.find_next('p')
                    if next_p:
                        description = next_p.text.strip()
                        break
                else:  # String match
                    parent = element.parent
                    if parent.name == 'p':
                        description = parent.text.strip()
                    else:
                        next_p = element.find_next('p')
                        if next_p:
                            description = next_p.text.strip()
                    break
        
        # Extract code - multiple patterns
        code_patterns = [
            # Standard pre>code tag
            lambda s: s.find('pre', recursive=True).find('code') if s.find('pre') else None,
            # Just pre tag
            lambda s: s.find('pre'),
            # Just code tag
            lambda s: s.find('code'),
            # After "code block" heading
            lambda s: s.find(['h1', 'h2', 'h3'], string=re.compile('code', re.I))
        ]
        
        for pattern in code_patterns:
            element = pattern(soup)
            if element:
                if element.name == 'code':
                    code = element.text.strip()
                    break
                elif element.name == 'pre':
                    if element.find('code'):
                        code = element.find('code').text.strip()
                    else:
                        code = element.text.strip()
                    break
                elif element.name in ['h1', 'h2', 'h3']:
                    next_pre = element.find_next('pre')
                    if next_pre:
                        if next_pre.find('code'):
                            code = next_pre.find('code').text.strip()
                        else:
                            code = next_pre.text.strip()
                    break
        
        # If still no code found, try regex for code blocks
        if not code:
            code = extract_code_from_markdown(html_content)
            
        # Handle code with HTML entities
        if code and '&lt;' in code:
            code = code.replace('&lt;', '<').replace('&gt;', '>')
                        
        # Extract conclusion - multiple patterns
        conclusion_patterns = [
            # Look for h1/h2/h3 with "conclusion" and get next paragraph
            lambda s: s.find(['h1', 'h2', 'h3'], string=re.compile('conclusion', re.I)),
            # Look for p after "conclusion" text
            lambda s: s.find(string=re.compile('conclusion:', re.I)),
            # Last paragraph as fallback
            lambda s: s.find_all('p')[-1] if len(s.find_all('p')) > 1 else None
        ]
        
        for pattern in conclusion_patterns:
            element = pattern(soup)
            if element:
                if element.name == 'p':
                    # Make sure it's not the same as description
                    if element.text.strip() != description:
                        conclusion = element.text.strip()
                    break
                elif element.name in ['h1', 'h2', 'h3']:
                    next_p = element.find_next('p')
                    if next_p and next_p.text.strip() != description:
                        conclusion = next_p.text.strip()
                        break
                else:  # String match
                    parent = element.parent
                    if parent.name == 'p':
                        conclusion = parent.text.strip()
                    else:
                        next_p = element.find_next('p')
                        if next_p and next_p.text.strip() != description:
                            conclusion = next_p.text.strip()
                    break
                    
        # Fallbacks for complex structures
        if not description and soup.find_all(['p', 'div']):
            # Find first substantial text block
            for el in soup.find_all(['p', 'div']):
                if len(el.text.strip()) > 30:  # Reasonable description length
                    description = el.text.strip()
                    break
        
        if not conclusion and soup.find_all(['p', 'div']):
            # Find last substantial text block
            elements = soup.find_all(['p', 'div'])
            elements.reverse()
            for el in elements:
                if len(el.text.strip()) > 30 and el.text.strip() != description:
                    conclusion = el.text.strip()
                    break
                    
        # If no structured content found, handle raw text
        if not (description or code or conclusion) and html_content.strip():
            parts = html_content.strip().split("\n\n")
            if len(parts) >= 3:
                description = parts[0]
                conclusion = parts[-1]
                code = "\n\n".join(parts[1:-1])
            elif len(parts) == 2:
                description = parts[0]
                code = parts[1]
            else:
                code = parts[0]
                
        return {
            "description": description,
            "code": code,
            "conclusion": conclusion
        }
    except Exception as e:
        return {
            "description": "Error parsing the response.",
            "code": html_content,  # Return the original content as code
            "conclusion": f"Error: {str(e)}"
        }

def generate_curl_command(url, payload):
    """Generate a curl command for the API request"""
    curl_cmd = f'curl -X POST "{url}" \\\n'
    curl_cmd += '  -H "Content-Type: application/json" \\\n'
    curl_cmd += f'  -d \'{json.dumps(payload)}\''
    
    return curl_cmd

def format_document(document_text):
    """Format document text with proper paragraphs and styling"""
    if not document_text:
        return ""
    
    # Clean up any HTML tags if present
    if "<" in document_text and ">" in document_text:
        soup = BeautifulSoup(document_text, 'html.parser')
        document_text = soup.get_text()
    
    # Split into paragraphs
    paragraphs = re.split(r'\n\s*\n', document_text)
    
    # Format with proper paragraph tags
    formatted_text = ""
    for p in paragraphs:
        if p.strip():
            formatted_text += f"<p>{p.strip()}</p>"
    
    return formatted_text

# Tabs for different generation types
tab1, tab2, tab3 = st.tabs(["Code Generator", "Document Generator", "Story Generator"])

# Tab 1: Code Generator
with tab1:
    st.header("Code Generator")
    
    col1, col2 = st.columns(2)
    with col1:
        language_input = st.text_input("Programming Language", placeholder="e.g., Python, JavaScript", key="code_lang")
        
        # Show language suggestion if possible
        language_suggestion = suggest_language(language_input)
        if language_suggestion and language_suggestion.lower() != language_input.lower():
            st.info(f"Did you mean: {language_suggestion}? Using this suggestion.")
            language = language_suggestion
        else:
            language = language_input

    with col2:
        question = st.text_area("Question", placeholder="What code would you like to generate?", height=100, key="code_question")

    if st.button("Generate Code", type="primary", key="generate_code_btn"):
        if not language or not question:
            st.error("Please provide both a programming language and a question.")
        else:
            with st.spinner("Generating code..."):
                payload = {"language": language, "question": question}
                try:
                    response = requests.post(
                        API_ENDPOINTS["code"],
                        json=payload,
                        headers={"Content-Type": "application/json"}
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        # Add curl command to the result
                        result["curl_command"] = generate_curl_command(API_ENDPOINTS["code"], payload)
                        
                        # Clean the HTML response
                        cleaned_data = clean_html_response(result.get("code", ""))
                        
                        # Display results in expandable sections
                        st.subheader("Generated Code Results")
                        
                        # Description
                        if cleaned_data["description"]:
                            with st.expander("Description", expanded=True):
                                st.write(cleaned_data["description"])
                        
                        # Code Block
                        if cleaned_data["code"]:
                            with st.expander("Code", expanded=True):
                                st.code(cleaned_data["code"], language=language.lower())
                        
                        # Conclusion
                        if cleaned_data["conclusion"]:
                            with st.expander("Conclusion", expanded=True):
                                st.write(cleaned_data["conclusion"])
                        
                        # Curl Command
                        with st.expander("Curl Command", expanded=False):
                            st.code(result["curl_command"], language="bash")
                    else:
                        st.error(f"Error: {response.status_code} - {response.text}")
                except Exception as e:
                    st.error(f"Error: {str(e)}")

# Tab 2: Document Generator
with tab2:
    st.header("Document Generator")
    
    col1, col2 = st.columns(2)
    with col1:
        document_topic = st.text_input("Document Topic", placeholder="e.g., Climate Change, Space Exploration", key="doc_topic")
    with col2:
        word_count = st.number_input("Approximate Word Count", min_value=100, max_value=2000, value=500, step=100, key="doc_words")
    
    if st.button("Generate Document", type="primary", key="generate_doc_btn"):
        if not document_topic:
            st.error("Please provide a document topic.")
        else:
            with st.spinner("Generating document..."):
                payload = {"document_topic": document_topic, "word_count": int(word_count)}
                try:
                    response = requests.post(
                        API_ENDPOINTS["document"],
                        json=payload,
                        headers={"Content-Type": "application/json"}
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        # Add curl command to the result
                        result["curl_command"] = generate_curl_command(API_ENDPOINTS["document"], payload)
                        
                        # Display results
                        st.subheader(f"Document: {document_topic}")
                        
                        # Document content
                        st.markdown(format_document(result.get("document", "")), unsafe_allow_html=True)
                        
                        # Curl Command
                        with st.expander("Curl Command", expanded=False):
                            st.code(result["curl_command"], language="bash")
                    else:
                        st.error(f"Error: {response.status_code} - {response.text}")
                except Exception as e:
                    st.error(f"Error: {str(e)}")

# Tab 3: Story Generator
with tab3:
    st.header("Story Generator")
    
    col1, col2 = st.columns(2)
    with col1:
        story_title = st.text_input("Story Title", placeholder="e.g., The Last Starship, Journey to the Unknown", key="story_title")
    with col2:
        story_form = st.selectbox("Story Form", options=STORY_FORMS, index=0, key="story_form")
    
    if st.button("Generate Story", type="primary", key="generate_story_btn"):
        if not story_title:
            st.error("Please provide a story title.")
        else:
            with st.spinner("Generating story..."):
                payload = {"story_title": story_title, "story_form": story_form}
                try:
                    response = requests.post(
                        API_ENDPOINTS["story"],
                        json=payload,
                        headers={"Content-Type": "application/json"}
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        # Add curl command to the result
                        result["curl_command"] = generate_curl_command(API_ENDPOINTS["story"], payload)
                        
                        # Display results
                        st.subheader(f"{story_form}: {story_title}")
                        
                        # Story content
                        st.markdown(format_document(result.get("document", "")), unsafe_allow_html=True)
                        
                        # Curl Command
                        with st.expander("Curl Command", expanded=False):
                            st.code(result["curl_command"], language="bash")
                    else:
                        st.error(f"Error: {response.status_code} - {response.text}")
                except Exception as e:
                    st.error(f"Error: {str(e)}")

# Add footer
st.markdown("---")
st.markdown("Multi-Content Generator - Generate code, documents, and stories with AI assistance.")