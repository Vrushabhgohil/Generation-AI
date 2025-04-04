import re
import json
import requests
import streamlit as st
import streamlit.components.v1 as components
from bs4 import BeautifulSoup
from streamlit_option_menu import option_menu

# Configuration
st.set_page_config(page_title="AI Code Assistant", layout="wide")

# Constants
API_CONFIG = {
    "BASE_URL": "https://generation-ai.onrender.com/v1/generate",
    "ENDPOINTS": {
        "code": "/generate-code",
        "document": "/generate-document",
        "story": "/generate-story",
        "chat": "/chat",
    },
}

LANGUAGE_OPTIONS = ["Python", "JavaScript", "Java","Laravel","Typescript","Nextjs", "C++", "PHP", "HTML", "CSS", "Ruby", "Kotlin"]
STORY_FORMS = ["Short Story", "Poem", "Novel Chapter"]

# Chat avatars
USER_AVATAR_URL = "https://cdn-icons-png.flaticon.com/512/3135/3135715.png"
BOT_AVATAR_URL = "https://cdn-icons-png.flaticon.com/512/4712/4712109.png"


class APIClient:
    @staticmethod
    def send_request(endpoint, payload):
        url = f"{API_CONFIG['BASE_URL']}{API_CONFIG['ENDPOINTS'][endpoint]}"
        try:
            response = requests.post(url, json=payload, headers={"Content-Type": "application/json"})
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            st.error(f"API Request failed: {str(e)}")
            return None

    @staticmethod
    def generate_curl_command(endpoint, payload):
        url = f"{API_CONFIG['BASE_URL']}{API_CONFIG['ENDPOINTS'][endpoint]}"
        return (
            f'curl -X POST "{url}" \\\n'
            '  -H "Content-Type: application/json" \\\n'
            f"  -d '{json.dumps(payload)}'"
        )


class ResponseParser:
    @staticmethod
    def format_document(text):
        if not text:
            return ""
        if "<" in text and ">" in text:
            text = BeautifulSoup(text, "html.parser").get_text()
        return "".join(
            f"<p>{p.strip()}</p>" for p in re.split(r"\n\s*\n", text) if p.strip()
        )

    @staticmethod
    def extract_code_from_markdown(content):
        matches = re.findall(r"```(?:\w+)?\n([\s\S]*?)\n```", content)
        return "\n\n".join(matches) if matches else None

    @staticmethod
    def clean_html_response(html_content):
        try:
            code = ResponseParser.extract_code_from_markdown(html_content)
            if code:
                soup = BeautifulSoup(code, "html.parser")
                if not any(soup.find(tag) for tag in ["h1", "h2", "p", "pre"]):
                    return {
                        "description": "Generated code:",
                        "code": code,
                        "conclusion": "Code generation complete.",
                    }

            soup = BeautifulSoup(html_content, "html.parser")
            description = soup.find("p").text.strip() if soup.find("p") else ""

            code_element = soup.find("pre")
            if code_element and code_element.find("code"):
                code = code_element.find("code").text.strip()
            elif code_element:
                code = code_element.text.strip()
            else:
                code = code or html_content

            conclusion = ""
            if len(soup.find_all("p")) > 1:
                conclusion = soup.find_all("p")[-1].text.strip()

            return {"description": description, "code": code, "conclusion": conclusion}
        except Exception as e:
            return {
                "description": "Error parsing response.",
                "code": html_content,
                "conclusion": f"Error: {str(e)}",
            }


