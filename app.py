import os
from fastapi import FastAPI
import uvicorn
from endpoints.generate.api import code_router

import openai
app = FastAPI()
openapi_key = os.getenv("OPENAI_API_KEY")


app.include_router(code_router,prefix='/v1')
@app.get("/")
def home():
    return {"message": "Welcome to Code AI!"}

class ChatRequest(openai.BaseModel):
    prompt: str

@app.post("/chat/")
async def chat(request: ChatRequest):
    client = openai.OpenAI(api_key=openapi_key)
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": request.prompt}]
    )
    return {"response": response.choices[0].message.content}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000, reload=True)
