from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Sequence, List
import pandas as pd # type: ignore
from src.patterns.singleton import Config


class Strategy(ABC):
    """Interchangeable strategy interface."""
    @abstractmethod
    def generate_signals(self, prices: Sequence[float]) -> List[int]:
        """Return list of {-1,0,+1} signals for given price history."""
        ...


class MeanReversionStrategy(Strategy):
    """
    Buy when price is sufficiently below rolling mean,
    sell when price is sufficiently above.
    """
    def __init__(self, window: int | None = None, k: float | None = None):
        cfg = Config.instance()
        self.window = window if window is not None else int(
            cfg.get_path("strategy_params", "mean_reversion", "window", default=5)
        )
        self.k = k if k is not None else float(
            cfg.get_path("strategy_params", "mean_reversion", "k", default=1.0)
        )

    def generate_signals(self, prices: Sequence[float]) -> List[int]:
        s = pd.Series(list(prices), dtype="float64")
        if s.empty:
            return []

        mean = s.rolling(self.window, min_periods=1).mean()
        std = s.rolling(self.window, min_periods=1).std().fillna(0.0)

        upper = mean + self.k * std
        lower = mean - self.k * std

        sig = (s < lower).astype(int) - (s > upper).astype(int)  # +1 if below, -1 if above, else 0
        sig = sig.shift(1).fillna(0).astype(int)
        return sig.tolist()


class BreakoutStrategy(Strategy):
    """
    Buy on upside breakout above prior lookback high,
    sell on downside breakout below prior lookback low.
    """
    def __init__(self, lookback: int | None = None):
        cfg = Config.instance()
        self.lookback = lookback if lookback is not None else int(
            cfg.get_path("strategy_params", "breakout", "lookback", default=20)
        )

    def generate_signals(self, prices: Sequence[float]) -> List[int]:
        s = pd.Series(list(prices), dtype="float64")
        if s.empty:
            return []

        prior_high = s.shift(1).rolling(self.lookback, min_periods=1).max()
        prior_low = s.shift(1).rolling(self.lookback, min_periods=1).min()

        buy = (s > prior_high).astype(int)
        sell = (s < prior_low).astype(int)

        sig = buy - sell 
        return sig.astype(int).tolist()