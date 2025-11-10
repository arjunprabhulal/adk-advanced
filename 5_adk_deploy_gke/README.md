# ADK GKE Deployment

This directory contains implementations for deploying Google ADK agents to Google Kubernetes Engine (GKE).

## Which README Should I Read?

**Quick Navigation Guide:**

- **Start here** → This README (`5_adk_deploy_gke/README.md`): 
  - Overview and workflow
  - Installation instructions (parent directory level)
  - Quick start guide for using existing implementation

- **For detailed project info** → Child README (`adk_agent_gke_demo/README.md`):
  - Project-specific details
  - Complete GKE setup and Workload Identity configuration
  - Detailed deployment steps
  - Testing and troubleshooting

**Typical Workflow:**
1. Read this README for installation and overview
2. Navigate to `adk_agent_gke_demo/` for deployment
3. Refer to child README for detailed setup, Workload Identity configuration, and deployment instructions

## Table of Contents

- [Overview](#overview)
- [Quick Start: Using Existing Implementation](#quick-start-using-existing-implementation)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Deployment](#deployment)
  - [Testing](#testing)
- [References](#references)

## Overview

Google Kubernetes Engine (GKE) provides a managed Kubernetes environment for deploying containerized applications. These implementations demonstrate how to deploy Google ADK agents to GKE with proper configuration, Workload Identity, service accounts, and networking.

---

## Quick Start: Using Existing Implementation

**If you want to use the existing `adk_agent_gke_demo` implementation**, follow these steps:

### Prerequisites

- Python 3.11 or later
- `uv` or `pip` package manager
- Google Cloud Project with billing enabled
- Required APIs enabled (GKE, Cloud Build, Artifact Registry, Vertex AI)
- `kubectl` installed and configured
- `gcloud` CLI installed and authenticated
- Docker installed (for building container images)
- Appropriate IAM permissions (Project Editor or Owner recommended for initial setup)

### Installation

**Install dependencies at the parent directory level** (`5_adk_deploy_gke/`):

**Using uv (recommended):**
```bash
# Navigate to parent directory
cd 5_adk_deploy_gke

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
cd 5_adk_deploy_gke

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
cd adk_agent_gke_demo

# Set up environment variables (create .env from .env.example)
cp .env.example .env
# Edit .env with your configuration

# Set your GCP project variables
export PROJECT_ID=your-project-id
export GOOGLE_CLOUD_REGION=us-central1
export CLUSTER_NAME=adk-cluster

# Authenticate with Google Cloud
gcloud auth login
gcloud config set project $PROJECT_ID

# Follow the detailed setup in the child README for:
# 1. Enabling APIs
# 2. Creating GKE cluster with Workload Identity
# 3. Configuring service accounts and IAM bindings
# 4. Deploying using adk deploy gke
```

> **Note**: GKE deployment requires extensive setup including Workload Identity configuration. See [adk_agent_gke_demo/README.md](adk_agent_gke_demo/README.md) for complete step-by-step instructions.

### Testing

After successful deployment, test your agent:

**1. Check Deployment Status:**
```bash
# Check pod status
kubectl get pods -l app=adk-agent

# Get external IP
kubectl get service
```

**2. Access the Agent:**
- Web UI: Open the external IP in your browser: `http://<EXTERNAL-IP>`
- API: Use the REST API endpoints (see child README for examples)

**3. View Logs:**
```bash
kubectl logs -l app=adk-agent -f
```

> **Note**: For detailed testing examples and troubleshooting, see [adk_agent_gke_demo/README.md](adk_agent_gke_demo/README.md)

---

## Implementations

### adk_agent_gke_demo

Complete implementation demonstrating deployment of a Google ADK agent to Google Kubernetes Engine with Workload Identity configuration.

**Key Features:**
- Kubernetes deployment using `adk deploy gke` command
- Workload Identity configuration for secure GCP authentication
- Container image building and pushing to Artifact Registry
- Load balancer setup for external access
- Service account and IAM bindings
- FastAPI server for REST API and web UI

**Directory:** [adk_agent_gke_demo/](adk_agent_gke_demo/)

**See:** [adk_agent_gke_demo/README.md](adk_agent_gke_demo/README.md) for detailed project-specific instructions.

## Key Concepts

- **Workload Identity**: Allows Kubernetes service accounts to authenticate to Google Cloud services using IAM roles
- **Container Images**: Built and stored in Artifact Registry
- **Kubernetes Manifests**: Deployment and Service configurations generated by `adk deploy gke`
- **Load Balancer**: External IP for accessing the agent

## References

- [Google ADK GKE Deployment](https://google.github.io/adk-docs/deploy/gke/)
- [Google Kubernetes Engine Documentation](https://cloud.google.com/kubernetes-engine/docs)
- [Workload Identity](https://cloud.google.com/kubernetes-engine/docs/how-to/workload-identity)

