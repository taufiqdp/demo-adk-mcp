A simple agent built with Google ADK and MCP.

## Prerequisites

- [Python](https://www.python.org/downloads/)
- [Node.js](https://nodejs.org/en/download/)
- [uv](https://docs.astral.sh/uv/getting-started/installation/)

### MCP Server

- [Filesystem](https://github.com/modelcontextprotocol/servers/tree/main/src/filesystem)
- [SQLite](https://github.com/modelcontextprotocol/servers/tree/main/src/sqlite)

## How to run

1. Clone the repository

   ```bash
   git clone https://github.com/taufiqdp/demo-adk-mcp
   cd demo-adk-mcp
   ```

2. Install the required packages

   ```bash
   uv sync -U
   ```

3. Configure environment

   ```bash
   cp .env.example .env
   ```

   Edit `.env` file and set the `GOOGLE_API_KEY` to your Gemini API key.

   You can get your Gemini API key from [AI Studio](https://aistudio.google.com/app/apikey).

4. Configure filesystem directory

   Open `agent/agent.py` and locate the `connect_to_stdio_server` function call for "filesystem". Change the directory path to your own directory:

   ```python
   await client.connect_to_stdio_server(
       server_id="filesystem",
       command="npx",
       args=[
           "-y",
           "@modelcontextprotocol/server-filesystem",
           "D:\\Your\\Own\\Directory\\Path",  # replace with your directory
       ],
   )
   ```

   This directory will be used to provide filesystem access to the agent.

5. Run the agent

   ```bash
   uv run adk web --no-reload # for Windows

   uv run adk web # for Linux and MacOS
   ```

   > ⚠️ Windows users need to use the `--no-reload` flag due to this issue: [https://github.com/google/adk-python/issues/387](https://github.com/google/adk-python/issues/387)
