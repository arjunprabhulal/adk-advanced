# ADK Function Tool - Order Status

An ADK agent that demonstrates creating custom function tools. This agent uses a `FunctionTool` to check order status.

## Overview

This agent shows how to create custom tools using the `FunctionTool` wrapper. The agent can check the status of orders using a custom function.

**What is a Function Tool?** A Function Tool allows you to wrap any Python function and make it available to your ADK agent. The agent can automatically call these functions based on user queries, enabling it to perform custom operations beyond built-in capabilities.

## Project Structure

```
adk_custom_tool_agent/
├── agent.py         # Main agent code with custom FunctionTool
├── __init__.py      # Package initialization
└── .env.example     # Example environment variables template
```

## Prerequisites

- Python 3.11 or later
- Google ADK installed (see parent directory README for installation instructions)
- Google API key from [Google AI Studio](https://aistudio.google.com/apikey)

## Setup

1. Create a `.env` file with your API key and configuration:

Copy the example environment file and update it with your API key:

```bash
cp .env.example .env
```

Then edit `.env` and replace `"your-api-key"` (or `"YOUR_API_KEY"`) with your actual Google API key.

**Environment Variables:**
- `GOOGLE_GENAI_USE_VERTEXAI=False`: Use AI Studio (Gemini API) instead of Vertex AI
- `GOOGLE_API_KEY`: Your Google API key from [Google AI Studio](https://aistudio.google.com/apikey)

## Usage

### Run with Command Line Interface

From the `1_adk_tools` directory:

```bash
adk run adk_custom_tool_agent
```

### Run with Web Interface

From the `1_adk_tools` directory:

```bash
adk web
```

Then open the URL shown in the terminal (typically `http://localhost:8000`) in your browser and select the agent.

## Agent Details

- **Google ADK Version**: `1.18.0`
- **Model**: `gemini-2.5-flash`
- **Tool**: Custom `FunctionTool` wrapping `get_order_status` function
- **Capabilities**: Check order status by order ID

## Custom Tool Implementation

The agent includes a custom function:

```python
def get_order_status(order_id: str):
    """Retrieves the status of an order by order ID."""
    return {"order_id": order_id, "status": "Shipped", "delivery_date": "Nov 4, 2025"}
```

This function is wrapped with `FunctionTool` to make it available to the agent:

```python
tools=[FunctionTool(get_order_status)]
```

## Demo

![Custom Function Tool Agent Demo](../../images/custom_tool_demo.png)

## Extending the Tool

You can extend this example by:
- Connecting to a real order database
- Adding more order-related functions
- Implementing authentication
- Adding error handling

## References

- [ADK Documentation](https://google.github.io/adk-docs/)
- [Function Tools](https://google.github.io/adk-docs/tools/function-tools/)
- [Python Quickstart](https://google.github.io/adk-docs/get-started/python/)

