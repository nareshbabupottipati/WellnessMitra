"""Gemini helper. Returns None when no API key is configured."""
import google.generativeai as genai

from backend.config import GEMINI_MODEL, GOOGLE_API_KEY, gemini_configured

_ready = False


def generate_text(prompt: str, system: str | None = None) -> str | None:
    global _ready
    if not gemini_configured():
        return None
    if not _ready:
        genai.configure(api_key=GOOGLE_API_KEY)
        _ready = True
    kwargs = {"model_name": GEMINI_MODEL}
    if system:
        kwargs["system_instruction"] = system
    model = genai.GenerativeModel(**kwargs)
    response = model.generate_content(
        prompt,
        generation_config={
            "max_output_tokens": 280,
            "temperature": 0.4,
        },
        request_options={"timeout": 12, "retry": None},
    )
    return (response.text or "").strip() or None
