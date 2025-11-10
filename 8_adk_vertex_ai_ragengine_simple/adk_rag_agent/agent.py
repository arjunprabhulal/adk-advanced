from google.adk.agents import Agent
from google.adk.tools.retrieval.vertex_ai_rag_retrieval import VertexAiRagRetrieval
from vertexai.preview import rag

# Configuration
# Replace with your RAG Corpus ID
# Format: projects/YOUR_PROJECT_ID/locations/YOUR_LOCATION/ragCorpora/YOUR_CORPUS_ID
RAG_CORPUS = "projects/YOUR_PROJECT_ID/locations/us-central1/ragCorpora/YOUR_CORPUS_ID"

root_agent = Agent(
    name="vertex_rag_agent",
    model="gemini-2.5-flash",
    instruction="Answer questions using Vertex AI RAG Engine to retrieve information from the knowledge base. Always cite sources when available.",
    description="RAG agent that retrieves information from Vertex AI RAG Engine corpus",
    tools=[
        VertexAiRagRetrieval(
            name="retrieve_rag_documentation",
            description="Use this tool to retrieve documentation and reference materials from the RAG corpus.",
            rag_resources=[
                rag.RagResource(
                    rag_corpus=RAG_CORPUS
                )
            ],
            similarity_top_k=10,
            vector_distance_threshold=0.6,
        )
    ]
)

