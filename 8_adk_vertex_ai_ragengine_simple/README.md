# ADK Vertex AI RAG Engine

A simple Google ADK agent that uses Vertex AI RAG Engine to answer questions from your knowledge base.

## Table of Contents

- [Agent Details](#agent-details)
- [Overview](#overview)
- [RagManagedDb and Billing](#ragmanageddb-and-billing)
  - [Understanding RagManagedDb](#understanding-ragmanageddb)
  - [Tier Options](#tier-options)
  - [Cost Considerations](#cost-considerations)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Getting Started](#getting-started)
  - [Installation](#installation)
  - [1. Environment Variables](#1-environment-variables)
  - [2. Prepare Vertex AI RAG Engine Corpus](#2-prepare-vertex-ai-rag-engine-corpus)
  - [3. Configure the Agent](#3-configure-the-agent)
  - [4. Authentication Setup](#4-authentication-setup)
  - [5. Run Your Agent](#5-run-your-agent)
- [Example Prompts to Try](#example-prompts-to-try)
- [How It Works](#how-it-works)
- [Configuration Options](#configuration-options)
- [Troubleshooting](#troubleshooting)
- [References](#references)

## Agent Details

- **Google ADK Version**: `1.18.0`
- **Model**: `gemini-2.5-flash`
- **Tool**: `VertexAiRagRetrieval`
- **Capabilities**: Retrieve information from Vertex AI RAG Engine corpus with automatic source attribution

## Overview

**Vertex AI RAG Engine** is a managed service that enables you to build RAG (Retrieval-Augmented Generation) applications by storing and retrieving information from your knowledge base. It provides vector search capabilities and integrates seamlessly with Google ADK agents.

This agent demonstrates how to use the `VertexAiRagRetrieval` tool to connect to your RAG corpus and retrieve relevant information to generate accurate, context-aware responses.

## RagManagedDb and Billing

**Important:** Vertex AI RAG Engine uses `RagManagedDb` by default, which is a fully-managed Google Spanner instance. You will be charged for the use of this Google-managed Spanner instance using standard Spanner SKUs.

### Understanding RagManagedDb

`RagManagedDb` is an enterprise-ready, fully-managed Google Spanner instance used for resource storage by Vertex AI RAG Engine. It stores your RAG corpus and RAG file resource metadata, and can optionally be used as the vector database for your RAG corpora. Through Spanner, Vertex AI RAG Engine offers a consistent, highly available, and highly scalable database.

### Tier Options

Vertex AI RAG Engine provides three tier options that impact performance and cost:

- **Basic tier (default)**: Cost-effective option with 100 processing units (0.1 nodes). Suitable for:
  - Experimenting with RagManagedDb
  - Small data sizes
  - Latency-insensitive workloads
  - Using Vertex AI RAG Engine with other vector databases only

- **Scaled tier**: Production-scale performance with autoscaling (1-10 nodes, 1,000-10,000 processing units). Suitable for:
  - Large amounts of data
  - Performance-sensitive workloads
  - Production applications

- **Unprovisioned tier**: Deletes the RagManagedDb and its underlying Spanner instance, disabling the Vertex AI RAG Engine service and stopping billing. **Warning:** This permanently deletes your data and cannot be recovered.

### Cost Considerations

Billing for Vertex AI RAG Engine is based on:
- The tier configuration you choose (Basic or Scaled)
- The number of RAG corpora
- The volume of data processed
- Standard Spanner pricing for the managed instance

For detailed pricing information, see the [Vertex AI RAG Engine billing documentation](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/rag-engine/rag-engine-billing).

For more information about RagManagedDb, see the [Understanding RagManagedDb documentation](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/rag-engine/understanding-ragmanageddb).

## Project Structure

```
8_adk_vertex_ai_ragengine_simple/
├── adk_rag_agent/
│   ├── agent.py         # Agent definition with VertexAiRagRetrieval
│   ├── __init__.py      # Package initialization
│   └── .env.example     # Example environment variables template
├── requirements.txt     # Python dependencies
└── README.md            # This file
```

## Prerequisites

- Python 3.11 or later
- `uv` or `pip` package manager
- Google Cloud Project with billing enabled
- Vertex AI RAG Engine corpus created and populated with documents
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

Navigate to the `adk_rag_agent/` directory and create a `.env` file from the example:

```bash
cd adk_rag_agent
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

### 2. Prepare Vertex AI RAG Engine Corpus

If you already have a Vertex AI RAG Engine corpus and its corpus ID, you can skip this section.

**Option A: Using UI Console**

1. Go to [Vertex AI Console](https://console.cloud.google.com/vertex-ai)
2. Navigate to **RAG Engine** in the left menu
3. Click **Create Corpus**
4. Enter a display name and description
5. Select your location (e.g., `us-central1`)
6. Click **Create**
7. Upload documents to your corpus:
   - Click **Import Data**
   - Choose your data source (Cloud Storage, local files, etc.)
   - Upload and wait for indexing to complete
8. Copy the **Corpus ID** from the corpus details page

**RAG Corpus Creation Process:**

![RAG Corpus Creation](../images/corpus-creation.gif)

> **⚠️ Warning: Billing Charges**
> 
> Creating a RAG corpus automatically provisions a RagManagedDb Spanner instance, which will incur charges. If you're just testing or experimenting, **delete the corpus after you're done** to avoid ongoing charges. You can delete the corpus from the Vertex AI Console or using the `gcloud ai rag-corpora delete` command.

**Option B: Using gcloud CLI**

Create a corpus using the Vertex AI API:

```bash
gcloud ai rag-corpora create \
  --display-name="YOUR_CORPUS_NAME" \
  --description="Your corpus description" \
  --location=us-central1 \
  --project=PROJECT_ID
```

Upload files to the corpus:

```bash
gcloud ai rag-files import \
  --corpus=CORPUS_ID \
  --source-uris=gs://YOUR_BUCKET/your-file.pdf \
  --location=us-central1 \
  --project=PROJECT_ID
```

Get the corpus ID:

```bash
gcloud ai rag-corpora list \
  --location=us-central1 \
  --project=PROJECT_ID
```

The RAG Corpus ID format is:
```
projects/PROJECT_ID/locations/LOCATION/ragCorpora/CORPUS_ID
```

> **⚠️ Warning: Billing Charges**
> 
> Creating a RAG corpus automatically provisions a RagManagedDb Spanner instance, which will incur charges. If you're just testing or experimenting, **delete the corpus after you're done** to avoid ongoing charges. You can delete the corpus using:
> 
> ```bash
> gcloud ai rag-corpora delete CORPUS_ID \
>   --location=us-central1 \
>   --project=PROJECT_ID
> ```

### 3. Configure the Agent

Edit `adk_rag_agent/agent.py` and replace the placeholder values in the Configuration section:

```python
RAG_CORPUS = "projects/YOUR_PROJECT_ID/locations/us-central1/ragCorpora/YOUR_CORPUS_ID"
```

Replace:
- `YOUR_PROJECT_ID` with your Google Cloud project ID
- `us-central1` with your preferred location (if different)
- `YOUR_CORPUS_ID` with your actual RAG corpus ID

### 4. Authentication Setup

Set up Google Cloud authentication:

```bash
gcloud auth application-default login
gcloud config set project YOUR_PROJECT_ID
```

### 5. Run Your Agent

From this directory (`8_adk_vertex_ai_ragengine_simple/`):

**Command line:**
```bash
adk run adk_rag_agent
```

**Web interface:**
```bash
adk web
```

Then open the URL shown in your browser and select the agent from the dropdown.

## Example Prompts to Try

- "What is the main topic of the documentation?"
- "Explain the key concepts from the knowledge base"
- "What are the important points I should know?"
- "Summarize the relevant information about [topic]"

## How It Works

1. You ask a question to the agent
2. The agent's LLM analyzes whether it needs information from your corpus
3. If needed, it automatically calls `VertexAiRagRetrieval` to search your RAG corpus
4. Relevant document chunks are retrieved based on semantic similarity (top 10 results, similarity threshold 0.6)
5. The agent generates a response using the retrieved information
6. Source citations are included in the response

## Configuration Options

The agent uses the following retrieval settings:

- **similarity_top_k**: `10` - Number of top results to retrieve
- **vector_distance_threshold**: `0.6` - Minimum similarity score threshold

You can adjust these values in `adk_rag_agent/agent.py` to fine-tune retrieval behavior.

## Troubleshooting

**Agent can't find documents:**
- Verify your RAG corpus ID is correct in `agent.py`
- Ensure documents are fully indexed in your corpus
- Check that your corpus has content

**Authentication errors:**
- Run `gcloud auth application-default login`
- Verify your project has Vertex AI API enabled
- Check IAM permissions for Vertex AI RAG Engine access

**No response from agent:**
- Check that your corpus contains relevant documents
- Try rephrasing your question
- Verify the agent is using the correct corpus ID
- Lower the `vector_distance_threshold` if results are too strict

## References

- [ADK Documentation](https://google.github.io/adk-docs/)
- [Vertex AI RAG Engine](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/rag-engine/rag-overview)
- [RAG Engine Quickstart](https://cloud.google.com/vertex-ai/generative-ai/docs/rag-quickstart)
- [RAG Best Practices](https://cloud.google.com/vertex-ai/docs/generative-ai/learn/rag-overview)
- [Understanding RagManagedDb](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/rag-engine/understanding-ragmanageddb)
- [Vertex AI RAG Engine Billing](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/rag-engine/rag-engine-billing)
