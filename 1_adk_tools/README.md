# ADK Tools

This directory contains implementations demonstrating different types of tools available in the Agent Development Kit (ADK).

## Table of Contents

- [Overview](#overview)
- [Project Structure](#project-structure)
- [Implementations](#implementations)
  - [Built-in Tool Agent](#built-in-tool-agent)
  - [Custom Function Tool Agent](#custom-function-tool-agent)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Usage](#usage)
- [Demo](#demo)
  - [Built-in Tool Demo](#built-in-tool-demo)
  - [Custom Function Tool Demo](#custom-function-tool-demo)
- [References](#references)

## Overview

Tools extend the capabilities of ADK agents by providing access to external functions, APIs, and services. This section covers built-in tools and custom function tools.

**Built-in Tools** are pre-configured tools provided by Google ADK, such as `google_search`, that require no additional setup.

**Function Tools** allow you to wrap any Python function and make it available to your ADK agent, enabling custom operations beyond built-in capabilities.

## Project Structure

```
1_adk_tools/
├── adk_builtin_tool_agent/
│   ├── agent.py         # Agent definition with built-in google_search tool
│   ├── __init__.py      # Package initialization
│   └── .env.example     # Example environment variables template
├── adk_custom_tool_agent/
│   ├── agent.py         # Agent definition with custom FunctionTool
│   ├── __init__.py      # Package initialization
│   └── .env.example     # Example environment variables template
├── requirements.txt     # Python dependencies
└── README.md            # This file
```

## Implementations

### Built-in Tool Agent

Demonstrates using ADK's built-in `google_search` tool to enable agents to search the web and retrieve real-time information.

**Key Features:**
- Built-in tool integration
- Real-time web search capabilities
- No additional setup required

**Directory:** [adk_builtin_tool_agent/](adk_builtin_tool_agent/)

**See:** [adk_builtin_tool_agent/README.md](adk_builtin_tool_agent/README.md)

### Custom Function Tool Agent

Demonstrates creating custom tools using the `FunctionTool` wrapper to add domain-specific functionality to agents.

**Key Features:**
- Custom function tool creation
- Type hints for tool parameters
- Function wrapping with `FunctionTool`

**Directory:** [adk_custom_tool_agent/](adk_custom_tool_agent/)

**See:** [adk_custom_tool_agent/README.md](adk_custom_tool_agent/README.md)

## Getting Started

### Prerequisites

- Python 3.11 or later
- `uv` or `pip` package manager
- Google API key from [Google AI Studio](https://aistudio.google.com/apikey)

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
3. Set up your `.env` file with required API keys
4. Run from this directory (`1_adk_tools`) with:
   - `adk run <agent-name>` for CLI
   - `adk web` for web interface (then select the agent in the browser)

## Demo

### Built-in Tool Demo

**User:** "what is price of SP500 today"

**Agent:** Uses `google_search` to retrieve current S&P 500 index information:
- Current S&P 500 Index: "On Monday, November 10, 2025, the S&P 500 index is around 6,810.52 USD, having risen by 0.13% in the past 24 hours."
- Other sources show the S&P 500 at approximately 6,781.49 USD, 6,799.23, and 6,728.80.
- Highest Quote Ever: "The S&P 500 reached its highest quote ever on October 28, 2025, at 6,920.34 USD."

The agent automatically uses the built-in `google_search` tool to find real-time information and provides comprehensive results from multiple sources.

### Custom Function Tool Demo

**User:** "what can you do?"

**Agent:** "I can help you retrieve the status of an order by its order ID. What is the order ID you would like to check?"

**User:** "what is order id 1234?"

**Agent:** 
- Calls tool: `get_order_status`
- Tool execution: Success
- Response: "The order with ID 1234 has been Shipped and will be delivered on Nov 24, 2025."

The agent automatically detects when to use the custom function tool and executes it to retrieve the order information.

## References

- [ADK Tools Documentation](https://google.github.io/adk-docs/tools/)
- [Built-in Tools](https://google.github.io/adk-docs/tools/built-in-tools/)
- [Function Tools](https://google.github.io/adk-docs/tools/function-tools/)
