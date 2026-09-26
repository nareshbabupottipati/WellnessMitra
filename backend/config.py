from dotenv import load_dotenv
import os
from pathlib import Path
import google.generativeai as genai

load_dotenv()

BASE_DIR            = Path(__file__).resolve().parent.parent
DATA_DIR            = Path(os.getenv("DATA_DIR", str(BASE_DIR / "data")))

GOOGLE_API_KEY      = os.getenv("GOOGLE_API_KEY")
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")
APP_ENV             = os.getenv("APP_ENV", "development")
CORS_ORIGINS        = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
GEMINI_MODEL        = os.getenv("GEMINI_MODEL", "gemini-3.5-flash")

FALLBACK_MODELS     = ["gemini-3.5-flash", "gemini-3.7-flash", "gemini-3.5-flash-lite", "gemini-3.8-flash"]

if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)


def generate_content_safe(prompt: str, system_instruction: str = None) -> str:
    """
    Generate content with automatic fallback across available Gemini models
    if quota (429) or model deprecation (404) is encountered.
    """
    models_to_try = [GEMINI_MODEL] + [m for m in FALLBACK_MODELS if m != GEMINI_MODEL]
    last_err = None
    for model_name in models_to_try:
        try:
            if system_instruction:
                m = genai.GenerativeModel(model_name=model_name, system_instruction=system_instruction)
            else:
                m = genai.GenerativeModel(model_name=model_name)
            response = m.generate_content(prompt)
            if response and response.text:
                return response.text
        except Exception as e:
            last_err = e
            continue
    raise last_err or RuntimeError("Could not generate content from Gemini API.")
