import gradio as gr
from chat_handler import chat

CSS = """
/* Container centered and card look */
.app-card {
  max-width: 900px;
  margin: 32px auto;
  padding: 18px;
  border-radius: 12px;
  box-shadow: 0 8px 24px rgba(0,0,0,0.08);
  background: #ffffff;
}

/* Increase chat height and spacing */
#chatbot { max-height: 560px; }

/* Small adjustments for inputs/buttons */
.action-row { display: flex; gap: 8px; align-items: center; }
.grow { flex: 1 1 auto; }

/* Minimal chat bubble hints (non-invasive): override Gradio default message styles if present */
#chatbot .message.user { background-color: #0b93f6 !important; color: white !important; }
#chatbot .message.assistant { background-color: #f1f3f5 !important; color: #111 !important; }

/* Make Markdown header centered */
.app-header { text-align: center; margin-bottom: 6px; }
"""


def _clear_chat():
    return [], []


with gr.Blocks(css=CSS, title="Gradio Chatbot") as demo:
    with gr.Column(elem_classes="app-card"):
        gr.Markdown("# 🤖 Gradio Chatbot", elem_classes="app-header")

        with gr.Row():
            # Main chat column centered inside the card
            with gr.Column():
                chatbot = gr.Chatbot(elem_id="chatbot", height=520)

        # Use a separate state object to hold history; recommended pattern.
        state = gr.State([])

        with gr.Row(elem_classes="action-row"):
            msg = gr.Textbox(
                placeholder="Nhập câu hỏi...",
                label="",
                elem_id="input-box",
                elem_classes="grow",
                autofocus=True,
            )
            send = gr.Button("Send")
            clear = gr.Button("Clear")

        # When the user submits (Enter) or clicks Send, call `chat`.
        msg.submit(fn=chat, inputs=[msg, state], outputs=[chatbot, state])
        send.click(fn=chat, inputs=[msg, state], outputs=[chatbot, state])

        # Clear the input after submit (keeps UX tidy)
        msg.submit(lambda: "", None, msg)
        send.click(lambda: "", None, msg)

        # Clear chat history button
        clear.click(fn=_clear_chat, inputs=None, outputs=[chatbot, state])


if __name__ == "__main__":
    demo.launch()