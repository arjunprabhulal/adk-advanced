# Agent Starter Pack - Remote Template (RAG - Production-ready)

This directory contains a **production-ready RAG agent remote template** that can be used with Agent Starter Pack to create new agent projects from a Git repository.

## Table of Contents

- [Overview](#overview)
- [What is a Remote Template?](#what-is-a-remote-template)
- [Project Structure](#project-structure)
- [Implementation](#implementation)
- [Using This Template](#using-this-template)
- [Getting Started](#getting-started)
  - [Creating a New Project](#creating-a-new-project)
  - [Using the Existing Implementation](#using-the-existing-implementation)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
    - [Deployment](#deployment)
- [References](#references)

## Overview

This is a **remote template** for Agent Starter Pack that demonstrates a complete RAG (Retrieval-Augmented Generation) agent implementation using Vertex AI RAG Engine, deployed to Vertex AI Agent Engine. 

**Key Features:**
- Production-ready RAG agent with Vertex AI RAG Engine integration
- Full deployment infrastructure (Terraform, CI/CD pipelines)
- Agent Engine deployment configuration
- Testing and evaluation frameworks
- Complete project structure with best practices

## What is a Remote Template?

Remote templates allow you to create production-ready AI agents from Git repositories using Agent Starter Pack. Any Git repository can be used as a template - the system automatically handles fetching, configuration, and generating your complete agent project.

When you use a remote template, the system:
1. **Fetches** the template repository from Git
2. **Checks for version locking** - if the template specifies a starter pack version in `uv.lock`, automatically uses that version for guaranteed compatibility
3. **Applies intelligent defaults** based on repository structure
4. **Merges** template files with base agent infrastructure
5. **Generates** a complete, production-ready agent project

For more information, see [Using Remote Templates](https://googlecloudplatform.github.io/agent-starter-pack/remote-templates/using-remote-templates.html).

## Project Structure

```
6_adk_deploy_rag_to_agent_engine/
├── adk_rag_agent_engine_demo/
│   ├── deployment/             # Infrastructure and deployment scripts
│   │   ├── deploy.py           # Deployment script
│   │   ├── grant_permissions.sh # Permission setup script
│   │   ├── run.py              # Testing script for deployed agent
│   │   └── terraform/          # Terraform infrastructure as code
│   ├── eval/                   # Evaluation framework
│   │   ├── data/               # Test data and configuration
│   │   └── test_eval.py        # Evaluation test script
│   ├── notebooks/              # Jupyter notebooks for prototyping and evaluation
│   ├── rag/                    # Core application code
│   │   ├── agent.py            # Main agent logic with VertexAiRagRetrieval
│   │   ├── agent_engine_app.py # Agent Engine application logic
│   │   ├── prompts.py          # Agent prompts
│   │   ├── shared_libraries/   # Shared utilities
│   │   │   └── prepare_corpus_and_data.py # RAG corpus preparation script
│   │   └── utils/              # Utility functions and helpers
│   ├── tests/                  # Unit, integration, and load tests
│   ├── .env.example            # Example environment variables template
│   ├── .gitignore              # Git ignore patterns
│   ├── deployment_metadata.json # Deployment metadata (created/updated after deployment)
│   ├── GEMINI.md               # AI-assisted development guide
│   ├── Makefile                # Makefile for common commands
│   ├── pyproject.toml          # Project dependencies and configuration
│   ├── RAG_architecture.png    # RAG architecture diagram
│   ├── RAG_workflow.png        # RAG workflow diagram
│   ├── README.md               # Project-specific README
│   ├── starter_pack_README.md  # Agent Starter Pack README
│   └── uv.lock                  # Locked dependency versions
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## Implementation

### adk_rag_agent_engine_demo

A complete RAG agent template that demonstrates:
- Vertex AI RAG Engine integration using `VertexAiRagRetrieval` tool
- Agent Engine deployment with full infrastructure
- Terraform configuration for GCP resources
- CI/CD pipelines (Cloud Build or GitHub Actions)
- Testing frameworks and evaluation notebooks
- Data ingestion pipeline for RAG corpus preparation

**Directory:** [adk_rag_agent_engine_demo/](adk_rag_agent_engine_demo/)

**See:** [adk_rag_agent_engine_demo/README.md](adk_rag_agent_engine_demo/README.md) for detailed project-specific instructions.

## Using This Template

You can create a new RAG agent project using the `adk@rag` template from Google's ADK samples:

**Using the `adk@rag` template (Recommended):**
```bash
uvx agent-starter-pack create adk-rag-agent-engine-demo -a adk@rag
```

**RAG Remote Template Installation:**

![RAG Remote Template Installation](../images/rag-template.gif)

This command will:
1. Fetch the RAG template from `google/adk-samples`
2. Automatically detect and use the required Agent Starter Pack version (e.g., `0.19.1`)
3. Guide you through interactive prompts:
   - **Deployment Target**: Select `1` for Vertex AI Agent Engine
   - **CI/CD Runner**: Select `1` for Google Cloud Build or `2` for GitHub Actions
   - **GCP Region**: Enter your preferred region (default: `us-central1`)
   - **Project Confirmation**: Confirm your GCP project and account
4. Generate a complete production-ready project structure

**Example Interactive Session:**
```
> Please select a deployment target:
  1. Vertex AI Agent Engine - Vertex AI Managed platform for scalable agent deployments
  2. Cloud Run - GCP Serverless container execution
Enter the number of your deployment target choice (1): 1

> Please select a CI/CD runner:
  1. Google Cloud Build - Fully managed CI/CD, deeply integrated with GCP
  2. GitHub Actions - CI/CD with secure workload identity federation
Enter the number of your CI/CD runner choice (1): 1

Enter desired GCP region (us-central1): us-central1

> You are logged in with account: 'your-email@gmail.com'
> You are using project: 'your-project-id'
> Do you want to continue? [Y/skip/edit] (Y): Y

> Successfully configured project: your-project-id
> Testing GCP and Vertex AI Connection...
✔ Successfully verified connection to Vertex AI

> Success! Your agent project is ready.
```

**After Creation:**
```bash
cd adk-rag-agent-engine-demo
make install && make playground
```

> **Note**: The `adk@rag` template is the official RAG template from Google's ADK samples repository. It includes version locking in `uv.lock` to ensure compatibility with the correct Agent Starter Pack version.

## Getting Started

### Creating a New Project

To create a new RAG agent project, use the Agent Starter Pack CLI:

```bash
uvx agent-starter-pack create adk-rag-agent-engine-demo -a adk@rag
```

Follow the interactive prompts to configure your deployment target, CI/CD runner, and GCP settings. See the [Using This Template](#using-this-template) section above for details.

### Using the Existing Implementation

If you want to use or modify the existing `adk_rag_agent_engine_demo` implementation directly, follow the steps below:

#### Prerequisites

- Python 3.11 or later
- `uv` or `pip` package manager
- Google Cloud Project with billing enabled
- Vertex AI RAG Engine access
- Required APIs enabled (Agent Engine, Cloud Build, Vertex AI)
- Terraform installed (for infrastructure deployment)
- Google Cloud SDK installed and authenticated
- Appropriate IAM permissions

#### Installation

**Install dependencies at the parent directory level** (`6_adk_deploy_rag_to_agent_engine/`):

**Using uv (recommended):**
```bash
# Navigate to parent directory
cd 6_adk_deploy_rag_to_agent_engine

# Install uv if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create virtual environment (if needed)
uv venv

# Install dependencies
uv pip install -r requirements.txt
```

**Using pip:**
```bash
# Navigate to parent directory
cd 6_adk_deploy_rag_to_agent_engine

# Create and activate virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

#### Deployment

**Navigate to the implementation directory and deploy:**

```bash
# Navigate to the agent project
cd adk_rag_agent_engine_demo

# Set up environment variables (create .env from .env.example)
cp .env.example .env
# Edit .env with your configuration

# Set your GCP project
gcloud config set project YOUR_DEV_PROJECT_ID
```

**Before deploying, you need to create a RAG corpus:**

**RAG Corpus Creation Process:**

![RAG Corpus Creation](../images/corpus-creation.gif)

> **⚠️ Warning: Billing Charges**
> 
> Creating a RAG corpus automatically provisions a RagManagedDb Spanner instance, which will incur charges. If you're just testing or experimenting with this repository, **delete the corpus after you're done** to avoid ongoing charges. You can delete the corpus from the Vertex AI Console or using the `gcloud ai rag-corpora delete` command.

For detailed instructions on creating a RAG corpus, see the [corpus setup section](adk_rag_agent_engine_demo/README.md#how-to-upload-my-file-to-my-rag-corpus) in the child README.

**Deploy the agent:**

```bash
# Option A: Quick development deployment
make setup-dev-env  # Provision GCP resources
make deploy         # Deploy to Agent Engine

# Option B: Production CI/CD pipeline (recommended)
uvx agent-starter-pack setup-cicd
```

> **Note**: For detailed deployment instructions, see [adk_rag_agent_engine_demo/README.md](adk_rag_agent_engine_demo/README.md)

## References

- [How to Build a Production-Grade RAG with ADK & Vertex AI RAG Engine via the Agent Starter Pack](https://medium.com/google-cloud/how-to-build-a-production-grade-rag-with-adk-vertex-ai-rag-engine-via-the-agent-starter-pack-7e39e9cfe856) - Comprehensive guide on building and deploying production-ready RAG applications
- [Agent Starter Pack - Remote Templates](https://googlecloudplatform.github.io/agent-starter-pack/remote-templates/using-remote-templates.html)
- [Using Remote Templates Guide](https://googlecloudplatform.github.io/agent-starter-pack/remote-templates/using-remote-templates.html)
- [Google ADK Agent Engine Deployment](https://google.github.io/adk-docs/deploy/agent-engine/)
- [Vertex AI RAG Engine](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/rag-engine/rag-overview)
- [Agent Starter Pack Documentation](https://googlecloudplatform.github.io/agent-starter-pack/)
