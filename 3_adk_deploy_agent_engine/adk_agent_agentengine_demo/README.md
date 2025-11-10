# adk_agent_agentengine_demo

A base ReAct agent built with Google's Agent Development Kit (ADK)
Agent generated with [`googleCloudPlatform/agent-starter-pack`](https://github.com/GoogleCloudPlatform/agent-starter-pack) version `0.19.2`

## Agent Details

- **Google ADK Version**: `1.18.0`
- **Model**: `gemini-2.5-flash`
- **Deployment Target**: Vertex AI Agent Engine

> **Important**: 
> - **Installation** happens at the **parent directory level** (`3_adk_deploy_agent_engine/`). See [parent README](../README.md) for installation instructions.
> - **Deployment and testing** happen in **this directory** (`adk_agent_agentengine_demo/`).
> - For local testing, create a `.env` file from `.env.example` in this directory.

## Project Structure

This project is organized as follows:

```
adk_agent_agentengine_demo/
├── app/                 # Core application code
│   ├── agent.py         # Main agent logic
│   ├── agent_engine_app.py # Agent Engine application logic
│   └── utils/           # Utility functions and helpers
├── .cloudbuild/         # CI/CD pipeline configurations for Google Cloud Build
├── deployment/          # Infrastructure and deployment scripts
├── notebooks/           # Jupyter notebooks for prototyping and evaluation
├── tests/               # Unit, integration, and load tests
├── Makefile             # Makefile for common commands
├── GEMINI.md            # AI-assisted development guide
├── .env.example         # Example environment variables template
├── .env                 # Environment variables (create from .env.example)
├── deployment_metadata.json # Deployment metadata (created/updated after successful deployment)
└── pyproject.toml       # Project dependencies and configuration
```

## Requirements

Before you begin, ensure you have:
- **Python**: 3.11 or later
- **uv** or **pip**: Package manager (see parent directory README for installation instructions)
- **Google Cloud SDK**: For GCP services - [Install](https://cloud.google.com/sdk/docs/install)
- **Terraform**: For infrastructure deployment - [Install](https://developer.hashicorp.com/terraform/downloads)
- **make**: Build automation tool - [Install](https://www.gnu.org/software/make/) (pre-installed on most Unix-based systems)

## Setup

### 1. Environment Variables

Create a `.env` file from the example:

```bash
cp .env.example .env
```

**For Local Development:**
- Set `GOOGLE_GENAI_USE_VERTEXAI=False` and provide `GOOGLE_API_KEY` from [Google AI Studio](https://aistudio.google.com/apikey)
- This uses the Gemini Developer API for rapid prototyping

**For Deployment to Agent Engine (Recommended):**
- Set `GOOGLE_GENAI_USE_VERTEXAI=True` with `GOOGLE_CLOUD_PROJECT` and `GOOGLE_CLOUD_LOCATION`
- Uses Application Default Credentials (ADC) - no API key needed
- Provides access to Vertex AI enterprise features, managed sessions, grounding, and Cloud Trace

**Environment Variables:**
- `GOOGLE_GENAI_USE_VERTEXAI`: `True` for Vertex AI (deployment) or `False` for Gemini Developer API (local dev)
- `GOOGLE_API_KEY`: Required when `GOOGLE_GENAI_USE_VERTEXAI=False` (local development)
- `GOOGLE_CLOUD_PROJECT`: Required when `GOOGLE_GENAI_USE_VERTEXAI=True` (deployment)
- `GOOGLE_CLOUD_LOCATION`: Required when `GOOGLE_GENAI_USE_VERTEXAI=True` (deployment)


## Quick Start (Local Testing)

> **Note**: Dependencies are installed at the parent directory level. Navigate to `3_adk_deploy_agent_engine` and follow the installation instructions in the parent README first.

**Environment Variables Location:**

The `.env` file should be created in the **project root directory** (`adk_agent_agentengine_demo/`), at the same level as `app/`, `Makefile`, and `pyproject.toml`. 

ADK tools (`adk run`, `adk web`, `make playground`) automatically load `.env` files when run from the project root or agent directory. No explicit `load_dotenv()` call is needed in the code.

Install required packages and launch the local development environment:

```bash
make install && make playground
```

## Commands

| Command              | Description                                                                                 |
| -------------------- | ------------------------------------------------------------------------------------------- |
| `make install`       | Install all required dependencies using uv                                                  |
| `make playground`    | Launch Streamlit interface for testing agent locally and remotely |
| `make deploy`        | Deploy agent to Agent Engine |
| `make register-gemini-enterprise` | Register deployed agent to Gemini Enterprise ([docs](https://googlecloudplatform.github.io/agent-starter-pack/cli/register_gemini_enterprise.html)) |
| `make test`          | Run unit and integration tests                                                              |
| `make lint`          | Run code quality checks (codespell, ruff, mypy)                                             |
| `make setup-dev-env` | Set up development environment resources using Terraform                         |

For full command options and usage, refer to the [Makefile](Makefile).


## Usage

This template follows a "bring your own agent" approach - you focus on your business logic, and the template handles everything else (UI, infrastructure, deployment, monitoring).

1. **Prototype:** Build your Generative AI Agent using the intro notebooks in `notebooks/` for guidance. Use Vertex AI Evaluation to assess performance.
2. **Integrate:** Import your agent into the app by editing `app/agent.py`.
3. **Test:** Explore your agent functionality using the Streamlit playground with `make playground`. The playground offers features like chat history, user feedback, and various input types, and automatically reloads your agent on code changes.
4. **Deploy:** Set up and initiate the CI/CD pipelines, customizing tests as necessary. Refer to the [deployment section](#deployment) for comprehensive instructions. For streamlined infrastructure deployment, simply run `uvx agent-starter-pack setup-cicd`. Check out the [`agent-starter-pack setup-cicd` CLI command](https://googlecloudplatform.github.io/agent-starter-pack/cli/setup_cicd.html). Currently supports GitHub with both Google Cloud Build and GitHub Actions as CI/CD runners.
5. **Monitor:** Track performance and gather insights using Cloud Logging, Tracing, and the Looker Studio dashboard to iterate on your application.

The project includes a `GEMINI.md` file that provides context for AI tools like Gemini CLI when asking questions about your template.


## Deployment

This starter pack uses a robust, production-ready deployment strategy that combines **Terraform** for infrastructure as code and a **CI/CD pipeline** for automated builds, tests, and deployments.

### Development Environment Deployment

For a standalone development environment without the full CI/CD pipeline:

```bash
# Set your GCP project
gcloud config set project <your-dev-project-id>

# Provision GCP resources for dev environment
make setup-dev-env

# Deploy the application to Agent Engine
make deploy
```

The `make setup-dev-env` command runs the Terraform configuration in `deployment/terraform/dev` to provision a development environment.

> **Note**: After successful deployment, the `deployment_metadata.json` file is automatically updated with your Agent Engine ID. Use the provided Jupyter notebook (`notebooks/adk_app_testing.ipynb`) to validate and test your deployed agent programmatically.

### Automated CI/CD Deployment (Recommended)

For a streamlined, one-command deployment of the entire CI/CD pipeline and infrastructure:

```bash
# From the project root directory
uvx agent-starter-pack setup-cicd
```

This command handles:
- **Infrastructure Provisioning**: Uses Terraform to create and configure resources in staging and production Google Cloud projects
- **CI/CD Configuration**: Sets up a complete CI/CD pipeline with your chosen runner (Google Cloud Build or GitHub Actions)
- **Repository Connection**: Connects your GitHub repository to the CI/CD provider

**Deployment Workflow:**
1. **CI Pipeline**: Triggered on pull requests - runs unit and integration tests
2. **Staging CD Pipeline**: Triggered on merge to `main` - builds container, deploys to staging, performs load testing
3. **Production Deployment**: Requires manual approval - deploys tested container to production

For complete deployment details and configuration options, see the [Agent Starter Pack Deployment Guide](https://googlecloudplatform.github.io/agent-starter-pack/guide/deployment.html) and [setup-cicd CLI Reference](https://googlecloudplatform.github.io/agent-starter-pack/cli/setup_cicd.html).

## Testing Your Deployed Agent

After successful deployment, the `deployment_metadata.json` file in the project root is automatically updated with your Agent Engine deployment information:

```json
{
  "remote_agent_engine_id": "projects/YOUR_PROJECT/locations/us-central1/reasoningEngines/YOUR_ENGINE_ID",
  "deployment_timestamp": "2025-11-03T23:23:40.408958"
}
```

### Testing Methods

**1. Using Jupyter Notebook (Recommended)**

The project includes a comprehensive testing notebook:

```bash
# Launch Jupyter Notebook
jupyter notebook notebooks/adk_app_testing.ipynb
```

The notebook demonstrates:
- Loading the deployed agent using the Agent Engine ID from `deployment_metadata.json`
- Testing with streaming queries
- Comparing local vs. remote agent behavior
- Error handling and debugging

**2. Google Cloud Console**

After deployment, you'll receive a console link to access your agent directly in the Vertex AI Agent Engine interface. This provides:
- Interactive chat interface
- Session management
- Monitoring and logs
- Performance metrics

**3. Programmatic Testing**

You can test your deployed agent programmatically using the Python client:

```python
from google.cloud import aiplatform
from app.agent_engine_app import AgentEngineApp
import json

# Load deployment metadata
with open('deployment_metadata.json', 'r') as f:
    metadata = json.load(f)

# Initialize the remote agent
remote_agent = aiplatform.ReasoningEngine(
    reasoning_engine_name=metadata['remote_agent_engine_id']
)

# Query the agent
response = remote_agent.query(
    query="Hello, how can you help me?",
    user_id="test_user"
)

print(response)
```

**4. Local Testing (Before Deployment)**

For local testing before deployment, use the Streamlit playground:

```bash
make playground
```

This launches a local web UI where you can interact with your agent, test functionality, and debug issues before deploying to production.

## Monitoring and Observability
> You can use [this Looker Studio dashboard](https://lookerstudio.google.com/reporting/46b35167-b38b-4e44-bd37-701ef4307418/page/tEnnC
) template for visualizing events being logged in BigQuery. See the "Setup Instructions" tab to getting started.

The application uses OpenTelemetry for comprehensive observability with all events being sent to Google Cloud Trace and Logging for monitoring and to BigQuery for long term storage.
