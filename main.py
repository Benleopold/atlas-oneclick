from fastapi import FastAPI, Request
import os
import requests
from upgrade_agent import run_upgrade  # Make sure this is included

app = FastAPI()

@app.get("/")
def root():
    return {
        "message": "Atlas is live!",
        "huggingface": os.getenv("HUGGINGFACE_API_KEY"),
        "db": os.getenv("DATABASE_URL")
    }

@app.post("/chat")
async def chat(request: Request):
    body = await request.json()
    message = body.get("message", "")
    model = os.getenv("DEFAULT_MODEL", "claude")

    if model == "claude":
        key = os.getenv("ANTHROPIC_API_KEY")
        response = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "x-api-key": key,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json"
            },
            json={
                "model": "claude-3-sonnet-20240229",
                "messages": [{"role": "user", "content": message}],
                "max_tokens": 1024
            }
        )
        return response.json()

    elif model == "gpt":
        key = os.getenv("OPENAI_API_KEY")
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "gpt-4",
                "messages": [{"role": "user", "content": message}],
                "temperature": 0.7
            }
        )
        return response.json()

    return {"error": "Unsupported model"}

@app.get("/upgrade")
def upgrade():
    return run_upgrade()
    
