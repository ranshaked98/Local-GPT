import os
from openai import OpenAI
from dotenv import load_dotenv


# S: Config loading has its own function — one responsibility
def load_api_key() -> str:
    load_dotenv()
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise ValueError(
            "OPENROUTER_API_KEY is not set.\n"
            "1. Copy .env.example to .env\n"
            "2. Get your free key at https://openrouter.ai/keys\n"
            "3. Paste the key in .env"
        )
    return api_key
MODELS = [
    "openai/o4-mini",
    "openai/gpt-4.1-mini",
    "anthropic/claude-3-haiku",
    "google/gemini-2.0-flash-exp:free",
    "microsoft/phi-3-mini-128k-instruct:free",
]

# S: Manages only conversation history
class ChatSession:
    """Keeps track of the conversation history."""

    def __init__(self):
        self.history = [
            {
            "role": "system",
            "content": "You are a helpful assistant. Reply concisely. Your name is Tamir San."
            }
        ]

    def add_user(self, message: str):
        self.history.append({"role": "user", "content": message})

    def add_assistant(self, message: str):
        self.history.append({"role": "assistant", "content": message})


# S: Handles only sending messages to the API
# D: Depends on OpenAI abstraction via base_url — easy to swap provider
class AIClient:
    """Sends messages to OpenRouter, tries each model as fallback."""

    def __init__(self, api_key: str, models: list):
        self.client = OpenAI(api_key=api_key, base_url="https://openrouter.ai/api/v1")
        self.models = models

    def send(self, history: list) -> str:
        for model in self.models:
            try:
                response = self.client.chat.completions.create(
                    model=model,
                    messages=history,
                )
                print(f"  [model used: {model}]")
                return response.choices[0].message.content
            except Exception as e:
                print(f"  [skipping {model}: {e}]")
        raise RuntimeError("All models failed. Try again in a few minutes.")


# S: Handles only the user interaction / chat loop
class ChatLoop:
    """Runs the interactive chat between user and AI."""

    def __init__(self, session: ChatSession, client: AIClient):
        self.session = session
        self.client = client

    def run(self):
        print("💬 Local GPT Chat — type your message, or 'exit' to quit.\n")
        while True:
            user_input = input("You: ").strip()
            if not user_input:
                continue
            if user_input.lower() == "exit":
                print("Goodbye! 👋")
                break

            self.session.add_user(user_input)
            try:
                reply = self.client.send(self.session.history)
                self.session.add_assistant(reply)
                print(f"\nTamir San: {reply}\n")
            except RuntimeError as e:
                print(f"Error: {e}\n")


if __name__ == "__main__":
    api_key = load_api_key()
    client = AIClient(api_key=api_key, models=MODELS)
    session = ChatSession()
    ChatLoop(session=session, client=client).run()

