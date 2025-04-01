import openai
from pydantic import BaseModel

class CodeRequest(BaseModel):
    language: str
    question: str

class DocsRequest(BaseModel):
    document_topic: str
    word_count: int

class StoryRequest(BaseModel):
    story_title: str
    story_form: str

class ChatRequest(BaseModel): 
    prompt: str 

class CodeCompilerRequest(BaseModel):  
    language: str
    code: str