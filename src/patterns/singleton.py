from __future__ import annotations
import json
from pathlib import Path

class Singleton:
    _instances: dict[type, object] = {}
    def __new__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__new__(cls)
        return cls._instances[cls]

class Config(Singleton):
    def __init__(self, config_path: str | Path | None = None):
        default_path = Path(__file__).resolve().parents[2] / "data" / "config.json"
        path = Path(config_path) if config_path else default_path
        if getattr(self, "_initialized", False):
            if config_path is not None:
                self._load(path)
            return

        self._load(path)
        self._initialized = True

    @classmethod
    def instance(cls) -> "Config":
        return cls()

    def _load(self, path: Path) -> None:
        with open(path, "r", encoding="utf-8") as f:
            self._data = json.load(f)
        self._config_path = Path(path)

    def get(self, key, default=None):
        return self._data.get(key, default)

    def get_path(self, *keys, default=None):
        cur = self._data
        for k in keys:
            if isinstance(cur, dict) and k in cur:
                cur = cur[k]
            else:
                return default
        return cur