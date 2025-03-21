from fastapi import APIRouter

from schema.codeai import CodeRequest, DocsRequest, StoryRequest
from utils.generate import generate_code_response, generate_document_response, generate_story_response
from utils.prompt import create_code_prompt,create_document_prompt, create_story_prompt


code_router = APIRouter(prefix="/generate", tags=["CodeAI"])

@code_router.post("/generate-code")
def generate_code(request: CodeRequest):
    """
    Generate code based on the given question and programming language.
    """
    prompt = create_code_prompt(request.language, request.question)
    generated_code = generate_code_response(prompt)
    return {"language": request.language, "code": generated_code}

@code_router.post("/generate-document")
def generate_docs(request: DocsRequest):
    """
    Generate Document based on its title.
    """
    prompt = create_document_prompt(request.document_topic,request.word_count)
    generated_docs = generate_document_response(prompt)
    return {"document topic": request.document_topic, "document": generated_docs}
@code_router.post("/generate-story")
def generate_docs(request: StoryRequest):
    """
    Generate Story Based on title and its form.
    """
    prompt = create_story_prompt(request.story_title,request.story_form)
    generated_story = generate_story_response(prompt)
    return {"document topic": request.story_title, "document": generated_story}