import sys

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


PROJECT_DIR = "/content/agentic_mcp_chatbot"


def server_parameters():
    return StdioServerParameters(
        command=sys.executable,
        args=["-m", "mcp_server.server"],
        cwd=PROJECT_DIR
    )


async def call_mcp_tool(tool_name, arguments):
    params = server_parameters()

    async with stdio_client(
        params,
        errlog=sys.__stderr__
    ) as (read, write):

        async with ClientSession(
            read,
            write
        ) as session:

            await session.initialize()

            result = await session.call_tool(
                tool_name,
                arguments
            )

            return result
