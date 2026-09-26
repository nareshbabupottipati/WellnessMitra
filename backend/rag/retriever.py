"""Keyword search over local knowledge text. No vector database."""
import re
from pathlib import Path

DOCS = Path(__file__).parent / "knowledge_docs"
COLLECTION_FILES = {
    "fitness": ["fitness_exercises.txt"],
    "nutrition": ["nutrition_guidelines.txt"],
    "general": ["wellness_tips.txt", "fitness_exercises.txt", "nutrition_guidelines.txt"],
}


def _chunks(collection: str) -> list[str]:
    names = COLLECTION_FILES.get(collection, COLLECTION_FILES["general"])
    chunks = []
    for name in names:
        path = DOCS / name
        if not path.exists():
            continue
        parts = re.split(r"\n(?=### )", path.read_text(encoding="utf-8"))
        for part in parts:
            text = part.strip()
            if len(text) > 40:
                chunks.append(text)
    return chunks


def retrieve_context(query: str, collection: str = "general", top_k: int = 3) -> str:
    words = {word for word in re.findall(r"[a-z0-9]+", query.lower()) if len(word) > 2}
    scored = []
    for chunk in _chunks(collection):
        haystack = chunk.lower()
        score = sum(1 for word in words if word in haystack)
        if score:
            scored.append((score, chunk))
    scored.sort(key=lambda item: item[0], reverse=True)
    if not scored:
        picked = _chunks(collection)[:1]
    else:
        picked = [chunk for _, chunk in scored[:top_k]]
    clipped = [chunk[:350].strip() for chunk in picked]
    return "\n\n".join(clipped)
