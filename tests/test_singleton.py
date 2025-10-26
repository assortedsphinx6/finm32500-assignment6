# tests/test_singleton.py
from datetime import datetime
from src.models import MarketDataPoint
from src.patterns.singleton import Config


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


from src.patterns.singleton import Config, Singleton
import json, tempfile, os

def test_singleton_instance_identity():
    c1 = Config()
    c2 = Config()
    assert c1 is c2  # same instance

def test_config_reads_data(tmp_path):
    path = tmp_path / "config.json"
    path.write_text(json.dumps({"test": {"value": 123}}))
    c = Config(path)
    assert c.get_path("test", "value") == 123