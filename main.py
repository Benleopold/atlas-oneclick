from fastapi import FastAPI, Request
import os
import requests

app = FastAPI()
HF_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
MODEL = "mistralai/Mistral-7B-Instruct-v0.1"

@app.post("/chat")
async def chat(request: Request):
    body = await request.json()
    user_input = body.get("message")
    
    response = requests.post(
        f"https://api-inference.huggingface.co/models/{MODEL}",
        headers={"Authorization": f"Bearer {HF_API_KEY}"},
        json={"inputs": user_input}
    )
    result = response.json()
    return {"response": result}
