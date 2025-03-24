from docx import Document
from dotenv import load_dotenv
import openai
from fastapi import HTTPException
import os
from reportlab.pdfgen import canvas
load_dotenv()
# Ensure API key is properly loaded
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("OPENAI_API_KEY environment variable is not set!")




def generate_code_response(prompt: str) -> str:
    """
    Handles the response from OpenAI API for code generation (Compatible with OpenAI v1.0.0+).
    """
    try:
        # Pass the API key explicitly when creating the client
        client = openai.OpenAI(api_key=api_key)  

        response = client.chat.completions.create(
            model="gpt-4",  
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        return response.choices[0].message.content.strip()
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# def generate_document_response(prompt: str) -> str:
#     """
#     Handles the response from OpenAI API for document generation (Compatible with OpenAI v1.0.0+).
#     """
#     try:
#         client = openai.OpenAI()  

#         response = client.chat.completions.create(
#             model="gpt-4",  
#             messages=[
#                 {"role": "system", "content": "You are a helpful document creator."},
#                 {"role": "user", "content": prompt}
#             ],
#             max_tokens=700
#         )

#         return response.choices[0].message.content.strip()
    
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


def generate_document_response(prompt: str) -> str:
    """
    Handles the response from OpenAI API for document generation.
    """
    try:
        client = openai.OpenAI()

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "system", "content": "You are a helpful document creator."},
                      {"role": "user", "content": prompt}],
            max_tokens=1500
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def save_text_to_pdf(text: str, filename: str) -> str:
    pdf_path = f"static/{filename}"
    c = canvas.Canvas(pdf_path)
    c.drawString(100, 750, "Generated Document")

    y_position = 730
    for line in text.split("\n"):
        c.drawString(100, y_position, line)
        y_position -= 20

    c.save()
    return pdf_path

def save_text_to_docx(text: str, filename: str) -> str:
    doc_path = f"static/{filename}"
    doc = Document()
    doc.add_paragraph(text)
    doc.save(doc_path)
    return doc_path

def generate_story_response(prompt: str) -> str:
    """
    Handles the response from OpenAI API for document generation (Compatible with OpenAI v1.0.0+).
    """
    try:
        client = openai.OpenAI()  

        response = client.chat.completions.create(
            model="gpt-4",  
            messages=[
                {"role": "system", "content": "You are a helpful Story creator."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=700
        )

        return response.choices[0].message.content.strip()
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
