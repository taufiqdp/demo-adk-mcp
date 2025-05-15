from contextlib import AsyncExitStack
from typing import Any, List, Optional, Tuple, Union

from google.adk.tools.mcp_tool import MCPTool
from google.adk.tools.mcp_tool.mcp_session_manager import (MCPSessionManager,
                                                           SseServerParams)
from mcp import ClientSession, StdioServerParameters
from mcp.client.sse import sse_client
from mcp.client.stdio import stdio_client


class Client:
    def __init__(self):
        self.exit_stack: AsyncExitStack = AsyncExitStack()
        self.sessions: dict = {}
        self.session_managers: dict = {}

    async def _connect_to_server(
        self,
        server_id: str,
        server_params: Union[StdioServerParameters, SseServerParams],
        transport: Tuple[Any],
    ):
        print(f"Connecting to server {server_id}")
        read_stream, write_stream = transport

        session = await self.exit_stack.enter_async_context(
            ClientSession(read_stream=read_stream, write_stream=write_stream)
        )

        self.sessions[server_id] = session

        self.session_managers[server_id] = MCPSessionManager(
            connection_params=server_params, exit_stack=self.exit_stack
        )

        await session.initialize()

        print(f"Connected to server {server_id}")

    async def connect_to_stdio_server(
        self, server_id: str, command: str, args: List[str]
    ) -> None:
        server_params = StdioServerParameters(command=command, args=args)

        stdio_transport = await self.exit_stack.enter_async_context(
            stdio_client(server=server_params)
        )

        await self._connect_to_server(
            server_id=server_id, server_params=server_params, transport=stdio_transport
        )

    async def connect_to_sse_server(self, server_id: str, url: str) -> None:
        server_params = SseServerParams(url=url)

        sse_transport = await self.exit_stack.enter_async_context(
            sse_client(url=server_params.url)
        )

        await self._connect_to_server(
            server_id=server_id, server_params=server_params, transport=sse_transport
        )

    async def get_tools(self, server_id: Optional[str] = None) -> List[MCPTool]:
        all_tools = []

        if server_id:
            session = self.sessions[server_id]
            tools = await session.list_tools()
            all_tools.extend(
                [
                    MCPTool(
                        mcp_tool=tool,
                        mcp_session=session,
                        mcp_session_manager=self.session_managers[server_id],
                    )
                    for tool in tools.tools
                ]
            )

        else:
            for server_id, session in self.sessions.items():
                tools = await session.list_tools()
                all_tools.extend(
                    [
                        MCPTool(
                            mcp_tool=tool,
                            mcp_session=session,
                            mcp_session_manager=self.session_managers[server_id],
                        )
                        for tool in tools.tools
                    ]
                )

        return all_tools

    async def cleanup(self) -> None:
        await self.exit_stack.aclose()
