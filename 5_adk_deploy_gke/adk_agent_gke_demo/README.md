# ADK GKE Demo - Capital Agent

A simple Google ADK agent running on Google Kubernetes Engine (GKE) that answers questions about world capitals.

## Agent Details

- **Google ADK Version**: `1.18.0`
- **Model**: `gemini-2.0-flash`
- **Capabilities**: Answers questions about world capitals
- **Deployment Target**: Google Kubernetes Engine (GKE)

> **Important**: 
> - **Installation** happens at the **parent directory level** (`5_adk_deploy_gke/`). See [parent README](../README.md) for installation instructions.
> - **Deployment and testing** happen in **this directory** (`adk_agent_gke_demo/`).

## Project Structure

```
adk_agent_gke_demo/
├── agent.py                    # Top-level agent loader (ADK discovery point)
├── capital_agent/
│   ├── __init__.py            # Package initialization
│   └── agent.py               # Agent definition with root_agent
├── main.py                    # FastAPI application entry point
├── requirements.txt           # Python dependencies (installed at parent level)
├── .env.example               # Example environment variables template
└── README.md                  # This file
```

## Prerequisites

- **Python**: 3.11 or later
- **gcloud CLI**: Google Cloud command-line tool
- **kubectl**: Kubernetes command-line tool
- **Active GCP Project** with billing enabled

## Setup Instructions

### 1. Configure Google Cloud Environment

Set your GCP project variables:

```bash
export GOOGLE_CLOUD_PROJECT="your-project-id"
export GOOGLE_CLOUD_LOCATION="us-central1"
export GOOGLE_GENAI_USE_VERTEXAI=True
export GOOGLE_CLOUD_PROJECT_NUMBER=$(gcloud projects describe --format json $GOOGLE_CLOUD_PROJECT | jq -r ".projectNumber")
```

### 2. Enable Required APIs

```bash
gcloud services enable \
    container.googleapis.com \
    artifactregistry.googleapis.com \
    cloudbuild.googleapis.com \
    aiplatform.googleapis.com
```

### 3. Grant IAM Permissions

Grant roles to the Compute Engine service account:

```bash
ROLES_TO_ASSIGN=(
    "roles/artifactregistry.writer"
    "roles/storage.objectViewer"
    "roles/logging.viewer"
    "roles/logging.logWriter"
)

for ROLE in "${ROLES_TO_ASSIGN[@]}"; do
    gcloud projects add-iam-policy-binding "${GOOGLE_CLOUD_PROJECT}" \
        --member="serviceAccount:${GOOGLE_CLOUD_PROJECT_NUMBER}-compute@developer.gserviceaccount.com" \
        --role="${ROLE}"
done
```

### 4. Create GKE Cluster

Create a GKE Autopilot cluster:

```bash
gcloud container clusters create-auto adk-cluster \
    --location=$GOOGLE_CLOUD_LOCATION \
    --project=$GOOGLE_CLOUD_PROJECT
```

Get cluster credentials:

```bash
gcloud container clusters get-credentials adk-cluster \
    --location=$GOOGLE_CLOUD_LOCATION \
    --project=$GOOGLE_CLOUD_PROJECT
```

### 5. Set Up Workload Identity for Vertex AI

Even with automated deployment, you need to configure Workload Identity so your agent can authenticate to Vertex AI.

**Create Google Service Account:**

```bash
export GSA_NAME=vertex-ai-gke-sa

gcloud iam service-accounts create $GSA_NAME \
    --project=$GOOGLE_CLOUD_PROJECT \
    --display-name="Service account for Vertex AI access from GKE" \
    || echo "Service account already exists"
```

**Grant Vertex AI Permissions:**

```bash
gcloud projects add-iam-policy-binding $GOOGLE_CLOUD_PROJECT \
    --member="serviceAccount:$GSA_NAME@$GOOGLE_CLOUD_PROJECT.iam.gserviceaccount.com" \
    --role=roles/aiplatform.user
```

**Create Kubernetes Service Account:**

