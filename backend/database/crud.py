from sqlalchemy.orm import Session
from backend.models import User, WorkoutLog, WeightLog, MealLog
import datetime


# ── User CRUD ──────────────────────────────────────────────────────────────────

def create_user(db: Session, user_data: dict) -> User:
    user = User(**user_data)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user(db: Session, user_id: str) -> User:
    return db.query(User).filter(User.id == user_id).first()


def update_user(db: Session, user_id: str, updates: dict) -> User:
    db.query(User).filter(User.id == user_id).update(updates)
    db.commit()
    return get_user(db, user_id)


# ── Workout Log CRUD ───────────────────────────────────────────────────────────

def log_workout(db: Session, data: dict) -> WorkoutLog:
    log = WorkoutLog(**data)
    db.add(log)
    db.commit()
    db.refresh(log)
    return log


def get_workout_logs(db: Session, user_id: str, days: int = 30):
    since = datetime.date.today() - datetime.timedelta(days=days)
    return (
        db.query(WorkoutLog)
        .filter(WorkoutLog.user_id == user_id, WorkoutLog.date >= since)
        .order_by(WorkoutLog.date.desc())
        .all()
    )


# ── Weight Log CRUD ────────────────────────────────────────────────────────────

def log_weight(db: Session, user_id: str, weight_kg: float, height_cm: float) -> WeightLog:
    height_m = height_cm / 100
    bmi = round(weight_kg / (height_m ** 2), 1)
    log = WeightLog(
        user_id=user_id,
        date=datetime.date.today(),
        weight_kg=weight_kg,
        bmi=bmi
    )
    db.add(log)
    db.commit()
    db.refresh(log)
    return log


def get_weight_logs(db: Session, user_id: str, days: int = 30):
    since = datetime.date.today() - datetime.timedelta(days=days)
    return (
        db.query(WeightLog)
        .filter(WeightLog.user_id == user_id, WeightLog.date >= since)
        .order_by(WeightLog.date.asc())
        .all()
    )


# ── Meal Log CRUD ──────────────────────────────────────────────────────────────

def log_meal(db: Session, data: dict) -> MealLog:
    meal = MealLog(**data)
    db.add(meal)
    db.commit()
    db.refresh(meal)
    return meal


def get_meal_logs(db: Session, user_id: str, days: int = 7):
    since = datetime.date.today() - datetime.timedelta(days=days)
    return (
        db.query(MealLog)
        .filter(MealLog.user_id == user_id, MealLog.date >= since)
        .order_by(MealLog.date.desc())
        .all()
    )
