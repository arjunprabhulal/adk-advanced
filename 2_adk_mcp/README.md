# ADK MCP

This directory contains implementations demonstrating Model Context Protocol (MCP) integration with ADK agents.

## Table of Contents

- [Overview](#overview)
- [Project Structure](#project-structure)
- [Implementations](#implementations)
  - [GitHub MCP Agent](#github-mcp-agent)
  - [Firecrawl MCP Agent](#firecrawl-mcp-agent)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Usage](#usage)
- [References](#references)

## Overview

MCP (Model Context Protocol) allows agents to connect to external services and tools through a standardized protocol. This enables agents to access a wide variety of third-party services and APIs.

**MCP Tools** provide a standardized way to connect ADK agents to external services like GitHub, Firecrawl, and other third-party APIs through the Model Context Protocol.

## Project Structure

```
2_adk_mcp/
├── adk_mcp_github_agent/
│   ├── agent.py         # Agent definition with GitHub MCP toolset
│   ├── __init__.py      # Package initialization
│   └── .env.example     # Example environment variables template
├── adk_mcp_firecrawl_agent/
│   ├── agent.py         # Agent definition with Firecrawl MCP client
│   ├── __init__.py      # Package initialization
│   └── .env.example     # Example environment variables template
├── requirements.txt     # Python dependencies
└── README.md            # This file
```

## Implementations

### GitHub MCP Agent

Demonstrates connecting to GitHub via MCP toolset using the GitHub Copilot MCP API.

**Key Features:**
- MCP toolset integration
- GitHub API access
- Read-only operations
- Bearer token authentication

**Directory:** [adk_mcp_github_agent/](adk_mcp_github_agent/)

**See:** [adk_mcp_github_agent/README.md](adk_mcp_github_agent/README.md)

### Firecrawl MCP Agent

Demonstrates using Firecrawl MCP client for web scraping and crawling capabilities.

**Key Features:**
- Firecrawl MCP integration
- Web scraping capabilities
- Content extraction
- Stdio connection via npx

**Directory:** [adk_mcp_firecrawl_agent/](adk_mcp_firecrawl_agent/)

**See:** [adk_mcp_firecrawl_agent/README.md](adk_mcp_firecrawl_agent/README.md)

## Getting Started

### Prerequisites

- Python 3.11 or later
- `uv` or `pip` package manager
- Google API key from [Google AI Studio](https://aistudio.google.com/apikey)
- Service-specific tokens (e.g., GitHub token, Firecrawl API key)

### Installation

Install dependencies using `uv` (recommended) or `pip`:

**Using uv:**
```bash
# Install uv if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create virtual environment (if needed)
uv venv

# Install dependencies
uv pip install -r requirements.txt
```

**Using pip:**
```bash
# Create and activate virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Usage

1. Navigate to any implementation directory
2. Follow the README.md in that directory
3. Set up your `.env` file with required API keys and tokens
4. Run from this directory (`2_adk_mcp`) with:
   - `adk run <agent-name>` for CLI
   - `adk web` for web interface (then select the agent in the browser)

## References

- [ADK MCP Tools Documentation](https://google.github.io/adk-docs/tools/mcp-tools/)
- [MCP Protocol](https://modelcontextprotocol.io/)
- [Third-party Tools](https://google.github.io/adk-docs/tools/third-party/)
