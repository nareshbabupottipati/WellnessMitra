import sys
import chromadb
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pathlib import Path
from backend.config import GOOGLE_API_KEY

CHROMA_PATH = "./chroma_db"

COLLECTION_MAP = {
    "fitness_exercises":   "fitness",
    "workout_programs":    "fitness",
    "nutrition_guidelines":"nutrition",
    "dietary_plans":       "nutrition",
    "wellness_tips":       "general",
    "injury_prevention":   "general",
}


def ingest_documents():
    """Load knowledge docs, chunk, embed, and store in ChromaDB."""
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001",
        google_api_key=GOOGLE_API_KEY
    )
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)

    docs_path = Path(__file__).parent / "knowledge_docs"
    if not docs_path.exists():
        print(f"[WARN] Knowledge docs directory not found: {docs_path}")
        return

    for doc_file in docs_path.glob("*.txt"):
        stem = doc_file.stem
        collection_name = COLLECTION_MAP.get(stem, "general")
        collection = client.get_or_create_collection(collection_name)

        text = doc_file.read_text(encoding="utf-8")
        chunks = splitter.split_text(text)

        for i, chunk in enumerate(chunks):
            try:
                embedding = embeddings.embed_query(chunk)
                collection.upsert(
                    ids=[f"{stem}_{i}"],
                    documents=[chunk],
                    embeddings=[embedding]
                )
            except Exception as err:
                print(f"[ERROR] Embedding chunk {i} of {doc_file.name}: {err}")

        print(f"[OK] Ingested {len(chunks)} chunks from '{doc_file.name}' into '{collection_name}'")

    print("\n[DONE] RAG knowledge ingestion complete!")


if __name__ == "__main__":
    ingest_documents()
