"""JSON file store for the POC. Replaces SQLite."""
from __future__ import annotations

import json
import threading
import uuid
from datetime import date, datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = ROOT / "data" / "store.json"
_lock = threading.Lock()


class Record:
    def __init__(self, data: dict):
        self._data = dict(data)
        for key, value in self._data.items():
            setattr(self, key, value)

    def to_dict(self) -> dict:
        return dict(self._data)


def _empty() -> dict:
    return {
        "users": [],
        "workout_logs": [],
        "weight_logs": [],
        "meal_logs": [],
        "next_id": 1,
    }


def _load() -> dict:
    if not DATA_FILE.exists():
        return _empty()
    with DATA_FILE.open(encoding="utf-8") as handle:
        data = json.load(handle)
    for key in ("users", "workout_logs", "weight_logs", "meal_logs"):
        data.setdefault(key, [])
    data.setdefault("next_id", 1)
    return data


def _save(data: dict) -> None:
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    temporary = DATA_FILE.with_suffix(".tmp")
    temporary.write_text(json.dumps(data, indent=2), encoding="utf-8")
    temporary.replace(DATA_FILE)


def _now() -> str:
    return datetime.now().isoformat(timespec="seconds")


def create_user(user_data: dict) -> Record:
    with _lock:
        data = _load()
        user = {
            "id": f"usr_{uuid.uuid4().hex[:8]}",
            "allergies": [],
            "location": "Hyderabad, India",
            "days_per_week": 3,
            "medical_notes": "",
            **user_data,
            "created_at": _now(),
            "updated_at": _now(),
        }
        data["users"].append(user)
        _save(data)
        return Record(user)


def get_user(user_id: str) -> Record | None:
    with _lock:
        data = _load()
    for user in data["users"]:
        if user["id"] == user_id:
            return Record(user)
    return None


def update_user(user_id: str, updates: dict) -> Record | None:
    with _lock:
        data = _load()
        for user in data["users"]:
            if user["id"] == user_id:
                user.update(updates)
                user["updated_at"] = _now()
                _save(data)
                return Record(user)
    return None


def _since(days: int) -> str:
    return (date.today() - timedelta(days=days)).isoformat()


def _next_id(data: dict) -> int:
    value = int(data["next_id"])
    data["next_id"] = value + 1
    return value


def log_workout(entry: dict) -> Record:
    with _lock:
        data = _load()
        row = {
            "id": _next_id(data),
            "notes": "",
            **entry,
            "date": entry.get("date") or date.today().isoformat(),
            "logged_at": _now(),
        }
        if not isinstance(row["date"], str):
            row["date"] = row["date"].isoformat()
        data["workout_logs"].append(row)
        _save(data)
        return Record(row)


def get_workout_logs(user_id: str, days: int = 30) -> list[Record]:
    cutoff = _since(days)
    with _lock:
        data = _load()
    rows = [
        row for row in data["workout_logs"]
        if row["user_id"] == user_id and row["date"] >= cutoff
    ]
    rows.sort(key=lambda row: row["date"], reverse=True)
    return [Record(row) for row in rows]


def log_weight(user_id: str, weight_kg: float, height_cm: float) -> Record:
    height_m = height_cm / 100 if height_cm else 0
    bmi = round(weight_kg / (height_m ** 2), 1) if height_m else None
    with _lock:
        data = _load()
        row = {
            "id": _next_id(data),
            "user_id": user_id,
            "date": date.today().isoformat(),
            "weight_kg": weight_kg,
            "bmi": bmi,
            "logged_at": _now(),
        }
        data["weight_logs"].append(row)
        _save(data)
        return Record(row)


def get_weight_logs(user_id: str, days: int = 30) -> list[Record]:
    cutoff = _since(days)
    with _lock:
        data = _load()
    rows = [
        row for row in data["weight_logs"]
        if row["user_id"] == user_id and row["date"] >= cutoff
    ]
    rows.sort(key=lambda row: row["date"])
    return [Record(row) for row in rows]
