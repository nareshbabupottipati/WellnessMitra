from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api.routes import chat_routes, progress_routes, user_routes, workout_routes
from backend.config import CORS_ORIGINS, gemini_configured

app = FastAPI(
    title="WellnessMitra API",
    description="JSON-backed fitness POC",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_routes.router)
app.include_router(chat_routes.router)
app.include_router(workout_routes.router)
app.include_router(progress_routes.router)


@app.get("/", tags=["Health"])
def root():
    return {
        "app": "WellnessMitra",
        "status": "running",
        "storage": "json",
        "version": "1.0.0",
        "docs": "/docs",
    }


@app.get("/health", tags=["Health"])
def health_check():
    return {
        "status": "healthy",
        "storage": "json",
        "gemini_configured": gemini_configured(),
        "maps": "openstreetmap",
    }
