# ADK Vertex AI Search

A simple Google ADK agent that uses Vertex AI Search to answer questions from your internal documents.

## Table of Contents

- [Agent Details](#agent-details)
- [Overview](#overview)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Getting Started](#getting-started)
  - [Installation](#installation)
  - [1. Environment Variables](#1-environment-variables)
  - [2. Prepare Vertex AI Search Datastore](#2-prepare-vertex-ai-search-datastore)
  - [3. Configure the Agent](#3-configure-the-agent)
  - [4. Authentication Setup](#4-authentication-setup)
  - [5. Run Your Agent](#5-run-your-agent)
- [Example Prompts to Try](#example-prompts-to-try)
- [Understanding Search Responses](#understanding-search-responses)
- [How It Works](#how-it-works)
- [Troubleshooting](#troubleshooting)
- [References](#references)

## Agent Details

- **Google ADK Version**: `1.18.0`
- **Model**: `gemini-2.5-flash`
- **Tool**: `VertexAiSearchTool`
- **Capabilities**: Search and retrieve information from indexed enterprise documents with automatic source attribution

## Overview

**Vertex AI Search** is Google Cloud's enterprise-grade retrieval and search service that lets you build AI-powered search and retrieval systems across private data such as documents, websites, databases, or cloud storage without managing any search infrastructure. It's part of the Vertex AI Agent Platform and often used inside RAG (Retrieval-Augmented Generation) pipelines or chatbots to fetch relevant information before LLM reasoning.

This agent demonstrates how to use the `VertexAiSearchTool` to connect to your indexed documents and retrieve relevant information to generate accurate, context-aware responses with proper source attribution.

## Project Structure

```
7_adk_vertex_ai_search_simple/
├── vertex_search_agent/
│   ├── agent.py         # Agent definition with VertexAiSearchTool
│   ├── __init__.py      # Package initialization
│   └── .env.example     # Example environment variables template
├── requirements.txt     # Python dependencies
└── README.md            # This file
```

## Prerequisites

- Python 3.11 or later
- `uv` or `pip` package manager
- Google Cloud Project with billing enabled
- Vertex AI Search datastore created and populated with documents
- Google Cloud authentication configured

## Getting Started

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

### 1. Environment Variables

Navigate to the `vertex_search_agent/` directory and create a `.env` file from the example:

```bash
cd vertex_search_agent
cp .env.example .env
```

**For Local Development:**
- Set `GOOGLE_GENAI_USE_VERTEXAI=False` and provide `GOOGLE_API_KEY` from [Google AI Studio](https://aistudio.google.com/apikey)
- This uses the Gemini Developer API for rapid prototyping

**For Deployment to Vertex AI (Recommended):**
- Set `GOOGLE_GENAI_USE_VERTEXAI=True` with `GOOGLE_CLOUD_PROJECT` and `GOOGLE_CLOUD_LOCATION`
- Uses Application Default Credentials (ADC) - no API key needed
- Provides access to Vertex AI enterprise features

**Environment Variables:**
- `GOOGLE_GENAI_USE_VERTEXAI`: `True` for Vertex AI (deployment) or `False` for Gemini Developer API (local dev)
- `GOOGLE_API_KEY`: Required when `GOOGLE_GENAI_USE_VERTEXAI=False` (local development)
- `GOOGLE_CLOUD_PROJECT`: Required when `GOOGLE_GENAI_USE_VERTEXAI=True` (deployment)
- `GOOGLE_CLOUD_LOCATION`: Required when `GOOGLE_GENAI_USE_VERTEXAI=True` (deployment)

### 2. Prepare Vertex AI Search Datastore

If you already have a Vertex AI Search Data Store and its Data Store ID, you can skip this section.

**Option A: Using UI Console (Recommended for beginners)**

1. Go to [Vertex AI Search Console](https://console.cloud.google.com/gen-app-builder)
2. Click "Create Data Store"
3. Select the `Unstructured data` tab
4. Configure your data source (Cloud Storage, BigQuery, website, etc.)
5. Upload document from Storage or local computer
6. After creation, open the Data Stores in the console
7. Select the data store you created
8. Find the **Data Store ID** and note it for later use

![Vertex AI Search Datastore](../images/datastore.png)

**Option B: Using gcloud CLI**

Create a datastore using the Discovery Engine API:

```bash
curl -X POST \
  -H "Authorization: Bearer $(gcloud auth print-access-token)" \
  -H "Content-Type: application/json" \
  -H "X-Goog-User-Project: PROJECT_ID" \
  "https://discoveryengine.googleapis.com/v1/projects/PROJECT_ID/locations/global/collections/default_collection/dataStores?dataStoreId=DATA_STORE_ID" \
  -d '{
    "displayName": "DATA_STORE_DISPLAY_NAME",
    "industryVertical": "GENERIC",
    "solutionTypes": ["SOLUTION_TYPE_SEARCH"]
  }'
```

Replace:
- `PROJECT_ID` with your Google Cloud project ID
- `DATA_STORE_ID` with your desired datastore ID
- `DATA_STORE_DISPLAY_NAME` with a display name for your datastore

After creation, get the Data Store ID:
```bash
gcloud discovery-engine data-stores list \
  --project=PROJECT_ID \
  --location=global \
  --collection=default_collection
```

The Data Store ID format is:
```
projects/PROJECT_ID/locations/global/collections/default_collection/dataStores/DATA_STORE_ID
```

### 3. Configure the Agent

Edit `vertex_search_agent/agent.py` and replace the placeholder values in the Configuration section:

```python
DATASTORE_ID = "projects/YOUR_PROJECT_ID/locations/global/collections/default_collection/dataStores/YOUR_DATASTORE_ID"
```

Replace:
- `YOUR_PROJECT_ID` with your Google Cloud project ID
- `YOUR_DATASTORE_ID` with your actual Data Store ID

### 4. Authentication Setup

Set up Google Cloud authentication:

```bash
gcloud auth application-default login
gcloud config set project YOUR_PROJECT_ID
```

### 5. Run Your Agent

From this directory (`7_adk_vertex_ai_search_simple/`):

**Command line:**
```bash
adk run vertex_search_agent
```

**Web interface:**
```bash
adk web
```

Then open the URL shown in your browser and select the agent from the dropdown.

## Example Prompts to Try

- "What is the company's refund policy?"
- "How do I reset my password?"
- "What are the key features of product X?"
- "Summarize the main points from the documentation"

## Understanding Search Responses

When the agent uses Vertex AI Search to retrieve information, it returns:
- **Final answer text**: The generated response incorporating retrieved information
- **Search metadata**: Detailed information about the documents used

The search metadata includes:
- **groundingChunks**: List of enterprise documents the model consulted (title, URI, ID)
- **groundingSupports**: Links specific sentences in the answer back to source documents
- **retrievalQueries**: Shows the search queries executed against your datastore

You can view this metadata in the ADK web UI under the Response tab.

## How It Works

The search and retrieval process follows these steps:

1. **User Query**: You ask a question about internal documents or enterprise data
2. **ADK Orchestration**: ADK passes your message to the agent
3. **LLM Analysis**: The agent's LLM analyzes whether information from your documents is needed
4. **Tool Calling**: If needed, it calls `VertexAiSearchTool` to search your datastore
5. **Document Retrieval**: Vertex AI Search retrieves and ranks relevant document chunks
6. **Context Injection**: Retrieved snippets are integrated into the model's context
7. **Response Generation**: The LLM generates a response incorporating the retrieved information
8. **Source Attribution**: The response includes document references and grounding metadata

## Troubleshooting

**Agent can't find documents:**
- Verify your Data Store ID is correct in `agent.py`
- Ensure documents are fully indexed in your datastore
- Check that your datastore has content

**Authentication errors:**
- Run `gcloud auth application-default login`
- Verify your project has Vertex AI Search API enabled
- Check IAM permissions for Vertex AI Search access

**No response from agent:**
- Check that your datastore contains relevant documents
- Try rephrasing your question
- Verify the agent is using the correct Data Store ID

## References

- [Understanding Vertex AI Search Grounding](https://google.github.io/adk-docs/grounding/vertex_ai_search_grounding/) - Official ADK documentation for Vertex AI Search
- [ADK Documentation](https://google.github.io/adk-docs/)
- [Vertex AI Search Documentation](https://cloud.google.com/generative-ai-app-builder/docs)
