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

# Models to try in order (starts with cheapest, fallback to others)
MODELS = [
    "openai/o4-mini",
    "openai/gpt-4.1-mini",
    "anthropic/claude-3-haiku",
    "google/gemini-2.0-flash-exp:free",
    "microsoft/phi-3-mini-128k-instruct:free",
]


def ask(prompt: str) -> str:
    """Send a prompt, trying each model until one responds."""
    for model in MODELS:
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
    raise RuntimeError("All models failed. Try again in a few minutes.")


if __name__ == "__main__":
    print("💬 Local GPT Chat — type your message, or 'exit' to quit.\n")

    history = [
        {"role": "system", "content": "You are a helpful assistant. Reply concisely."}
    ]

    while True:
        user_input = input("You: ").strip()
        if not user_input:
            continue
        if user_input.lower() == "exit":
            print("Goodbye! 👋")
            break

        history.append({"role": "user", "content": user_input})

        for model in MODELS:
            try:
                response = client.chat.completions.create(
                    model=model,
                    messages=history,
                )
                reply = response.choices[0].message.content
                history.append({"role": "assistant", "content": reply})
                print(f"\nAI ({model}): {reply}\n")
                break
            except Exception as e:
                print(f"  [skipping {model}: {e}]")
        else:
            print("All models failed. Try again.\n")
