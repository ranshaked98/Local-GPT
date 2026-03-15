import os
from openai import OpenAI
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
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

# Allow all origins — needed for ngrok public URLs
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve the frontend folder as static files
FRONTEND_DIR = os.path.join(os.path.dirname(__file__), "..", "frontend")
app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

@app.get("/")
def serve_frontend():
    """Serve index.html at the root URL."""
    return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))

# --- Data model for incoming request ---
class ChatRequest(BaseModel):
    message: str
    history: list = []
    model: str = "openai/o4-mini"   # default if frontend sends nothing

# --- API Endpoint ---
@app.post("/chat")
def chat(req: ChatRequest):
    """Receive a message + history + chosen model, return AI reply."""
    messages = [
        {"role": "system", "content": "Your name is Tamir san. You are a helpful assistant. Reply concisely."},
        *req.history,
        {"role": "user", "content": req.message},
    ]

    # Try the model the user chose first, then fall back to the rest
    preferred = req.model
    fallbacks  = [m for m in MODELS if m != preferred]
    for model in [preferred, *fallbacks]:
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
