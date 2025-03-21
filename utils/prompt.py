def create_code_prompt(language: str, question: str) -> str:
    """
    Generates a strict prompt to ensure AI outputs a properly formatted
    code block in the requested programming language within an HTML structure.
    
    Args:
        language (str): The programming language for the generated code (e.g., "Python", "JavaScript").
        question (str): User's coding request or problem statement.
        
    Returns:
        str: A well-structured prompt enforcing proper language-specific code formatting in HTML.
    """

    # Handle vague inputs
    if len(question.strip()) < 10:
        question = f"Create a practical {language} example"

    prompt = (
        f"You are a highly skilled code assistant. Your task is to generate a code block in {language} "
        f"for the following request: \"{question}\". Your response must follow these strict formatting rules: "
        f"1. The output must be a **fully formatted HTML string** containing the code block. "
        f"2. Use the appropriate HTML syntax highlighting for the specified language, wrapping the code inside: "
        f"   - `<pre><code class='{language.lower()}'>` for the code block. "
        f"   - Ensure the closing `</code></pre>` is properly placed. "
        f"3. **Do not include any newline characters (\\n) or tabs (\\t)** anywhere in your response. "
        f"4. Replace newlines with `<br>` tags to maintain readability when required. "
        f"5. Use `&nbsp;` instead of tabs for indentation. "
        f"6. Provide a **brief explanation** of the code before displaying the formatted code block. "
        f"7. Ensure the output is a **single continuous HTML string** that can be rendered in a browser correctly. "
        f"8. **Do not use Markdown**—only valid HTML with correct syntax highlighting. "
        f"9. **Verify that the generated output is fully complete and contains no syntax errors.** "
        f"10. The response must be fully structured with proper HTML document elements if necessary."
    )

    return prompt

def create_document_prompt(document_topic: str, word_count: int) -> str:
    """
    Creates a prompt that enforces an approximate word count range (±50 words) 
    while generating a complete HTML document.
    
    Args:
        document_topic (str): The subject of the document.
        word_count (int): The target number of words required in the document.
        
    Returns:
        str: A strict prompt enforcing structured HTML output within the word count range.
    """
    # Handle vague topics
    if len(document_topic.strip()) < 5:
        document_topic = "Comprehensive Informational Document"

    word_count = word_count + 200 
    # Ensure a reasonable word count limit
    if word_count < 50:
        word_count = 50  # Set a reasonable lower limit

    min_words = word_count - 50
    max_words = word_count + 50

    prompt = (
        f"You are an expert document generation assistant. Your task is to create a well-structured, high-quality, and formatted HTML document "
        f"on the topic: \"{document_topic}\" with a strict word count between {min_words} and {max_words} words."
        f"\n\nSTRICT REQUIREMENTS FOR YOUR RESPONSE:"
        f"\n1. The document MUST contain between {min_words} and {max_words} words."
        f"\n2. COUNT WORDS CAREFULLY. Ensure that the total word count falls within this range."
        f"\n3. If the word count is too low, expand ideas, add explanations, and provide additional details."
        f"\n4. If the word count is too high, remove redundant sentences and be more concise."
        f"\n5. Structure the document properly to naturally fit the required word count."
        f"\n6. The output must be a fully structured and well-formatted HTML document."
        f"\n7. The document must include:"
        f"\n   - A clear and engaging title inside <h1> tags."
        f"\n   - An introductory paragraph inside <p> tags."
        f"\n   - Well-structured sections with subheadings (<h2>, <h3> as needed)."
        f"\n   - Informative and detailed content ensuring natural flow and readability."
        f"\n   - A conclusion summarizing the key points."
        f"\n8. The word count must be evenly distributed across all sections for readability."
        f"\n9. BEFORE submitting, recount the words and adjust if necessary to ensure compliance with the {min_words}-{max_words} range."
        f"\n10. The response must be a SINGLE CONTINUOUS HTML string with NO newlines (\\n) or tab characters (\\t)."
        f"\n11. Instead of newlines, use <br> for visual separation."
        f"\n12. Instead of tabs, use &nbsp; for indentation."
        f"\n13. DO NOT USE MARKDOWN - ONLY HTML."
        f"\n14. VERIFY AGAIN before finalizing: The final document MUST HAVE between {min_words} and {max_words} words."
    )

    return prompt

def create_story_prompt(title: str, story_type: str) -> str:
    """
    Generates a prompt for AI to create a structured, complete story in strict HTML format
    without newlines, tabs, Markdown elements, or incomplete outputs.

    Args:
        title (str): The title of the story.
        story_type (str): The genre of the story (e.g., "Children's Story", "Horror Story", "Biography", "Sci-Fi").

    Returns:
        str: A structured prompt guiding AI to generate a compelling, full-length story in clean HTML format.
    """

    # Handle vague inputs
    if len(title.strip()) < 3:
        title = "An Untold Tale"
    if len(story_type.strip()) < 3:
        story_type = "General Fiction"

    prompt = (
        f"You are a skilled storyteller. Generate a fully detailed, well-structured, and engaging story titled '{title}' "
        f"in the format of a '{story_type}' story. Follow these strict requirements to ensure a complete and properly formatted response: "
        f"1. The response must be a **fully completed** story with a beginning, middle, and end, ensuring it is never cut off. "
        f"2. The output must be a **single, valid HTML string** without any escape sequences, newlines, tabs, or incomplete sentences. "
        f"3. The title must be enclosed within <h1> tags, and the story content must be wrapped in <p> tags. Use <br> for logical line breaks. "
        f"4. Ensure proper HTML structure that renders perfectly in a web browser. "
        f"6. NO Markdown, unnecessary whitespace, or special characters should be present—only valid HTML. "
        f"7. The story must strictly follow the conventions of the chosen genre: "
        f"   - If 'Children's Story' is selected, make it engaging, imaginative, and suitable for young readers. "
        f"   - If 'Horror Story' is selected, create suspenseful, eerie, and immersive storytelling. "
        f"   - If 'Biography' is selected, provide an accurate, chronological, and inspiring life story with real events. "
        f"   - If 'Historical' is selected, craft a compelling narrative that accurately represents the past. "
        f"   - If 'Sci-Fi' is selected, incorporate futuristic or speculative elements while ensuring a logical storyline. "
        f"8. The AI **must not stop mid-sentence** or generate an incomplete response—ensure the full story is outputted. "
        f"9. Maintain a natural storytelling flow while avoiding repetition or unnecessary filler content. "
    )

    return prompt
