import datetime
from typing import List, Optional, Any, Dict
from backend.models import User, WorkoutLog, WeightLog, MealLog
from backend.database.db import json_store


# ── User CRUD (JSON Store) ───────────────────────────────────────────────────

def create_user(arg1: Any, arg2: Optional[Dict] = None) -> User:
    """Create and store user profile in data/users.json."""
    user_data = arg2 if arg2 is not None else arg1
    users = json_store.read("users.json")
    if not isinstance(users, dict):
        users = {}

    user = User(**user_data)
    users[user.id] = user.model_dump()
    json_store.write("users.json", users)
    return user


def get_user(arg1: Any, arg2: Optional[str] = None) -> Optional[User]:
    """Retrieve user profile from data/users.json by ID."""
    user_id = str(arg2 if arg2 is not None else arg1)
    users = json_store.read("users.json")
    if not isinstance(users, dict):
        return None
    data = users.get(user_id)
    if data:
        return User(**data)
    return None


def update_user(arg1: Any, arg2: Any, arg3: Optional[Dict] = None) -> Optional[User]:
    """Update user profile in data/users.json."""
    if arg3 is not None:
        user_id, updates = str(arg2), arg3
    else:
        user_id, updates = str(arg1), arg2

    users = json_store.read("users.json")
    if not isinstance(users, dict) or user_id not in users:
        return None

    user_dict = users[user_id]
    user_dict.update(updates)
    user_dict["updated_at"] = datetime.datetime.now().isoformat()
    users[user_id] = user_dict
    json_store.write("users.json", users)
    return User(**user_dict)


# ── Workout Log CRUD (JSON Store) ─────────────────────────────────────────────

def log_workout(arg1: Any, arg2: Optional[Dict] = None) -> WorkoutLog:
    """Log a workout session to data/workout_logs.json."""
    data = arg2 if arg2 is not None else arg1
    logs = json_store.read("workout_logs.json")
    if not isinstance(logs, list):
        logs = []

    next_id = max([item.get("id", 0) for item in logs], default=0) + 1
    log_dict = dict(data)
    log_dict["id"] = next_id
    if not log_dict.get("date"):
        log_dict["date"] = str(datetime.date.today())
    else:
        log_dict["date"] = str(log_dict["date"])

    if not log_dict.get("logged_at"):
        log_dict["logged_at"] = datetime.datetime.now().isoformat()

    workout = WorkoutLog(**log_dict)
    logs.append(workout.model_dump())
    json_store.write("workout_logs.json", logs)
    return workout


def get_workout_logs(arg1: Any, arg2: Optional[Any] = None, days: int = 30) -> List[WorkoutLog]:
    """Get workout history for a user over the last N days."""
    if arg2 is not None and not isinstance(arg2, int):
        user_id = str(arg2)
    else:
        user_id = str(arg1)
        if isinstance(arg2, int):
            days = arg2

    logs = json_store.read("workout_logs.json")
    if not isinstance(logs, list):
        return []

    cutoff = (datetime.date.today() - datetime.timedelta(days=days)).isoformat()
    filtered = [
        WorkoutLog(**item) for item in logs
        if str(item.get("user_id")) == user_id and str(item.get("date", "")) >= cutoff
    ]
    filtered.sort(key=lambda x: str(x.date), reverse=True)
    return filtered


# ── Weight Log CRUD (JSON Store) ──────────────────────────────────────────────

def log_weight(arg1: Any, user_id: Optional[str] = None, weight_kg: Optional[float] = None, height_cm: Optional[float] = None) -> WeightLog:
    """Log body weight and compute BMI in data/weight_logs.json."""
    if height_cm is not None:
        target_uid = str(user_id)
        w_kg = float(weight_kg)
        h_cm = float(height_cm)
    else:
        target_uid = str(arg1)
        w_kg = float(user_id)
        h_cm = float(weight_kg) if weight_kg is not None else 170.0

    height_m = (h_cm or 170.0) / 100.0
    bmi = round(w_kg / (height_m ** 2), 1) if height_m > 0 else 22.0

    logs = json_store.read("weight_logs.json")
    if not isinstance(logs, list):
        logs = []

    next_id = max([item.get("id", 0) for item in logs], default=0) + 1
    log_dict = {
        "id": next_id,
        "user_id": target_uid,
        "date": str(datetime.date.today()),
        "weight_kg": w_kg,
        "bmi": bmi,
        "logged_at": datetime.datetime.now().isoformat()
    }
    weight_log = WeightLog(**log_dict)
    logs.append(weight_log.model_dump())
    json_store.write("weight_logs.json", logs)
    return weight_log


