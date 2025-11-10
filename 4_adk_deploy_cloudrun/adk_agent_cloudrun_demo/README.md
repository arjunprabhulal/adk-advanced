# adk_agent_cloudrun_demo

A base ReAct agent built with Google's Agent Development Kit (ADK)
Agent generated with [`googleCloudPlatform/agent-starter-pack`](https://github.com/GoogleCloudPlatform/agent-starter-pack) version `0.19.2`

## Agent Details

- **Google ADK Version**: `1.18.0`
- **Model**: `gemini-2.5-flash`
- **Deployment Target**: Google Cloud Run

> **Important**: 
> - **Installation** happens at the **parent directory level** (`4_adk_deploy_cloudrun/`). See [parent README](../README.md) for installation instructions.
> - **Deployment and testing** happen in **this directory** (`adk_agent_cloudrun_demo/`).
> - For local testing, create a `.env` file from `.env.example` in this directory.

## Project Structure

This project is organized as follows:

```
adk_agent_cloudrun_demo/
├── app/                 # Core application code
│   ├── agent.py         # Main agent logic
│   ├── server.py        # FastAPI Backend server
│   └── utils/           # Utility functions and helpers
├── .cloudbuild/         # CI/CD pipeline configurations for Google Cloud Build
├── deployment/          # Infrastructure and deployment scripts
├── notebooks/           # Jupyter notebooks for prototyping and evaluation
├── tests/               # Unit, integration, and load tests
├── Makefile             # Makefile for common commands
├── GEMINI.md            # AI-assisted development guide
├── .env.example         # Example environment variables template
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

> **Important**: The `.env` file is **only needed for local development/testing**. For Cloud Run deployment, environment variables are configured through Cloud Run's environment variable settings (via Terraform or `gcloud` commands), not through `.env` files.

**Create a `.env` file from the example for local development:**

```bash
cp .env.example .env
```

**For Local Development (Uncomment and set values in `.env`):**

Edit `.env` and uncomment the appropriate section:

```bash
# Option 1: Local testing with AI Studio (Gemini Developer API)
GOOGLE_GENAI_USE_VERTEXAI=False
GOOGLE_API_KEY="your-api-key"  # Get from https://aistudio.google.com/apikey
```

OR

```bash
# Option 2: Local testing with Vertex AI (uses gcloud authentication)
GOOGLE_GENAI_USE_VERTEXAI=True
GOOGLE_CLOUD_PROJECT="your-project-id"
GOOGLE_CLOUD_LOCATION="us-central1"
```

**For Deployment to Cloud Run:**

The `.env` file is **NOT used** during deployment. Environment variables are set through:
- **Terraform configuration** (in `deployment/terraform/`)
- **Cloud Run service configuration** (via `gcloud` commands or Cloud Console)
- **Application Default Credentials (ADC)** - automatically used when running on Cloud Run

**Environment Variables Reference:**
- `GOOGLE_GENAI_USE_VERTEXAI`: `True` for Vertex AI or `False` for Gemini Developer API
- `GOOGLE_API_KEY`: Required when `GOOGLE_GENAI_USE_VERTEXAI=False` (local development only)
- `GOOGLE_CLOUD_PROJECT`: Required when `GOOGLE_GENAI_USE_VERTEXAI=True`
- `GOOGLE_CLOUD_LOCATION`: Required when `GOOGLE_GENAI_USE_VERTEXAI=True`


## Quick Start (Local Testing)

> **Note**: Dependencies are installed at the parent directory level. Navigate to `4_adk_deploy_cloudrun` and follow the installation instructions in the parent README first.

Install required packages and launch the local development environment:

```bash
make install && make playground
```

## Commands

| Command              | Description                                                                                 |
| -------------------- | ------------------------------------------------------------------------------------------- |
| `make install`       | Install all required dependencies using uv                                                  |
| `make playground`    | Launch local development environment with backend and frontend - leveraging `adk web` command.|
| `make deploy`        | Deploy agent to Cloud Run (use `IAP=true` to enable Identity-Aware Proxy, `PORT=8080` to specify container port). By default, deploys with `--no-allow-unauthenticated` requiring authentication. |
| `make local-backend` | Launch local development server with hot-reload |
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

# Deploy the application to Cloud Run
make deploy
```

The `make setup-dev-env` command runs the Terraform configuration in `deployment/terraform/dev` to provision a development environment.

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

After successful deployment, test your Cloud Run service:

**1. Using Jupyter Notebook (Recommended)**

The project includes a comprehensive testing notebook:

```bash
# Launch Jupyter Notebook
jupyter notebook notebooks/adk_app_testing.ipynb
```

The notebook demonstrates:
- Testing the deployed Cloud Run service endpoints
- Validating API responses
- Testing with streaming queries
- Error handling and debugging

**2. Cloud Run Console**

Access your service via the Cloud Run console:
- View service URL and endpoints
- Monitor logs and metrics
- Check service health and performance

**3. Local Proxy Testing (For Authenticated Services)**

If your Cloud Run service is deployed with `--no-allow-unauthenticated` (requires authentication), you can use `gcloud` to create a local proxy:

```bash
# Create a local proxy to your Cloud Run service
gcloud run services proxy adk-agent-cloudrun-demo \
  --region us-central1 \
  --project YOUR_PROJECT_ID
```

This will:
- Create a local proxy at `http://127.0.0.1:8080`
- Automatically handle authentication using your `gcloud` credentials
- Proxy requests to your Cloud Run service

**Test the proxied service:**

```bash
# In another terminal, test the local proxy
curl -X POST http://127.0.0.1:8080/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Hello, how can you help me?", "user_id": "test_user"}'
```

**4. Direct API Testing (For Public Services)**

If your service allows unauthenticated access, test directly:

```bash
# Get your service URL from Cloud Run console
curl -X POST https://YOUR-SERVICE-URL.run.app/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Hello, how can you help me?", "user_id": "test_user"}'
```

> **Note**: For authenticated services, use the local proxy method above. For public services, you can test directly using the service URL.

**5. Local Testing (Before Deployment)**

For local testing before deployment, use:

```bash
# Streamlit playground
make playground

# Or local backend server
make local-backend
```


## Monitoring and Observability
> You can use [this Looker Studio dashboard](https://lookerstudio.google.com/reporting/46b35167-b38b-4e44-bd37-701ef4307418/page/tEnnC
) template for visualizing events being logged in BigQuery. See the "Setup Instructions" tab to getting started.

The application uses OpenTelemetry for comprehensive observability with all events being sent to Google Cloud Trace and Logging for monitoring and to BigQuery for long term storage.
