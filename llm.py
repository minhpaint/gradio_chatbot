from openai import OpenAI
from config import OPENAI_API_KEY, MODEL_NAME, TEMPERATURE, MAX_TOKENS

# Instantiate client. The `OpenAI` class will also read from the environment
# if api_key is not provided, but we explicitly pass it for clarity.
client = OpenAI(api_key=OPENAI_API_KEY)


def call_llm(messages):
    """Call the OpenAI Chat Completions endpoint using the new SDK.

    messages should be a list of dicts with `role` and `content` keys.
    Returns the assistant's reply text.
    """
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS,
        )
    except Exception as e:
        # Surface a helpful error message instead of crashing with confusing tracebacks
        raise RuntimeError(f"LLM request failed: {e}")

    # New SDK responses typically expose the message content as shown below.
    # Be defensive: try attribute access, fall back to dict-style access.
    try:
        return response.choices[0].message.content
    except Exception:
        try:
            return response.choices[0]["message"]["content"]
        except Exception:
            raise RuntimeError("Unable to parse LLM response object")