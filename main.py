from fastapi import FastAPI, Request
from pydantic import BaseModel
import os
import requests

app = FastAPI()

class ChatRequest(BaseModel):
    prompt: str
    model: str  # 'gpt', 'claude', or 'huggingface'

@app.get("/")
def read_root():
    return {
        "message": "Atlas is live!",
        "huggingface": os.getenv("HF_API_KEY"),
        "openai": os.getenv("OPENAI_API_KEY_ATLAS"),
        "anthropic": os.getenv("ANTHROPIC_API_KEY_ATLAS"),
        "db": os.getenv("DATABASE_URL")
    }

@app.post("/chat")
def chat(req: ChatRequest):
    if req.model == "gpt":
        api_key = os.getenv("OPENAI_API_KEY_ATLAS")
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": req.prompt}]
        }
        response = requests.post("https://api.openai.com/v1/chat/completions", json=payload, headers=headers)
        return response.json()

    elif req.model == "claude":
        api_key = os.getenv("ANTHROPIC_API_KEY_ATLAS")
        headers = {
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "claude-3-sonnet-20240229",
            "max_tokens": 1000,
            "messages": [{"role": "user", "content": req.prompt}]
        }
        response = requests.post("https://api.anthropic.com/v1/messages", json=payload, headers=headers)
        return response.json()

    elif req.model == "huggingface":
        api_key = os.getenv("HF_API_KEY")
        headers = {
            "Authorization": f"Bearer {api_key}"
        }
        data = {
            "inputs": req.prompt
        }
        response = requests.post("https://api-inference.huggingface.co/models/gpt2", headers=headers, json=data)
        return response.json()

    else:
        return {"error": "Invalid model. Choose 'gpt', 'claude', or 'huggingface'."}
        
