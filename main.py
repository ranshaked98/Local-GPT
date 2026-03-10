"""
OpenRouter - Simple Example
----------------------------
OpenRouter is an API gateway that gives you access to hundreds of AI models
(GPT-4, Claude, Llama, Gemma, Mistral and more) through a single unified API.
It is fully compatible with the OpenAI SDK — just change the base_url.

Free models are available and don't require billing info.
Full model list: https://openrouter.ai/models?q=free
"""

import os
from openai import OpenAI
from dotenv import load_dotenv

# Load OPENROUTER_API_KEY from .env file
load_dotenv()

api_key = os.getenv("OPENROUTER_API_KEY")
if not api_key:
    raise ValueError(
        "OPENROUTER_API_KEY is not set.\n"
        "1. Copy .env.example to .env\n"
        "2. Get your free key at https://openrouter.ai/keys\n"
        "3. Paste the key in .env"
    )

# Create client — identical to OpenAI SDK but pointing to OpenRouter
client = OpenAI(
    api_key=api_key,
    base_url="https://openrouter.ai/api/v1",
)

# A completely free model (no billing required)
FREE_MODEL = "meta-llama/llama-3.1-8b-instruct:free"


def ask(prompt: str) -> str:
    """Send a prompt to the model and return the text response."""
    response = client.chat.completions.create(
        model=FREE_MODEL,
        messages=[
            {"role": "system", "content": "You are a helpful assistant. Reply concisely."},
            {"role": "user", "content": prompt},
        ],
    )
    return response.choices[0].message.content


if __name__ == "__main__":
    print(f"Using model: {FREE_MODEL}\n")

    questions = [
        "What is OpenRouter in one sentence?",
        "Name 3 popular free AI models available on OpenRouter.",
        "Write a Python one-liner that reverses a string.",
    ]

    for q in questions:
        print(f"Q: {q}")
        answer = ask(q)
        print(f"A: {answer}\n")
