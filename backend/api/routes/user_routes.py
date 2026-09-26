from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional

from backend.agents.location_agent import find_nearby_gyms
from backend.agents.nutrition_agent import build_meal_plan
from backend.store import create_user, get_user, update_user

router = APIRouter(prefix="/users", tags=["Users"])


class UserCreate(BaseModel):
    name: str
    age: int
    gender: str
    weight_kg: float
    height_cm: float
    fitness_goal: str
    activity_level: str
    dietary_pref: Optional[str] = "none"
    allergies: Optional[List[str]] = []
    location: Optional[str] = "Hyderabad, India"
    days_per_week: Optional[int] = 3
    medical_notes: Optional[str] = ""


class UserUpdate(BaseModel):
    weight_kg: Optional[float] = None
    fitness_goal: Optional[str] = None
    activity_level: Optional[str] = None
    dietary_pref: Optional[str] = None
    location: Optional[str] = None
    days_per_week: Optional[int] = None


@router.post("/onboard")
def onboard_user(user: UserCreate):
    height_m = user.height_cm / 100
    bmi = round(user.weight_kg / (height_m ** 2), 1)
    created = create_user(user.model_dump())
    return {
        "status": "success",
        "user_id": created.id,
        "name": created.name,
        "bmi": bmi,
        "message": f"Welcome to WellnessMitra, {created.name}!",
    }


@router.get("/{user_id}/gyms")
def nearby_gyms(user_id: str):
    user = get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    try:
        gyms = find_nearby_gyms(user.location or "Hyderabad, India")
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Gym search failed: {exc}") from exc
    return {"location": user.location, "gyms": gyms}


@router.get("/{user_id}/meal-plan")
def meal_plan(user_id: str):
    user = get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return build_meal_plan(user.to_dict())


@router.get("/{user_id}/profile")
def get_profile(user_id: str):
    user = get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user.to_dict()


@router.put("/{user_id}/profile")
def update_profile(user_id: str, updates: UserUpdate):
    if not get_user(user_id):
        raise HTTPException(status_code=404, detail="User not found")
    update_data = {key: value for key, value in updates.model_dump().items() if value is not None}
    updated = update_user(user_id, update_data)
    return {"status": "updated", "user": updated.to_dict()}
