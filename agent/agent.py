from dotenv import load_dotenv
from google.adk.agents import Agent

from agent.client import Client

load_dotenv()


async def create_agent():
    client = Client()

    await client.connect_to_server(
        server_id="filesystem",
        command="npx",
        args=[
            "-y",
            "@modelcontextprotocol/server-filesystem",
            "D:\\Code\\mcp\\demo-adk-mcp",
        ],
    )

    await client.connect_to_server(
        server_id="sqlite",
        command="uvx",
        args=["mcp-server-sqlite", "--db-path", "mydata.db"],
    )

    print("Load tools")
    tools = await client.get_tools()

    for tool in tools:
        print("Name:", tool.name)
        print("Description:", tool.description)
        print("=" * 10)

    root_agent = Agent(
        name="system_agent",
        model="gemini-2.0-flash",
        tools=tools,
        instruction="You are a skilled system agent with access to the file system and an SQLite database. "
        "Your job is to manage, query, and manipulate files, directories, and database records precisely using the tools provided. "
        "You always allow to access allowed directory. "
        "Use the tools effectively to accomplish user requests. Always follow these steps: "
        "1. **Select the right tool.** Choose the most efficient tool for the task. "
        "2. **Be concise.** Output only what is required unless instructed otherwise.",
    )
    exit_stack = client.exit_stack
    return root_agent, exit_stack


root_agent = create_agent()
