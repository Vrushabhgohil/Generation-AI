import os
from fastapi import FastAPI
import uvicorn
from endpoints.generate.api import code_router
from fastapi.middleware.cors import CORSMiddleware
import openai
app = FastAPI()


app.include_router(code_router,prefix='/v1')

@app.get("/")
def home():
    return {"message": "Welcome to Code AI!"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"], 
)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000, reload=True)
