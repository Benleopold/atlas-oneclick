from fastapi import FastAPI
import os

app = FastAPI()

@app.get("/")
def read_root():
    return {
        "message": "Atlas is live!",
        "huggingface": os.getenv("HUGGINGFACE_API_KEY"),
        "db": os.getenv("DATABASE_URL")
    }