from sqlalchemy import Column, String, Integer, Float, JSON, DateTime, Date
from sqlalchemy.sql import func
from backend.database.db import Base
import uuid


class User(Base):
    __tablename__ = "users"

    id             = Column(String, primary_key=True, default=lambda: f"usr_{uuid.uuid4().hex[:8]}")
    name           = Column(String, nullable=False)
    age            = Column(Integer)
    gender         = Column(String)
    weight_kg      = Column(Float)
    height_cm      = Column(Float)
    fitness_goal   = Column(String)   # weight_loss | muscle_gain | endurance | flexibility
    activity_level = Column(String)   # sedentary | light | moderate | active | very_active
    dietary_pref   = Column(String)   # vegan | vegetarian | keto | paleo | none
    allergies      = Column(JSON, default=list)
    location       = Column(String, default="Hyderabad, India")
    days_per_week  = Column(Integer, default=3)
    medical_notes  = Column(String, default="")
    created_at     = Column(DateTime, server_default=func.now())
    updated_at     = Column(DateTime, server_default=func.now(), onupdate=func.now())


class WorkoutLog(Base):
    __tablename__ = "workout_logs"

    id              = Column(Integer, primary_key=True, autoincrement=True)
    user_id         = Column(String, index=True)
    date            = Column(Date)
    exercises       = Column(JSON, default=list)
    duration_mins   = Column(Integer)
    calories_burned = Column(Float)
    intensity       = Column(String)  # low | medium | high
    notes           = Column(String, default="")
    logged_at       = Column(DateTime, server_default=func.now())


class WeightLog(Base):
    __tablename__ = "weight_logs"

    id        = Column(Integer, primary_key=True, autoincrement=True)
    user_id   = Column(String, index=True)
    date      = Column(Date)
    weight_kg = Column(Float)
    bmi       = Column(Float)
    logged_at = Column(DateTime, server_default=func.now())


class MealLog(Base):
    __tablename__ = "meal_logs"

    id             = Column(Integer, primary_key=True, autoincrement=True)
    user_id        = Column(String, index=True)
    date           = Column(Date)
    meal_type      = Column(String)  # breakfast | lunch | dinner | snack
    foods          = Column(JSON, default=list)
    total_calories = Column(Float)
    total_protein  = Column(Float)
    total_carbs    = Column(Float)
    total_fat      = Column(Float)
    logged_at      = Column(DateTime, server_default=func.now())
