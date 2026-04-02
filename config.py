import os
from dotenv import load_dotenv

# Load environment variables from .env if present
load_dotenv()

# Read OpenAI API key from environment (do not hardcode keys)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# If no API key is provided, we run in a safe "fallback" mode which
# doesn't call the OpenAI API. This lets the project run for testing
# or development without an API key.
USE_OPENAI = bool(OPENAI_API_KEY)

# Model and generation settings (allow overrides from environment)
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")
TEMPERATURE = float(os.getenv("TEMPERATURE", "0.7"))
MAX_TOKENS = int(os.getenv("MAX_TOKENS", "1024"))

# If you want strict behaviour (fail when no API key), set
# `OPENAI_API_KEY` in your environment or in a .env file.
