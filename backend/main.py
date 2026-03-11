import os
from openai import OpenAI
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Load API key from .env (one level up)
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))

api_key = os.getenv("OPENROUTER_API_KEY")
if not api_key:
    raise ValueError("OPENROUTER_API_KEY is not set. Check your .env file.")

# --- AI Client ---
client = OpenAI(api_key=api_key, base_url="https://openrouter.ai/api/v1")

MODELS = [
    "openai/o4-mini",
    "openai/gpt-4.1-mini",
    "anthropic/claude-3-haiku",
]

# --- FastAPI App ---
app = FastAPI()

# Allow the frontend (port 5500) to talk to us
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5500", "http://127.0.0.1:5500"],
    allow_methods=["POST"],
    allow_headers=["Content-Type"],
)

# --- Data model for incoming request ---
class ChatRequest(BaseModel):
    message: str
    history: list = []

# --- API Endpoint ---
@app.post("/chat")
def chat(req: ChatRequest):
    """Receive a message + history, return AI reply."""
    messages = [
        {"role": "system", "content": "Your name is Tamir san. You are a helpful assistant. Reply concisely."},
        *req.history,
        {"role": "user", "content": req.message},
    ]

    for model in MODELS:
        try:
            response = client.chat.completions.create(
                model=model,
                messages=messages,
            )
            reply = response.choices[0].message.content
            return {"reply": reply, "model": model}
        except Exception as e:
            print(f"[skipping {model}: {e}]")

    return {"reply": "All models failed. Try again.", "model": None}
