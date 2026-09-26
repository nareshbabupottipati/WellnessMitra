from dotenv import load_dotenv
import os
from pathlib import Path

load_dotenv()

BASE_DIR            = Path(__file__).resolve().parent.parent
DATA_DIR            = Path(os.getenv("DATA_DIR", str(BASE_DIR / "data")))

GOOGLE_API_KEY      = os.getenv("GOOGLE_API_KEY")
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")
APP_ENV             = os.getenv("APP_ENV", "development")
CORS_ORIGINS        = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
