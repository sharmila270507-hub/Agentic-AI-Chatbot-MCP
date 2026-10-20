import gradio as gr

from agent import run_agent


async def chat(message, history):

    if not message.strip():
        return ""

    try:
        answer = await run_agent(message)
        return answer

    except Exception as e:
        return f"Error: {e}"


demo = gr.ChatInterface(
    fn=chat,
    title="Agentic MCP Chatbot",
    description="Qwen 2.5 1.5B + MCP Tools + Web Search",
    textbox=gr.Textbox(
        placeholder="Ask me anything...",
        container=True
    )
)


if __name__ == "__main__":

    demo.launch(
        share=True,
        debug=True
    )
