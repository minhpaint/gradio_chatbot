import os
from dotenv import load_dotenv

# Load environment variables from .env if present
load_dotenv()

# Read OpenAI API key from environment (do not hardcode keys)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
	# Be explicit - the app should not proceed silently without an API key.
	# Raise here so callers get an immediate, informative error.
	raise RuntimeError(
		"OPENAI_API_KEY not found in environment. Set it in .env or the environment."
	)

# Model and generation settings
MODEL_NAME = "gpt-4o-mini"
TEMPERATURE = 0.7
MAX_TOKENS = 1024
