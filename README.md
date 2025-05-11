A simple agent built with Google ADK and MCP.

## Prerequisites

- [Python](https://www.python.org/downloads/)
- [Node.js](https://nodejs.org/en/download/)
- [uv](https://docs.astral.sh/uv/getting-started/installation/)

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

4. Run the agent
   ```bash
   uv run adk web
   ```

##
