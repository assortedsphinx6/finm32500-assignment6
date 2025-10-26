from src.analytics import VolatilityDecorator, BetaDecorator, DrawdownDecorator

class DummyInstrument:
    symbol = "AAPL"
    name = "Apple"
    instrument_type = "Stock"

def test_volatility_adds_key():
    d = VolatilityDecorator(DummyInstrument(), [100, 101, 102, 99])
    m = d.get_metrics()
    assert "volatility" in m

def test_beta_adds_key():
    d = BetaDecorator(DummyInstrument(), [100, 102, 101], [100, 101, 102])
    m = d.get_metrics()
    assert "beta" in m

def test_drawdown_adds_key():
    d = DrawdownDecorator(DummyInstrument(), [100, 120, 90, 95])
    m = d.get_metrics()
    assert "max_drawdown" in m
    assert m["max_drawdown"] <= 0.0

def test_stacking_decorators():
    base = DummyInstrument()
    v = VolatilityDecorator(base, [100, 102, 101, 103])
    b = BetaDecorator(v, [100, 102, 101, 103], [200, 201, 203, 202])
    d = DrawdownDecorator(b, [100, 120, 90, 110])
    m = d.get_metrics()
    for k in ("symbol", "volatility", "beta", "max_drawdown"):
        assert k in m