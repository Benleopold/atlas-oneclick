from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import requests
import os

app = FastAPI()

# Root endpoint just for sanity check
@app.get("/")
def read_root():
    return {
        "message": "Atlas is live!",
        "huggingface": os.getenv("HF_API_KEY"),
        "openai": os.getenv("OPENAI_API_KEY_ATLAS"),
        "anthropic": os.getenv("ANTHROPIC_API_KEY_ATLAS"),
        "db": os.getenv("DATABASE_URL")
    }

# Command endpoint to trigger upgrade_agent
@app.post("/command")
async def handle_command(request: Request):
    try:
        data = await request.json()
        prompt = data.get("prompt", "")

        response = requests.post("http://localhost:8000/command", json={"prompt": prompt})
        return JSONResponse(content=response.json())

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
