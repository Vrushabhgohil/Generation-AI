import openai
from fastapi import HTTPException
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_code_response(prompt: str) -> str:
    """
    Handles the response from OpenAI API for code generation (Compatible with OpenAI v1.0.0+).
    """
    try:
        client = openai.OpenAI()  

        response = client.chat.completions.create(
            model="gpt-4",  
            messages=[
                {"role": "system", "content": "You are a helpful coding assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=700
        )

        return response.choices[0].message.content.strip()
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def generate_document_response(prompt: str) -> str:
    """
    Handles the response from OpenAI API for document generation (Compatible with OpenAI v1.0.0+).
    """
    try:
        client = openai.OpenAI()  

        response = client.chat.completions.create(
            model="gpt-4",  
            messages=[
                {"role": "system", "content": "You are a helpful document creator."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=700
        )

        return response.choices[0].message.content.strip()
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

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
