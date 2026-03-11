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

# Free models to try in order (fallback if one is rate-limited)
# Models with different providers for resilience:
# - Venice provider: qwen, llama, mistral, hermes
# - Google AI Studio: gemma
# - OpenAI infra: gpt-oss
FREE_MODELS = [
    "openai/gpt-oss-20b:free",
    "openai/gpt-oss-120b:free",
    "google/gemma-3-27b-it:free",
    "google/gemma-3-12b-it:free",
    "qwen/qwen3-4b:free",
    "meta-llama/llama-3.3-70b-instruct:free",
    "mistralai/mistral-small-3.1-24b-instruct:free",
]


def ask(prompt: str) -> str:
    """Send a prompt, trying each free model until one responds."""
    for model in FREE_MODELS:
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant. Reply concisely."},
                    {"role": "user", "content": prompt},
                ],
            )
            print(f"  [model used: {model}]")
            return response.choices[0].message.content
        except Exception as e:
            print(f"  [skipping {model}: {e}]")
    raise RuntimeError("All free models failed. Try again in a few minutes.")


if __name__ == "__main__":
    print(f"Available free models: {FREE_MODELS}\n")

    questions = [
        "What is OpenRouter in one sentence?",
        "Name 3 popular free AI models available on OpenRouter.",
        "Write a Python one-liner that reverses a string.",
    ]

    for q in questions:
        print(f"Q: {q}")
        answer = ask(q)
        print(f"A: {answer}\n")
