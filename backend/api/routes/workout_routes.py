from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
from backend.database.db import get_db
from backend.database.crud import get_user, log_workout, get_workout_logs
import datetime

router = APIRouter(prefix="/workouts", tags=["Workouts"])


class ExerciseItem(BaseModel):
    name:      str
    sets:      int
    reps:      str
    weight_kg: Optional[float] = None


class WorkoutLogRequest(BaseModel):
    user_id:        str
    exercises:      List[ExerciseItem]
    duration_mins:  int
    calories_burned: float
    intensity:      Optional[str] = "medium"
    notes:          Optional[str] = ""


@router.post("/log")
def log_workout_entry(req: WorkoutLogRequest, db: Session = Depends(get_db)):
    """Log a completed workout session."""
    user = get_user(db, req.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    data = {
        "user_id":         req.user_id,
        "date":            datetime.date.today(),
        "exercises":       [e.model_dump() for e in req.exercises],
        "duration_mins":   req.duration_mins,
        "calories_burned": req.calories_burned,
        "intensity":       req.intensity,
        "notes":           req.notes
    }
    entry = log_workout(db, data)
    return {"status": "logged", "id": entry.id, "date": str(entry.date)}


@router.get("/{user_id}/logs")
def get_logs(user_id: str, days: int = 30, db: Session = Depends(get_db)):
    """Get workout history for the last N days."""
    user = get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    logs = get_workout_logs(db, user_id, days)
    return {
        "user_id": user_id,
        "days":    days,
        "total":   len(logs),
        "logs":    [
            {
                "id":              l.id,
                "date":            str(l.date),
                "exercises":       l.exercises,
                "duration_mins":   l.duration_mins,
                "calories_burned": l.calories_burned,
                "intensity":       l.intensity
            } for l in logs
        ]
    }
