from llm import call_llm
from prompts import SYSTEM_PROMPT


def build_messages(user_message, history):
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    # history is expected as a list of (user, assistant) tuples
    if history:
        for user, assistant in history:
            messages.append({"role": "user", "content": user})
            messages.append({"role": "assistant", "content": assistant})

    messages.append({"role": "user", "content": user_message})
    return messages


def chat(user_message, history):
    """Called by Gradio. Returns a tuple of (chat_history, state).

    - `history` is the existing chat history (list of (user, assistant) pairs).
    - Return value is the updated history for the Chatbot component and the state.
    """
    history = history or []

    messages = build_messages(user_message, history)
    assistant_reply = call_llm(messages)

    history.append((user_message, assistant_reply))

    # For Gradio we return both the chatbot content and the updated state (same object)
    return history, history