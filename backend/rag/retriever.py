"""
WellnessMitra Knowledge Retriever
A fast, pure-Python document retriever for fitness, nutrition, and wellness knowledge.
Zero C++ binary extensions, zero native segfaults, 100% reliable local search.
"""
from pathlib import Path
import re

KNOWLEDGE_DIR = Path(__file__).resolve().parent / "knowledge_docs"

# Cache loaded chunks: {collection_name: [ {"title": ..., "text": ...}, ... ]}
_CHUNKS_CACHE = {}


def _load_chunks_for_file(filepath: Path) -> list:
    """Read a markdown/text file and split into semantic sections."""
    if not filepath.exists():
        return []

    try:
        content = filepath.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return []

    chunks = []
    # Split by markdown headers
    sections = re.split(r'\n(?=#{1,3}\s)', content)
    for section in sections:
        section = section.strip()
        if not section or section.startswith("# FITNESS EXERCISES") or section.startswith("# NUTRITION") or section.startswith("# WELLNESS"):
            continue
        lines = section.splitlines()
        title = lines[0].lstrip('#').strip()
        chunks.append({
            "title": title,
            "text": section
        })

    return chunks


def _get_collection_chunks(collection: str) -> list:
    """Get parsed document chunks for the requested collection."""
    global _CHUNKS_CACHE

    if collection in _CHUNKS_CACHE:
        return _CHUNKS_CACHE[collection]

    mapping = {
        "fitness": ["fitness_exercises.txt"],
        "nutrition": ["nutrition_guidelines.txt"],
        "wellness": ["wellness_tips.txt"],
        "general": ["fitness_exercises.txt", "nutrition_guidelines.txt", "wellness_tips.txt"]
    }

    target_files = mapping.get(collection, ["fitness_exercises.txt", "nutrition_guidelines.txt", "wellness_tips.txt"])
    chunks = []
    for fname in target_files:
        fpath = KNOWLEDGE_DIR / fname
        chunks.extend(_load_chunks_for_file(fpath))

    _CHUNKS_CACHE[collection] = chunks
    return chunks


def retrieve_context(query: str, collection: str = "general", top_k: int = 3) -> str:
    """
    Retrieve the most relevant knowledge chunks for a given query using semantic keyword matching.

    Args:
        query: User query or agent prompt
        collection: Collection name (fitness | nutrition | wellness | general)
        top_k: Maximum number of chunks to return

    Returns:
        Concatenated relevant text chunks
    """
    try:
        chunks = _get_collection_chunks(collection)
        if not chunks:
            return ""

        # Normalize query tokens (alphanumeric words, min len 3)
        query_words = set(re.findall(r'[a-zA-Z0-9]+', query.lower()))
        # Remove very common stop words
        stopwords = {
            "the", "and", "for", "with", "this", "that", "from", "you", "your",
            "can", "are", "week", "plan", "give", "help", "about", "what", "how"
        }
        keywords = {w for w in query_words if len(w) > 2 and w not in stopwords}

        scored = []
        for c in chunks:
            title_lower = c["title"].lower()
            text_lower = c["text"].lower()

            # Score by title matches (high weight) and body matches
            score = 0
            for kw in keywords:
                if kw in title_lower:
                    score += 5
                score += text_lower.count(kw)

            if score > 0:
                scored.append((score, c["text"]))

        # Sort descending by score
        scored.sort(key=lambda x: x[0], reverse=True)

        selected = [item[1] for item in scored[:top_k]]
        if not selected and chunks:
            # If no direct keyword match, return the first few chunks as general guidance
            selected = [c["text"] for c in chunks[:top_k]]

        return "\n\n---\n\n".join(selected)

    except Exception:
        return ""
