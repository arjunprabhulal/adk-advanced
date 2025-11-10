import os
from google.adk.agents import Agent
from google.adk.tools.mcp_tool.mcp_session_manager import StreamableHTTPServerParams
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")

root_agent = Agent(
    model="gemini-2.5-pro",
    name="github_agent",
    instruction="Help users get information from GitHub",
    tools=[
        MCPToolset(
            connection_params=StreamableHTTPServerParams(
                url="https://api.githubcopilot.com/mcp/",
                headers={
                    "Authorization": f"Bearer {GITHUB_TOKEN}",
                    "X-MCP-Toolsets": "all",
                    "X-MCP-Readonly": "true"
                },
            ),
        )
    ],
)