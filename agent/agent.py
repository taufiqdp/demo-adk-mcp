from contextlib import AsyncExitStack
from typing import Tuple

from dotenv import load_dotenv
from google.adk.agents import Agent

from agent.client import Client
from agent.prompt import INSTRUCTION

load_dotenv()


async def create_agent() -> Tuple[Agent, AsyncExitStack]:
    client = Client()

    await client.connect_to_server(
        server_id="filesystem",
        command="npx",
        args=[
            "-y",
            "@modelcontextprotocol/server-filesystem",
            "D:\\Code\\mcp\\demo-adk-mcp\\agent\\data",  # replace with your directory
        ],
    )

    await client.connect_to_server(
        server_id="sqlite",
        command="uvx",
        args=["mcp-server-sqlite", "--db-path", "agent/data/mydata.db"],
    )

    tools = await client.get_tools()

    for tool in tools:
        print("Name:", tool.name)
        print("Description:", tool.description)
        print("=" * 10)

    root_agent = Agent(
        name="system_agent",
        model="gemini-2.0-flash",
        tools=tools,
        instruction=INSTRUCTION,
    )

    exit_stack = client.exit_stack
    return root_agent, exit_stack


root_agent = create_agent()
