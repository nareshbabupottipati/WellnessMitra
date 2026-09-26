from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.config import CORS_ORIGINS
from backend.api.routes import user_routes, chat_routes, workout_routes, progress_routes, nutrition_routes

app = FastAPI(
    title="WellnessMitra API",
    description="AI-powered Fitness & Wellness Agent API (JSON File Storage)",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include route modules
app.include_router(user_routes.router)
app.include_router(chat_routes.router)
app.include_router(workout_routes.router)
app.include_router(progress_routes.router)
app.include_router(nutrition_routes.router)


@app.get("/", tags=["Health"])
def root():
    return {
        "app": "WellnessMitra",
        "status": "running",
        "version": "1.0.0",
        "storage": "JSON file store (data/*.json)",
        "docs": "/docs"
    }


@app.get("/health", tags=["Health"])
def health_check():
    return {
        "status": "healthy",
        "agents": "ready",
        "storage": "json_files"
    }
