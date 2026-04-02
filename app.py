import gradio as gr
from chat_handler import chat


with gr.Blocks(title="Gradio Chatbot") as demo:
    gr.Markdown("# 🤖 Gradio Chatbot")

    chatbot = gr.Chatbot(elem_id="chatbot", height=400)
    msg = gr.Textbox(
        placeholder="Nhập câu hỏi...",
        label="Message",
        autofocus=True,
    )

    # Use a separate state object to hold history; this is the recommended pattern.
    state = gr.State([])

    # When the user submits, call `chat` which returns (chatbot_history, state)
    msg.submit(fn=chat, inputs=[msg, state], outputs=[chatbot, state])

    # Clear the input after submit
    msg.submit(lambda: "", None, msg)


demo.launch()