def get_weight_logs(arg1: Any, arg2: Optional[Any] = None, days: int = 30) -> List[WeightLog]:
    """Get weight progress entries for a user over the last N days."""
    if arg2 is not None and not isinstance(arg2, int):
        user_id = str(arg2)
    else:
        user_id = str(arg1)
        if isinstance(arg2, int):
            days = arg2

    logs = json_store.read("weight_logs.json")
    if not isinstance(logs, list):
        return []

    cutoff = (datetime.date.today() - datetime.timedelta(days=days)).isoformat()
    filtered = [
        WeightLog(**item) for item in logs
        if str(item.get("user_id")) == user_id and str(item.get("date", "")) >= cutoff
    ]
    filtered.sort(key=lambda x: str(x.date))  # Ascending order for progress trend charts
    return filtered


# ── Meal Log CRUD (JSON Store) ────────────────────────────────────────────────

def log_meal(arg1: Any, arg2: Optional[Dict] = None) -> MealLog:
    """Log a meal entry in data/meal_logs.json."""
    data = arg2 if arg2 is not None else arg1
    logs = json_store.read("meal_logs.json")
    if not isinstance(logs, list):
        logs = []

    next_id = max([item.get("id", 0) for item in logs], default=0) + 1
    log_dict = dict(data)
    log_dict["id"] = next_id
    if not log_dict.get("date"):
        log_dict["date"] = str(datetime.date.today())
    else:
        log_dict["date"] = str(log_dict["date"])

    if not log_dict.get("logged_at"):
        log_dict["logged_at"] = datetime.datetime.now().isoformat()

    meal = MealLog(**log_dict)
    logs.append(meal.model_dump())
    json_store.write("meal_logs.json", logs)
    return meal


def get_meal_logs(arg1: Any, arg2: Optional[Any] = None, days: int = 7) -> List[MealLog]:
    """Get meal logs for a user over the last N days."""
    if arg2 is not None and not isinstance(arg2, int):
        user_id = str(arg2)
    else:
        user_id = str(arg1)
        if isinstance(arg2, int):
            days = arg2

    logs = json_store.read("meal_logs.json")
    if not isinstance(logs, list):
        return []

    cutoff = (datetime.date.today() - datetime.timedelta(days=days)).isoformat()
    filtered = [
        MealLog(**item) for item in logs
        if str(item.get("user_id")) == user_id and str(item.get("date", "")) >= cutoff
    ]
    filtered.sort(key=lambda x: str(x.date), reverse=True)
    return filtered


# ── Food Nutrition Queries (JSON Store - foods.json) ───────────────────────────

def get_all_foods() -> List[dict]:
    """Retrieve full food list from data/foods.json."""
    data = json_store.read("foods.json")
    if isinstance(data, dict):
        return data.get("foods", [])
    elif isinstance(data, list):
        return data
    return []


def search_foods(query: str, limit: int = 20) -> List[dict]:
    """Search foods by name in data/foods.json."""
    query = (query or "").strip().lower()
    foods = get_all_foods()
    if not query:
        return foods[:limit]
    matches = [f for f in foods if query in f.get("name", "").lower()]
    return matches[:limit]


def get_food(name: str) -> Optional[dict]:
    """Find a specific food by exact/case-insensitive name."""
    target = (name or "").strip().lower()
    foods = get_all_foods()
    for f in foods:
        if f.get("name", "").strip().lower() == target:
            return f
    return None
