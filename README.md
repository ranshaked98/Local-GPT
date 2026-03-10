# OpenRouter – Python Starter

A minimal Python project that connects to [OpenRouter](https://openrouter.ai) and runs a conversation using a **free AI model** — no credit card required.

## What is OpenRouter?

OpenRouter is an API gateway that provides access to hundreds of AI models (GPT-4, Claude, Llama, Gemma, Mistral and more) through a **single unified API**, fully compatible with the OpenAI SDK.

- One API key → access to all models
- Pay per token, or use free-tier models at no cost
- Easy to switch between models without changing your code

## Project Structure

```
project2/
├── main.py            # Example: connect and ask questions
├── requirements.txt   # Python dependencies
├── .env.example       # Template for your API key (safe to commit)
├── .env               # Your actual API key (git-ignored!)
└── .gitignore
```

## Setup

### 1. Clone & enter the project folder
```bash
git clone <your-repo-url>
cd project2
```

### 2. Create a virtual environment
```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set your API key
Get a free key at <https://openrouter.ai/keys>, then:
```bash
cp .env.example .env
# Open .env and replace "your_api_key_here" with your real key
```

### 5. Run
```bash
python main.py
```

## Free Models

The project uses `meta-llama/llama-3.1-8b-instruct:free` by default.
Browse all free models at: <https://openrouter.ai/models?q=free>

To switch models, change the `FREE_MODEL` variable in `main.py`.

## Security Note

**Never commit your `.env` file.** It is listed in `.gitignore` to prevent accidental exposure of your API key.
