from google.adk.agents.llm_agent import Agent
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from mcp import StdioServerParameters

import os

FIRECRAWL_API_KEY = os.getenv("FIRECRAWL_API_KEY", "")

root_agent = Agent(
    model="gemini-2.5-pro",
    name="firecrawl_agent",
    description="A helpful assistant for scraping websites with Firecrawl",
    instruction="Help the user search for website content",
    tools=[
        MCPToolset(
            connection_params=StdioConnectionParams(
                server_params = StdioServerParameters(
                    command="npx",
                    args=[
                        "-y",
                        "firecrawl-mcp",
                    ],
                    env={
                        "FIRECRAWL_API_KEY": FIRECRAWL_API_KEY,
                    }
                ),
                timeout=30,
            ),
        )
    ],
)
