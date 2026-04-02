# gradio_chatbot

Minimal Gradio chatbot example that uses the OpenAI chat API.

Setup
-
1. Create a virtual environment and install dependencies:

```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

2. Copy `.env.example` to `.env` and set `OPENAI_API_KEY` (optional):

```bash
copy .env.example .env
# Edit .env to add your API key
```

Running
-
```bash
python app.py
```

Notes
-
- If `OPENAI_API_KEY` is not set, the app runs in a fallback mode that echoes the last user message, allowing local testing without an API key.
- The actual model and generation parameters can be overridden via environment variables: `MODEL_NAME`, `TEMPERATURE`, `MAX_TOKENS`.
