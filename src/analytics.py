import pandas as pd # type: ignore

class MetricsDecorator:
    """Base decorator for adding analytics to instruments (stackable)."""
    def __init__(self, instrument):
        self.instrument = instrument  

    def get_metrics(self):
        if hasattr(self.instrument, "get_metrics"):
            return self.instrument.get_metrics()

        return {
            "symbol": getattr(self.instrument, "symbol", None),
            "name": getattr(self.instrument, "name", None),
            "type": getattr(self.instrument, "instrument_type", None),
        }


class VolatilityDecorator(MetricsDecorator):
    """Adds volatility (std of returns)."""
    def __init__(self, instrument, prices):
        super().__init__(instrument)
        self.prices = pd.Series(prices)

    def get_metrics(self):
        m = super().get_metrics()
        returns = self.prices.pct_change().dropna()
        m["volatility"] = float(returns.std()) if not returns.empty else 0.0
        return m


class BetaDecorator(MetricsDecorator):
    """Adds beta vs. market (cov/var)."""
    def __init__(self, instrument, prices, market_prices):
        super().__init__(instrument)
        self.prices = pd.Series(prices)
        self.market_prices = pd.Series(market_prices)

    def get_metrics(self):
        m = super().get_metrics()
        r = self.prices.pct_change().dropna()
        rm = self.market_prices.pct_change().dropna()
        if r.empty or rm.empty or rm.var() == 0:
            m["beta"] = 0.0
        else:
            m["beta"] = float(r.cov(rm) / rm.var())
        return m


class DrawdownDecorator(MetricsDecorator):
    """Adds max drawdown (min of price/cummax - 1)."""
    def __init__(self, instrument, prices):
        super().__init__(instrument)
        self.prices = pd.Series(prices)

    def get_metrics(self):
        m = super().get_metrics()
        if self.prices.empty:
            m["max_drawdown"] = 0.0
            return m
        peak = self.prices.cummax()
        dd = self.prices / peak - 1.0
        m["max_drawdown"] = float(dd.min())
        return m