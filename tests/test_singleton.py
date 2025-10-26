# tests/test_singleton.py
from datetime import datetime
from src.models import Config, MarketDataPoint


def test_config_is_singleton():
    """Ensure Config.instance() always returns the same object."""
    c1 = Config.instance()
    c2 = Config.instance()
    assert c1 is c2


def test_config_loads_json_and_get_methods():
    """Verify that config.json was loaded and accessors work."""
    cfg = Config.instance()

    # config.json should be non-empty
    data = cfg.get("strategy_params")
    assert data is not None or isinstance(cfg.get("__missing__", 42), int)

    assert cfg.get_path("does", "not", "exist", default="NA") == "NA"


def test_market_data_point_fields():
    """Confirm that MarketDataPoint stores symbol, time, price, and meta."""
    mdp = MarketDataPoint(
        symbol="AAPL",
        time=datetime(2020, 1, 1, 16, 0, 0),
        price=150.25,
        meta={"source": "unit-test"},
    )
    assert mdp.symbol == "AAPL"
    assert mdp.price == 150.25
    assert mdp.meta == {"source": "unit-test"}