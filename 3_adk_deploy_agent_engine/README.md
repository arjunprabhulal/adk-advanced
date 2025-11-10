# ADK Agent Engine Deployment

This directory contains implementations for deploying Google ADK agents to Vertex AI Agent Engine.

## Which README Should I Read?

**Quick Navigation Guide:**

- **Start here** → Installation README (`3_adk_deploy_agent_engine/README.md`): 
  - Overview and workflow
  - Installation instructions (parent directory level)
  - Quick start guide for using existing implementation
  - Instructions for creating new projects

- **For Deployment - Detailed project info** →  README (`adk_agent_agentengine_demo/README.md`):
  - Project-specific details
  - Detailed deployment steps
  - Complete testing examples with code
  - Environment variable configuration

**Typical Workflow:**
1. Read this README for installation and overview
2. Navigate to `adk_agent_agentengine_demo/` for deployment
3. Refer to child README for detailed project-specific instructions

## Table of Contents

- [Overview](#overview)
- [Quick Start: Using Existing Implementation](#quick-start-using-existing-implementation)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Deployment](#deployment)
  - [Testing](#testing)
- [Creating a New Project](#creating-a-new-project)
- [Available Agent Templates](#available-agent-templates)
- [References](#references)

## Overview

Vertex AI Agent Engine provides a managed platform for deploying, running, and scaling AI agents. These implementations demonstrate how to deploy Google ADK agents to Agent Engine with proper configuration and infrastructure setup.

---

## Quick Start: Using Existing Implementation

**If you want to use the existing `adk_agent_agentengine_demo` implementation**, follow these steps:

### Prerequisites

- Python 3.11 or later
- `uv` or `pip` package manager
- Google Cloud Project with billing enabled
- Required APIs enabled (Agent Engine, Cloud Build, etc.)
- Appropriate IAM permissions
- Terraform installed (for infrastructure deployment)
- Google Cloud SDK installed and authenticated

### Installation

**Install dependencies at the parent directory level** (`3_adk_deploy_agent_engine/`):

**Using uv (recommended):**
```bash
# Navigate to parent directory
cd 3_adk_deploy_agent_engine

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
cd 3_adk_deploy_agent_engine

# Create and activate virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Deployment

**Navigate to the implementation directory and deploy:**

```bash
# Navigate to the agent project
cd adk_agent_agentengine_demo

# Set up environment variables (create .env from .env.example)
cp .env.example .env
# Edit .env with your configuration

# Set your GCP project
gcloud config set project YOUR_DEV_PROJECT_ID

# Option A: Quick development deployment
make setup-dev-env  # Provision GCP resources
make deploy         # Deploy to Agent Engine

# Option B: Production CI/CD pipeline (recommended)
uvx agent-starter-pack setup-cicd
```

> **Note**: For detailed deployment instructions, see [adk_agent_agentengine_demo/README.md](adk_agent_agentengine_demo/README.md)

### Testing

After successful deployment, test your agent:

```bash
# From the adk_agent_agentengine_demo directory
jupyter notebook notebooks/adk_app_testing.ipynb
```

**Testing Methods:**

1. **Jupyter Notebook** (Recommended): The `notebooks/adk_app_testing.ipynb` notebook provides comprehensive testing capabilities:
   - Loads the deployed agent using the Agent Engine ID from `deployment_metadata.json`
   - Tests with streaming queries
   - Compares local vs. remote agent behavior
   - Includes error handling and debugging examples

2. **Google Cloud Console**: Access your agent via the console link provided after deployment for interactive testing

3. **Programmatic Testing**: Use the Python client library to query your deployed agent programmatically

4. **Local Testing**: Use `make playground` to test your agent locally before deployment

The `deployment_metadata.json` file will be automatically updated with your Agent Engine ID after successful deployment. This file contains:
- `remote_agent_engine_id`: The full resource name of your deployed agent
- `deployment_timestamp`: When the deployment was completed

---

## Creating a New Project

**If you want to create a NEW agent project**, use the Agent Starter Pack CLI tool as described below.

The examples in this directory were created using the [Agent Starter Pack](https://github.com/GoogleCloudPlatform/agent-starter-pack) CLI tool. This boilerplate provides a production-ready template with infrastructure, CI/CD, testing, and deployment configurations.

### Prerequisites

Before creating a new agent project, ensure you have:
- `uv` or `uvx` installed ([Install uv](https://docs.astral.sh/uv/getting-started/installation/))
  ```bash
  # On macOS and Linux
  curl -LsSf https://astral.sh/uv/install.sh | sh
  
  # On Windows
  powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
  ```
- `gcloud` CLI installed and authenticated
- `terraform` installed (for infrastructure deployment)
- `git` installed
- `gh` CLI installed (optional, for automated CI/CD setup)

### Creating a New Agent Engine Project

You can use the `pip` workflow for a traditional setup, or `uvx` to create a project in a single command without a permanent install. Choose your preferred method below.

#### Using uvx (Recommended)

This single command downloads and runs the latest version:

```bash
uvx agent-starter-pack create adk_agent_agentengine_demo
```

#### Using pip

```bash
# Create and activate a Python virtual environment
python -m venv .venv && source .venv/bin/activate

# Install the agent starter pack
pip install --upgrade agent-starter-pack

# Create a new agent project
agent-starter-pack create adk_agent_agentengine_demo
```

> **Note**: Replace `adk_agent_agentengine_demo` with your desired project name. The directory name will match the project name you provide.

**No matter which method you choose, the `create` command will:**
- Let you choose an agent template (e.g., `adk_base`, `agentic_rag`)
- Let you select a deployment target (e.g., `cloud_run`, `agent_engine`)
- Generate a complete project structure (backend, optional frontend, deployment infra)

**Examples:**

You can also pass flags to skip the prompts:

```bash
# Using uvx with flags
uvx agent-starter-pack create my-adk-agent -a adk_base -d agent_engine

# Using pip with flags
agent-starter-pack create my-adk-agent -a adk_base -d agent_engine
```

**Interactive Setup Process:**

The CLI will prompt you to make the following selections:

1. **Select Agent Template:**
   - `adk_base` - A base ReAct agent built with Google's Agent Development Kit (ADK)
   - `adk_a2a_base` - ADK agent with Agent2Agent (A2A) Protocol support (experimental)
   - `adk_live` - Real-time multimodal agent with ADK and Gemini Live API
   - `agentic_rag` - ADK RAG agent for document retrieval and Q&A
   - `langgraph_base_react` - Base ReAct agent using LangGraph
   - `crewai_coding_crew` - Multi-agent system implemented with CrewAI
   - Browse agents from `google/adk-samples` - Discover additional samples

2. **Select Deployment Target:**
   - `Vertex AI Agent Engine` - Vertex AI Managed platform for scalable agent deployments
   - `Cloud Run` - GCP Serverless container execution

3. **Select CI/CD Runner:**
   - `Google Cloud Build` - Fully managed CI/CD, deeply integrated with GCP
   - `GitHub Actions` - CI/CD with secure workload identity federation

4. **Enter GCP Region:**
   - Default: `us-central1` (Gemini uses global endpoint by default)

5. **Confirm Project:**
   - The CLI will detect your current GCP project and account
   - Confirm to continue (it will check if Vertex AI is enabled)

**Example Interactive Session:**

```
> Please select a agent to get started:
  1. adk_base - A base ReAct agent built with Google's Agent Development Kit (ADK)
  2. adk_a2a_base - A base ReAct agent with Agent2Agent (A2A) Protocol
  ...
Enter the number of your template choice (1): 1

> Please select a deployment target:
  1. Vertex AI Agent Engine
  2. Cloud Run
Enter the number of your deployment target choice (1): 1

> Please select a CI/CD runner:
  1. Google Cloud Build
  2. GitHub Actions
Enter the number of your CI/CD runner choice (1): 1

Enter desired GCP region (us-central1): us-central1

> You are logged in with account: 'your-email@gmail.com'
> You are using project: 'your-project-id'
> Do you want to continue? [Y/skip/edit] (Y): Y

> Successfully configured project: your-project-id
> Testing GCP and Vertex AI Connection...
> Successfully verified connection to Vertex AI

> Success! Your agent project is ready.
```

### What Gets Created

The starter pack generates a complete project structure including:

```
adk_agent_agentengine_demo/
├── app/                    # Core application code
│   ├── agent.py            # Main agent logic
│   ├── agent_engine_app.py # Agent Engine application logic
│   └── utils/              # Utility functions and helpers
├── .cloudbuild/            # CI/CD pipeline configurations for Google Cloud Build
├── deployment/             # Infrastructure and deployment scripts
├── notebooks/              # Jupyter notebooks for prototyping and evaluation
├── tests/                  # Unit, integration, and load tests
├── Makefile                # Makefile for common commands
├── GEMINI.md               # AI-assisted development guide
└── pyproject.toml          # Project dependencies and configuration
```

### Next Steps After Creation

1. **Navigate to the created project directory:**
   ```bash
   cd adk_agent_agentengine_demo
   ```

2. **Install dependencies and launch local playground:**
   ```bash
   make install && make playground
   ```
   This will:
   - Install all required dependencies using `uv`
   - Launch the Streamlit playground for testing your agent locally

3. **Review the generated README.md** for detailed setup instructions

4. **Customize the agent logic** in `app/agent.py`

5. **Deploy to Agent Engine:**

   **Option A: Development Environment (Quick Deploy)**
   
   For a standalone development environment without the full CI/CD pipeline:
   
   ```bash
   # Set your GCP project
   gcloud config set project YOUR_DEV_PROJECT_ID
   
   # Provision GCP resources for dev environment
   make setup-dev-env
   
   # Deploy Backend to Agent Engine
   make deploy
   ```
   
   The deployment will:
   - Export dependencies to requirements file
   - Create/verify Cloud Storage bucket
   - Deploy agent to Vertex AI Agent Engine
   - Save Agent Engine ID to `deployment_metadata.json`
   - Provide console link and testing instructions
   
   **Option B: Automated CI/CD Pipeline (Recommended for Production)**
   
   For production-ready deployment with automated CI/CD:
   
   ```bash
   # From the project root directory (adk_agent_agentengine_demo/)
   uvx agent-starter-pack setup-cicd
   ```
   
   This command automates:
   - Infrastructure provisioning using Terraform (staging and production environments)
   - CI/CD pipeline setup (Google Cloud Build or GitHub Actions)
   - Repository connection to CI/CD provider
   - Automated testing, staging deployment, and production deployment with manual approval
   
   **Deployment Workflow:**
   - **CI Pipeline**: Runs on pull requests (unit and integration tests)
   - **Staging CD Pipeline**: Runs on merge to `main` (builds, deploys to staging, load testing)
   - **Production Deployment**: Manual approval required, deploys tested container to production
   
   For complete deployment details, see the [Agent Starter Pack Deployment Guide](https://googlecloudplatform.github.io/agent-starter-pack/guide/deployment.html).

6. **Test your deployed agent:**

   After successful deployment, the `deployment_metadata.json` file in the project root is automatically updated with your Agent Engine deployment information. See the [Testing](#testing) section above for details.

---

## Available Agent Templates

The Agent Starter Pack provides several production-ready agent templates designed to accelerate development while offering flexibility to use your preferred agent framework or pattern. For detailed information, see the [Agent Templates Overview](https://googlecloudplatform.github.io/agent-starter-pack/agents/overview.html).

| Agent Name | Description | Use Case |
|------------|-------------|----------|
| `adk_base` | A base ReAct agent implemented using Google's [Agent Development Kit](https://github.com/google/adk-python) | General purpose conversational agent |
| `adk_a2a_base` | An ADK agent with [Agent2Agent (A2A) Protocol](https://a2a-protocol.org/) support | Distributed agent communication and interoperability across frameworks |
| `agentic_rag` | A RAG agent for document retrieval and Q&A with production-ready data ingestion pipeline | Document search and question answering |
| `langgraph_base_react` | A base ReAct agent using LangGraph | Graph based conversational agent |
| `crewai_coding_crew` | A multi-agent system implemented with CrewAI | Collaborative coding assistance |
| `adk_live` | A real-time multimodal RAG agent powered by Gemini Live API | Audio/video/text chat with knowledge base |

#### Template Details

**ADK Base (`adk_base`):**
- Minimal example of a ReAct agent using Google's Agent Development Kit (ADK)
- Demonstrates core ADK concepts: agent creation, tool integration, reasoning, and tool selection
- Ideal for: Getting started with agent development, building general-purpose conversational agents, learning ADK framework

**ADK A2A Base (`adk_a2a_base`):**
- Integrates ADK with Agent2Agent (A2A) Protocol for distributed agent communication
- Enables interoperability across different frameworks and languages
- Ideal for: Building distributed multi-agent systems, microservices-based agent architectures

**Agentic RAG (`agentic_rag`):**
- Built on ADK with production-ready data ingestion pipeline
- Features: Automated data ingestion, flexible datastore options (Vertex AI Search, Vector Search), custom embeddings, answer synthesis
- Ideal for: Document-based question answering, knowledge base integration

**LangGraph Base ReAct (`langgraph_base_react`):**
- ReAct agent using LangGraph for graph-based structures
- Features: Explicit state management, fine-grained control over reasoning cycles, robust tool integration, streaming response support
- Ideal for: Complex multi-step reasoning flows, graph-based agent architectures

**CrewAI Coding Crew (`crewai_coding_crew`):**
- Multi-agent collaboration with LangGraph's conversational control
- Orchestrates specialized agents (Senior Engineer, QA Engineer) for code generation
- Features: Interactive requirements gathering, collaborative code development, sequential task processing
- Ideal for: Complex coding tasks requiring team collaboration simulation

**Live API (`adk_live`):**
- Real-time multimodal conversational RAG agent using Vertex AI Live API
- Features: Audio/video/text interactions, tool calling, WebSocket-based bidirectional communication, production-ready FastAPI backend and React frontend
- Ideal for: Low-latency voice/video chat applications, real-time multimodal interactions

#### Choosing the Right Template

When selecting a template, consider:

1. **Primary Goal**: Conversational bot, Q&A system, task automation, or other use case
2. **Core Pattern/Framework**: Preference for Google ADK, LangChain/LangGraph, CrewAI, or direct RAG implementation
3. **Reasoning Complexity**: Complex planning and tool use (ReAct) vs. retrieval and synthesis (basic RAG)
4. **Collaboration Needs**: Single agent vs. multiple specialized agents working together
5. **Modality**: Text-only vs. audio/video processing and responses

All templates are designed for customization - choose the one closest to your needs and modify as required.

For more information, see the [Agent Templates Overview](https://googlecloudplatform.github.io/agent-starter-pack/agents/overview.html) and [Agent Starter Pack Documentation](https://googlecloudplatform.github.io/agent-starter-pack/).

## Implementations

### adk_agent_agentengine_demo

Complete implementation demonstrating deployment of a Google ADK agent to Vertex AI Agent Engine.

**Key Features:**
- Agent Engine deployment
- Terraform infrastructure as code
- Automated deployment scripts
- Testing and evaluation notebooks

**Directory:** [adk_agent_agentengine_demo/](adk_agent_agentengine_demo/)

**See:** [adk_agent_agentengine_demo/README.md](adk_agent_agentengine_demo/README.md) for detailed project-specific instructions.

## References

- [Google ADK Agent Engine Deployment](https://google.github.io/adk-docs/deploy/agent-engine/)
- [Vertex AI Agent Engine Documentation](https://docs.cloud.google.com/agent-builder/agent-engine/overview)
- [Agent Starter Pack Deployment Guide](https://googlecloudplatform.github.io/agent-starter-pack/guide/deployment.html)
- [Agent Starter Pack setup-cicd CLI](https://googlecloudplatform.github.io/agent-starter-pack/cli/setup_cicd.html)
- [Terraform Documentation](https://www.terraform.io/docs)

