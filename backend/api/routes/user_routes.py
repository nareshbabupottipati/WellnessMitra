from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List
from backend.database.db import get_db
from backend.database.crud import create_user, get_user, update_user

router = APIRouter(prefix="/users", tags=["Users"])


class UserCreate(BaseModel):
    name:           str
    age:            int
    gender:         str
    weight_kg:      float
    height_cm:      float
    fitness_goal:   str
    activity_level: str
    dietary_pref:   Optional[str] = "none"
    allergies:      Optional[List[str]] = []
    location:       Optional[str] = "Hyderabad, India"
    days_per_week:  Optional[int] = 3
    medical_notes:  Optional[str] = ""


class UserUpdate(BaseModel):
    weight_kg:      Optional[float] = None
    fitness_goal:   Optional[str]   = None
    activity_level: Optional[str]   = None
    dietary_pref:   Optional[str]   = None
    location:       Optional[str]   = None
    days_per_week:  Optional[int]   = None


@router.post("/onboard")
def onboard_user(user: UserCreate, db: Session = Depends(get_db)):
    """Create a new user profile."""
    height_m = user.height_cm / 100
    bmi = round(user.weight_kg / (height_m ** 2), 1)
    user_data = user.model_dump()
    created = create_user(db, user_data)
    return {
        "status":  "success",
        "user_id": created.id,
        "name":    created.name,
        "bmi":     bmi,
        "message": f"Welcome to WellnessMitra, {created.name}! 🎉"
    }


@router.get("/{user_id}/profile")
def get_profile(user_id: str, db: Session = Depends(get_db)):
    """Retrieve a user's profile."""
    user = get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/{user_id}/profile")
def update_profile(user_id: str, updates: UserUpdate, db: Session = Depends(get_db)):
    """Update specific user profile fields."""
    user = get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    update_data = {k: v for k, v in updates.model_dump().items() if v is not None}
    updated = update_user(db, user_id, update_data)
    return {"status": "updated", "user": updated}
