import json
import os
from pathlib import Path
from typing import Any, Dict, List
from backend.config import DATA_DIR


class JSONStore:
    """Lightweight JSON file store replacing relational DB."""

    def __init__(self, data_dir: Path = DATA_DIR):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self._ensure_files()

    def _file_path(self, filename: str) -> Path:
        return self.data_dir / filename

    def _ensure_files(self):
        defaults = {
            "users.json": {},
            "workout_logs.json": [],
            "weight_logs.json": [],
            "meal_logs.json": [],
            "foods.json": {"foods": []}
        }
        for fname, default_data in defaults.items():
            path = self._file_path(fname)
            if not path.exists() or path.stat().st_size == 0:
                with open(path, "w", encoding="utf-8") as f:
                    json.dump(default_data, f, indent=2)

    def read(self, filename: str) -> Any:
        path = self._file_path(filename)
        if not path.exists():
            return {} if filename.endswith("users.json") else []
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {} if filename.endswith("users.json") else []

    def write(self, filename: str, data: Any):
        path = self._file_path(filename)
        temp_path = path.with_suffix(".tmp")
        with open(temp_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, default=str)
        temp_path.replace(path)


# Singleton store instance
json_store = JSONStore()


def get_db():
    """FastAPI dependency yielding JSONStore instance."""
    yield json_store


# Stubs for backwards compatibility if imported
class DummyMetadata:
    @staticmethod
    def create_all(bind=None):
        pass


class DummyBase:
    metadata = DummyMetadata()


Base = DummyBase()
engine = None
