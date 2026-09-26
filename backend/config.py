from dotenv import load_dotenv
import os

load_dotenv()

GOOGLE_API_KEY     = os.getenv("GOOGLE_API_KEY")
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")
EDAMAM_APP_ID      = os.getenv("EDAMAM_APP_ID")
EDAMAM_APP_KEY     = os.getenv("EDAMAM_APP_KEY")
DATABASE_URL       = os.getenv("DATABASE_URL", "sqlite:///./fitness_agent.db")
APP_ENV            = os.getenv("APP_ENV", "development")
CORS_ORIGINS       = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