```bash
export KSA_NAME=vertex-ai-sa
export NAMESPACE=default

kubectl create serviceaccount $KSA_NAME --namespace=$NAMESPACE || true
```

**Bind Kubernetes SA to Google SA (Workload Identity):**

```bash
gcloud iam service-accounts add-iam-policy-binding \
    $GSA_NAME@$GOOGLE_CLOUD_PROJECT.iam.gserviceaccount.com \
    --role=roles/iam.workloadIdentityUser \
    --member="serviceAccount:$GOOGLE_CLOUD_PROJECT.svc.id.goog[$NAMESPACE/$KSA_NAME]"

kubectl annotate serviceaccount $KSA_NAME \
    --namespace=$NAMESPACE \
    "iam.gke.io/gcp-service-account=$GSA_NAME@$GOOGLE_CLOUD_PROJECT.iam.gserviceaccount.com" \
    --overwrite
```

## Deployment

Deploy using the ADK CLI:

```bash
cd adk_agent_gke_demo

adk deploy gke \
    --project $GOOGLE_CLOUD_PROJECT \
    --cluster_name adk-cluster \
    --region $GOOGLE_CLOUD_LOCATION \
    --with_ui \
    --log_level info \
    .
```

> **Note**: The `adk deploy gke` command automatically handles containerization, image building, and Kubernetes deployment. However, you must configure Workload Identity (step 5) before deployment so your agent can authenticate to Vertex AI.

## Verify Deployment

Check pod status:

```bash
kubectl get pods -l app=adk-agent
```

**Important**: Ensure your pods are using the correct service account. If needed, patch the deployment to use the `vertex-ai-sa` service account:

```bash
kubectl patch deployment adk-default-service-name \
    -p '{"spec":{"template":{"spec":{"serviceAccountName":"vertex-ai-sa"}}}}'
```

Get the external IP:

```bash
kubectl get service
```

View logs:

```bash
kubectl logs -l app=adk-agent -f
```

## Testing Your Deployed Agent

### Access Web UI

If you deployed with `--with_ui`, get the external IP and access the web UI:

```bash
export APP_URL=$(kubectl get service adk-default-service-name -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
echo "Agent URL: http://$APP_URL"
```

Access the web UI at:
```
http://<EXTERNAL-IP>/dev-ui/
```

### Test via API

List available apps:

```bash
curl -X GET http://$APP_URL/list-apps
```

Run agent query:

```bash
curl -X POST http://$APP_URL/run_sse \
    -H "Content-Type: application/json" \
    -d '{
        "app_name": "capital_agent",
        "user_id": "user_123",
        "session_id": "session_abc",
        "new_message": {
            "role": "user",
            "parts": [{
                "text": "What is the capital of France?"
            }]
        },
        "streaming": false
    }'
```

## Local Development

For local testing, create a `.env` file from `.env.example`:

```bash
cp .env.example .env
```

Edit `.env` and set:
- `GOOGLE_GENAI_USE_VERTEXAI=False` for local testing with API key
- `GOOGLE_API_KEY="your-api-key"` (get from https://aistudio.google.com/apikey)

Then run:

```bash
adk run adk_agent_gke_demo
```

Or start the web server:

```bash
python main.py
```

## Clean Up

Delete the GKE cluster:

```bash
gcloud container clusters delete adk-cluster \
    --location=$GOOGLE_CLOUD_LOCATION \
    --project=$GOOGLE_CLOUD_PROJECT
```

Delete the Artifact Registry repository (if created):

```bash
gcloud artifacts repositories delete adk-repo \
    --location=$GOOGLE_CLOUD_LOCATION \
    --project=$GOOGLE_CLOUD_PROJECT
```

Delete the Google Service Account:

```bash
gcloud iam service-accounts delete $GSA_NAME@$GOOGLE_CLOUD_PROJECT.iam.gserviceaccount.com
```

## References

- [Google ADK GKE Deployment Guide](https://google.github.io/adk-docs/deploy/gke/)
- [ADK Documentation](https://google.github.io/adk-docs/)
