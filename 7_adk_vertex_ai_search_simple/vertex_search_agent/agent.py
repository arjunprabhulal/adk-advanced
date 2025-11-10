from google.adk.agents import Agent
from google.adk.tools import VertexAiSearchTool

# Configuration
DATASTORE_ID = "projects/YOUR_PROJECT_ID/locations/global/collections/default_collection/dataStores/YOUR_DATASTORE_ID"

root_agent = Agent(
    name="vertex_search_agent",
    model="gemini-2.5-flash",
    instruction="Answer questions using Vertex AI Search to find information from internal documents. Always cite sources when available.",
    tools=[VertexAiSearchTool(data_store_id=DATASTORE_ID)]
)
