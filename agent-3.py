import json
import re
import requests

from mcp_client import call_mcp_tool


OLLAMA_URL = "http://127.0.0.1:11434/api/chat"
MODEL = "qwen2.5:1.5b"


def detect_fast_tool(message):
    text = message.lower().strip()

    if (
        text.startswith("calculate ")
        or text.startswith("what is ")
        and any(c.isdigit() for c in text)
    ):
        expression = text
        expression = expression.replace("calculate ", "", 1)
        expression = expression.replace("what is ", "", 1)
        expression = re.sub(r"[^0-9+\-*/(). ]", "", expression)
        if expression.strip():
            return "calculate", {"expression": expression}

    if "count words" in text or "word count" in text:
        if ":" in message:
            content = message.split(":", 1)[1].strip()
        else:
            content = message
        return "count_words", {"text": content}

    search_words = [
        "latest", "recent", "current", "today", "news", "search",
        "what happened", "developments", "weather", "price", "who is"
    ]

    if any(word in text for word in search_words):
        return "search_web", {"query": message}

    return None, None


def ask_qwen(message):
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "messages": [{"role": "user", "content": message}],
            "stream": False,
            "options": {"temperature": 0, "num_predict": 128}
        },
        timeout=60
    )
    response.raise_for_status()
    return response.json()["message"]["content"].strip()


def extract_result(result):
    if hasattr(result, "content"):
        for item in result.content:
            if hasattr(item, "text"):
                return item.text
    return str(result)


async def run_agent(user_message: str):
    tool_name, arguments = detect_fast_tool(user_message)

    if tool_name:
        result = await call_mcp_tool(tool_name, arguments)
        result = extract_result(result)

        if tool_name == "calculate":
            return f"The answer is {result}."

        if tool_name == "count_words":
            return f"The text contains {result} words."

        if tool_name == "search_web":
            return result

    return ask_qwen(user_message)
