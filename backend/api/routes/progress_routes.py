from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from backend.database.db import get_db
from backend.database.crud import get_user, log_weight, get_weight_logs, get_workout_logs
import datetime

router = APIRouter(prefix="/progress", tags=["Progress"])


class WeightLogRequest(BaseModel):
    user_id:   str
    weight_kg: float


@router.post("/weight")
def add_weight_log(req: WeightLogRequest, db: Session = Depends(get_db)):
    """Log a new body weight measurement."""
    user = get_user(db, req.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    entry = log_weight(db, req.user_id, req.weight_kg, user.height_cm)
    return {
        "status":    "logged",
        "date":      str(entry.date),
        "weight_kg": entry.weight_kg,
        "bmi":       entry.bmi
    }


@router.get("/{user_id}/summary")
def get_progress_summary(user_id: str, days: int = 30, db: Session = Depends(get_db)):
    """Get a 30-day progress summary."""
    user = get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    workout_logs = get_workout_logs(db, user_id, days)
    weight_logs  = get_weight_logs(db, user_id, days)

    total_workouts    = len(workout_logs)
    total_calories    = sum(l.calories_burned for l in workout_logs if l.calories_burned)
    weight_start      = weight_logs[0].weight_kg  if weight_logs else user.weight_kg
    weight_current    = weight_logs[-1].weight_kg if weight_logs else user.weight_kg
    weight_change     = round(weight_current - weight_start, 2)

    height_m = (user.height_cm or 170) / 100
    bmi      = round(weight_current / (height_m ** 2), 1)

    return {
        "user_id":             user_id,
        "period_days":         days,
        "total_workouts":      total_workouts,
        "total_calories_burned": round(total_calories),
        "weight_start_kg":     weight_start,
        "weight_current_kg":   weight_current,
        "weight_change_kg":    weight_change,
        "current_bmi":         bmi,
        "weight_trend":        [{"date": str(l.date), "weight": l.weight_kg, "bmi": l.bmi} for l in weight_logs]
    }
