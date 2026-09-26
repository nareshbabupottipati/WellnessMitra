from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.store import get_user, get_weight_logs, get_workout_logs, log_weight

router = APIRouter(prefix="/progress", tags=["Progress"])


class WeightLogRequest(BaseModel):
    user_id: str
    weight_kg: float


@router.post("/weight")
def add_weight_log(req: WeightLogRequest):
    user = get_user(req.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    entry = log_weight(req.user_id, req.weight_kg, user.height_cm)
    return {
        "status": "logged",
        "date": entry.date,
        "weight_kg": entry.weight_kg,
        "bmi": entry.bmi,
    }


@router.get("/{user_id}/summary")
def get_progress_summary(user_id: str, days: int = 30):
    user = get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    workout_logs = get_workout_logs(user_id, days)
    weight_logs = get_weight_logs(user_id, days)
    total_calories = sum(log.calories_burned or 0 for log in workout_logs)
    weight_start = weight_logs[0].weight_kg if weight_logs else user.weight_kg
    weight_current = weight_logs[-1].weight_kg if weight_logs else user.weight_kg
    weight_change = round(weight_current - weight_start, 2)
    height_m = (user.height_cm or 170) / 100
    bmi = round(weight_current / (height_m ** 2), 1)

    return {
        "user_id": user_id,
        "period_days": days,
        "total_workouts": len(workout_logs),
        "total_calories_burned": round(total_calories),
        "weight_start_kg": weight_start,
        "weight_current_kg": weight_current,
        "weight_change_kg": weight_change,
        "current_bmi": bmi,
        "weight_trend": [
            {"date": log.date, "weight": log.weight_kg, "bmi": log.bmi}
            for log in weight_logs
        ],
    }
