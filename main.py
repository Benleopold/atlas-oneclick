from fastapi import FastAPI, Request
import os
import httpx

app = FastAPI()

@app.get("/")
def read_root():
    return {
        "message": "Atlas is live!",
        "huggingface": os.getenv("HUGGINGFACE_API_KEY"),
        "db": os.getenv("DATABASE_URL")
    }

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_input = data.get("message", "")
    provider = data.get("provider", "claude")  # claude or openai

    if provider == "openai":
        api_key = os.getenv("OPENAI_API_KEY")
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "gpt-4",
            "messages": [{"role": "user", "content": user_input}]
        }
        async with httpx.AsyncClient() as client:
            res = await client.post("https://api.openai.com/v1/chat/completions", json=payload, headers=headers)
            return res.json()
    else:
        api_key = os.getenv("ANTHROPIC_API_KEY")
        headers = {
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "claude-3-sonnet-20240229",
            "max_tokens": 512,
            "temperature": 0.7,
            "messages": [{"role": "user", "content": user_input}]
        }
        async with httpx.AsyncClient() as client:
            res = await client.post("https://api.anthropic.com/v1/messages", json=payload, headers=headers)
            return res.json()
            
