# src/models.py
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
import json
from typing import Any, Dict, Optional

@dataclass(frozen=True)
class MarketDataPoint:
    """Represents a single tick of normalized market data."""
    symbol: str
    time: datetime
    price: float
    meta: Optional[Dict[str, Any]] = None

class Config:
    """Singleton configuration loader."""
    _instance: "Config | None" = None

    def __new__(cls, *args, **kwargs):
        raise RuntimeError("Use Config.instance() instead of direct constructor.")

    @classmethod
    def instance(cls) -> "Config":
        if cls._instance is None:
            obj = object.__new__(cls)
            obj._load()
            cls._instance = obj
        return cls._instance

    def _load(self):
        """Load config.json from the data folder."""
        root = Path(__file__).resolve().parents[1]  # project root (above src/)
        config_path = root / "data" / "config.json"
        with open(config_path, "r", encoding="utf-8") as f:
            self._data = json.load(f)

    def get(self, key: str, default: Any = None) -> Any:
        return self._data.get(key, default)

    def get_path(self, *keys: str, default: Any = None) -> Any:
        cur = self._data
        for k in keys:
            if isinstance(cur, dict) and k in cur:
                cur = cur[k]
            else:
                return default
        return cur
    

@dataclass
class Instrument:
    """Base class for all instruments."""
    symbol: str
    name: str
    instrument_type: str

    def get_summary(self) -> str:
        return f"{self.instrument_type}: {self.symbol} - {self.name}"


@dataclass
class Stock(Instrument):
    exchange: str
    currency: str


@dataclass
class Bond(Instrument):
    coupon: float
    maturity: str


@dataclass
class ETF(Instrument):
    underlying_index: str
    expense_ratio: float