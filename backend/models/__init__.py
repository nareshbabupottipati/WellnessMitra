import uuid
import datetime
from typing import List, Optional, Any
from pydantic import BaseModel, Field


class BaseModelWithAccess(BaseModel):
    def __getitem__(self, item: str) -> Any:
        return getattr(self, item)

    def get(self, item: str, default: Any = None) -> Any:
        return getattr(self, item, default)

    model_config = {"extra": "allow"}


class User(BaseModelWithAccess):
    id: str = Field(default_factory=lambda: f"usr_{uuid.uuid4().hex[:8]}")
    name: str
    age: Optional[int] = None
    gender: Optional[str] = None
    weight_kg: Optional[float] = None
    height_cm: Optional[float] = None
    fitness_goal: Optional[str] = "general_fitness"  # weight_loss | muscle_gain | endurance | flexibility
    activity_level: Optional[str] = "moderate"       # sedentary | light | moderate | active | very_active
    dietary_pref: Optional[str] = "none"             # vegan | vegetarian | keto | paleo | none
    allergies: List[str] = Field(default_factory=list)
    location: Optional[str] = "Hyderabad, India"
    days_per_week: Optional[int] = 3
    medical_notes: Optional[str] = ""
    created_at: Optional[str] = Field(default_factory=lambda: datetime.datetime.now().isoformat())
    updated_at: Optional[str] = Field(default_factory=lambda: datetime.datetime.now().isoformat())


class WorkoutLog(BaseModelWithAccess):
    id: Optional[int] = None
    user_id: str
    date: str = Field(default_factory=lambda: str(datetime.date.today()))
    exercises: List[dict] = Field(default_factory=list)
    duration_mins: int = 0
    calories_burned: float = 0.0
    intensity: Optional[str] = "medium"  # low | medium | high
    notes: Optional[str] = ""
    logged_at: Optional[str] = Field(default_factory=lambda: datetime.datetime.now().isoformat())


class WeightLog(BaseModelWithAccess):
    id: Optional[int] = None
    user_id: str
    date: str = Field(default_factory=lambda: str(datetime.date.today()))
    weight_kg: float
    bmi: float
    logged_at: Optional[str] = Field(default_factory=lambda: datetime.datetime.now().isoformat())


class MealLog(BaseModelWithAccess):
    id: Optional[int] = None
    user_id: str
    date: str = Field(default_factory=lambda: str(datetime.date.today()))
    meal_type: Optional[str] = "lunch"  # breakfast | lunch | dinner | snack
    foods: List[dict] = Field(default_factory=list)
    total_calories: float = 0.0
    total_protein: float = 0.0
    total_carbs: float = 0.0
    total_fat: float = 0.0
    logged_at: Optional[str] = Field(default_factory=lambda: datetime.datetime.now().isoformat())