class UI:
    @staticmethod
    def show_code_generator():
        st.header("Code Generator")
        language = st.selectbox("Select Programming Language", LANGUAGE_OPTIONS)
        question = st.text_area("Enter your coding question")

        if st.button("Generate Code", type="primary"):
            if not all([language, question]):
                st.error("Please provide both language and question.")
                return

            with st.spinner("Generating code..."):
                payload = {"language": language, "question": question}
                result = APIClient.send_request("code", payload)
                if result:
                    UI.display_code_results(result, language)

    @staticmethod
    def show_document_generator():
        st.header("Document Generator")
        topic = st.text_input("Enter document topic")
        word_count = st.number_input("Word Count", min_value=100, max_value=5000, value=500)

        if st.button("Generate Document", type="primary"):
            if not topic:
                st.error("Please provide a document topic.")
                return

            with st.spinner("Generating document..."):
                payload = {"document_topic": topic, "word_count": word_count}
                result = APIClient.send_request("document", payload)
                if result:
                    st.markdown(
                        ResponseParser.format_document(result.get("document", "")),
                        unsafe_allow_html=True,
                    )

    @staticmethod
    def show_story_generator():
        st.header("Story Generator")
        title = st.text_input("Enter story title")
        story_form = st.selectbox("Select Story Form", STORY_FORMS)

        if st.button("Generate Story", type="primary"):
            if not title:
                st.error("Please provide a story title.")
                return

            with st.spinner("Generating story..."):
                payload = {"story_title": title, "story_form": story_form}
                result = APIClient.send_request("story", payload)
                if result:
                    st.markdown(
                        ResponseParser.format_document(result.get("document", "")),
                        unsafe_allow_html=True,
                    )

    @staticmethod
    def show_chat():
        st.header("Chat")

        # Reset chat instantly on clear button
        clear = st.button("Clear Chat")
        if clear:
            st.session_state.chat_history = []
            st.experimental_user()

        # Initialize history
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []

        user_input = st.text_input("Enter your message")

        if st.button("Send") and user_input.strip():
            st.session_state.chat_history.append({"sender": "user", "message": user_input})

            with st.spinner("Processing..."):
                payload = {"prompt": user_input}
                result = APIClient.send_request("chat", payload)

                if result and "response" in result:
                    st.session_state.chat_history.append({"sender": "bot", "message": result["response"]})
                else:
                    st.session_state.chat_history.append({"sender": "bot", "message": "❌ Failed to get a response."})

        # Show chat history
        for chat in st.session_state.chat_history:
            avatar = USER_AVATAR_URL if chat["sender"] == "user" else BOT_AVATAR_URL
            align = "flex-start" if chat["sender"] == "user" else "flex-end"
            bg_color = "#f0f0f0" if chat["sender"] == "user" else "#dceeff"
            text_color = "#000000" if chat["sender"] == "user" else "#1a1a1a"

            st.markdown(f"""
                <div style='display: flex; justify-content: {align}; margin-bottom: 1rem;'>
                    <img src='{avatar}' style='width: 40px; height: 40px; border-radius: 50%; margin-right: 10px;' />
                    <div style='background-color: {bg_color}; color: {text_color}; padding: 10px 15px; border-radius: 10px; max-width: 75%; word-wrap: break-word;'>
                        {chat["message"]}
                    </div>
                </div>
            """, unsafe_allow_html=True)


    @staticmethod
    def display_code_results(result, language):
        cleaned_data = ResponseParser.clean_html_response(result.get("code", ""))

        st.subheader("Generated Code Results")

        for section, expanded in [
            ("Description", True),
            ("Code", True),
            ("Conclusion", True),
            ("Curl Command", False),
        ]:
            with st.expander(section, expanded=expanded):
                if section == "Code":
                    st.code(cleaned_data["code"], language=language.lower())
                elif section == "Curl Command":
                    st.code(
                        APIClient.generate_curl_command("code", result), language="bash"
                    )
                else:
                    st.write(cleaned_data.get(section.lower(), ""))


def main():
    selected = option_menu(
        menu_title=None,
        options=["Code Generator", "Document Generator", "Story Generator", "Chat"],
        icons=["code-slash", "file-text", "book", "chat-dots"],
        orientation="horizontal",
    )

    if selected == "Code Generator":
        UI.show_code_generator()
    elif selected == "Document Generator":
        UI.show_document_generator()
    elif selected == "Story Generator":
        UI.show_story_generator()
    elif selected == "Chat":
        UI.show_chat()


if __name__ == "__main__":
    main()
