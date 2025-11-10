# ADK Cloud Run Deployment

This directory contains implementations for deploying Google ADK agents to Google Cloud Run.

## Which README Should I Read?

**Quick Navigation Guide:**

- **Start here** → This README (`4_adk_deploy_cloudrun/README.md`): 
  - Overview and workflow
  - Installation instructions (parent directory level)
  - Quick start guide for using existing implementation
  - Instructions for creating new projects

- **For detailed project info** → Child README (`adk_agent_cloudrun_demo/README.md`):
  - Project-specific details
  - Detailed deployment steps
  - Complete testing examples
  - Environment variable configuration

**Typical Workflow:**
1. Read this README for installation and overview
2. Navigate to `adk_agent_cloudrun_demo/` for deployment
3. Refer to child README for detailed project-specific instructions

## Table of Contents

- [Overview](#overview)
- [Quick Start: Using Existing Implementation](#quick-start-using-existing-implementation)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Deployment](#deployment)
  - [Testing](#testing)
- [Creating a New Project](#creating-a-new-project)
- [References](#references)

## Overview

Google Cloud Run is a fully managed serverless platform that automatically scales your applications. These implementations demonstrate how to containerize and deploy Google ADK agents to Cloud Run using **Agent Starter Pack (ASP)**.

---

## Quick Start: Using Existing Implementation

**If you want to use the existing `adk_agent_cloudrun_demo` implementation**, follow these steps:

### Prerequisites

- Python 3.11 or later
- `uv` or `pip` package manager
- Google Cloud Project with billing enabled
- Required APIs enabled (Cloud Run, Cloud Build, Container Registry)
- Docker installed (for local testing)
- Google Cloud SDK installed and authenticated
- Terraform installed (for infrastructure deployment)
- Appropriate IAM permissions

### Installation

**Install dependencies at the parent directory level** (`4_adk_deploy_cloudrun/`):

**Using uv (recommended):**
```bash
# Navigate to parent directory
cd 4_adk_deploy_cloudrun

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
cd 4_adk_deploy_cloudrun

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
cd adk_agent_cloudrun_demo

# Set up environment variables (create .env from .env.example)
cp .env.example .env
# Edit .env with your configuration

# Set your GCP project
gcloud config set project YOUR_DEV_PROJECT_ID

# Option A: Quick development deployment
make setup-dev-env  # Provision GCP resources
make deploy         # Deploy to Cloud Run

# Option B: Production CI/CD pipeline (recommended)
uvx agent-starter-pack setup-cicd
```

> **Note**: For detailed deployment instructions, see [adk_agent_cloudrun_demo/README.md](adk_agent_cloudrun_demo/README.md)

### Testing

After successful deployment, test your agent:

```bash
# From the adk_agent_cloudrun_demo directory
jupyter notebook notebooks/adk_app_testing.ipynb
```

**Testing Methods:**

1. **Jupyter Notebook** (Recommended): The `notebooks/adk_app_testing.ipynb` notebook provides comprehensive testing capabilities:
   - Tests the deployed Cloud Run service
   - Validates API endpoints
   - Tests with streaming queries
   - Includes error handling examples

2. **Cloud Run Console**: Access your service via the Cloud Run console link for monitoring and logs

3. **Local Proxy Testing** (For Authenticated Services): Use `gcloud run services proxy` to create a local proxy that handles authentication automatically

4. **Direct API Testing**: Use curl or Postman to test the deployed service endpoints (for public services)

5. **Local Testing**: Use `make playground` or `make local-backend` to test your agent locally before deployment

---

## Creating a New Project

**If you want to create a NEW agent project**, use the Agent Starter Pack CLI tool:

```bash
# Using uvx (recommended)
uvx agent-starter-pack create my-cloudrun-agent -a adk_base -d cloud_run

# Or using pip
pip install --upgrade agent-starter-pack
agent-starter-pack create my-cloudrun-agent -a adk_base -d cloud_run
```

The CLI will guide you through:
- Agent template selection
- Deployment target (Cloud Run)
- CI/CD runner selection (Cloud Build or GitHub Actions)
- GCP project configuration

For more details, see the [Agent Starter Pack Documentation](https://googlecloudplatform.github.io/agent-starter-pack/).

## Implementations

### adk_agent_cloudrun_demo

Complete implementation demonstrating deployment of a Google ADK agent to Google Cloud Run using **Agent Starter Pack (ASP)**.

**Key Features:**
- Docker containerization
- Cloud Run deployment
- Terraform infrastructure setup
- Automated CI/CD workflows
- Testing and evaluation notebooks

**Directory:** [adk_agent_cloudrun_demo/](adk_agent_cloudrun_demo/)

**See:** [adk_agent_cloudrun_demo/README.md](adk_agent_cloudrun_demo/README.md) for detailed project-specific instructions.

## References

- [Google ADK Cloud Run Deployment](https://google.github.io/adk-docs/deploy/cloud-run/)
- [Google Cloud Run Documentation](https://cloud.google.com/run/docs)
- [Agent Starter Pack Deployment Guide](https://googlecloudplatform.github.io/agent-starter-pack/guide/deployment.html)
- [Agent Starter Pack setup-cicd CLI](https://googlecloudplatform.github.io/agent-starter-pack/cli/setup_cicd.html)
- [Docker Documentation](https://docs.docker.com/)

