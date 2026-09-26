"""Knowledge files are read directly. Nothing to ingest for the JSON POC."""


def ingest_documents():
    from pathlib import Path
    docs = Path(__file__).parent / "knowledge_docs"
    files = sorted(docs.glob("*.txt"))
    print(f"Keyword search will read {len(files)} knowledge files from {docs}")
    for path in files:
        print(f"  - {path.name}")


if __name__ == "__main__":
    ingest_documents()
