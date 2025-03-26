from fastapi import FastAPI
import os

app = FastAPI()

@app.get("/")
def read_root():
    return {
        "message": "Atlas is live!",
        "huggingface": os.getenv("HF_API_KEY"),
        "openai": os.getenv("OPENAI_API_KEY_ATLAS"),
        "anthropic": os.getenv("ANTHROPIC_API_KEY_ATLAS"),
        "db": os.getenv("DATABASE_URL")
    }
    
