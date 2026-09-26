import chromadb
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from backend.config import GOOGLE_API_KEY

CHROMA_PATH = "./chroma_db"
_client = None


def get_chroma_client():
    global _client
    if _client is None:
        _client = chromadb.PersistentClient(path=CHROMA_PATH)
    return _client


def retrieve_context(query: str, collection: str = "general", top_k: int = 3) -> str:
    """
    Retrieve the most relevant knowledge chunks for a given query.

    Args:
        query: User query or agent prompt
        collection: ChromaDB collection name (fitness | nutrition | general)
        top_k: Number of chunks to retrieve

    Returns:
        Concatenated relevant text chunks
    """
    try:
        client = get_chroma_client()
        embeddings = GoogleGenerativeAIEmbeddings(
            model="models/text-embedding-004",
            google_api_key=GOOGLE_API_KEY
        )
        col = client.get_or_create_collection(collection)

        # Check if collection has any documents
        if col.count() == 0:
            return ""

        query_embedding = embeddings.embed_query(query)
        results = col.query(
            query_embeddings=[query_embedding],
            n_results=min(top_k, col.count())
        )

        if results.get("documents") and results["documents"][0]:
            return "\n\n---\n\n".join(results["documents"][0])
        return ""
    except Exception:
        return ""
