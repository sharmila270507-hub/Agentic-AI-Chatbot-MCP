from mcp.server.fastmcp import FastMCP

from .tools import (
    calculator,
    word_count,
    web_search
)


mcp = FastMCP("Agentic Tools")


@mcp.tool()
def calculate(expression: str) -> str:
    """Calculate a mathematical expression."""
    return calculator(expression)


@mcp.tool()
def count_words(text: str) -> str:
    """Count the number of words in text."""
    return word_count(text)


@mcp.tool()
def search_web(query: str) -> str:
    """Search the web for current information."""
    return web_search(query)


if __name__ == "__main__":
    mcp.run()
