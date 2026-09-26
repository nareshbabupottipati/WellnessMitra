import traceback
from backend.rag.ingestion import ingest_documents
try:
    ingest_documents()
except Exception:
    traceback.print_exc()
