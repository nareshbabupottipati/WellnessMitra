from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.config import CORS_ORIGINS
from backend.database.db import Base, engine
from backend.models import User, WorkoutLog, WeightLog, MealLog  # ensure models registered
from backend.api.routes import user_routes, chat_routes, workout_routes, progress_routes

# Create all database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="WellnessMitra API",
    description="AI-powered Fitness & Wellness Agent API",
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


@app.get("/", tags=["Health"])
def root():
    return {
        "app": "WellnessMitra",
        "status": "running",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "healthy", "agents": "ready"}
