from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional

from backend.store import get_user, get_workout_logs, log_workout

router = APIRouter(prefix="/workouts", tags=["Workouts"])


class ExerciseItem(BaseModel):
    name: str
    sets: int
    reps: str
    weight_kg: Optional[float] = None


class WorkoutLogRequest(BaseModel):
    user_id: str
    exercises: List[ExerciseItem]
    duration_mins: int
    calories_burned: float
    intensity: Optional[str] = "medium"
    notes: Optional[str] = ""


@router.post("/log")
def log_workout_entry(req: WorkoutLogRequest):
    if not get_user(req.user_id):
        raise HTTPException(status_code=404, detail="User not found")
    entry = log_workout({
        "user_id": req.user_id,
        "exercises": [exercise.model_dump() for exercise in req.exercises],
        "duration_mins": req.duration_mins,
        "calories_burned": req.calories_burned,
        "intensity": req.intensity,
        "notes": req.notes,
    })
    return {"status": "logged", "id": entry.id, "date": entry.date}


@router.get("/{user_id}/logs")
def get_logs(user_id: str, days: int = 30):
    if not get_user(user_id):
        raise HTTPException(status_code=404, detail="User not found")
    logs = get_workout_logs(user_id, days)
    return {
        "user_id": user_id,
        "days": days,
        "total": len(logs),
        "logs": [
            {
                "id": log.id,
                "date": log.date,
                "exercises": log.exercises,
                "duration_mins": log.duration_mins,
                "calories_burned": log.calories_burned,
                "intensity": log.intensity,
            }
            for log in logs
        ],
    }
