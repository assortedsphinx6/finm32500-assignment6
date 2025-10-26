from datetime import datetime
from pathlib import Path
from src.data_loader import YahooFinanceAdapter, BloombergXMLAdapter
from src.models import MarketDataPoint


def test_yahoo_adapter(tmp_path: Path):
    path = tmp_path / "external_data_yahoo.json"
    path.write_text('{"symbol": "AAPL", "time": "2020-01-01", "price": 150}', encoding="utf-8")

    adapter = YahooFinanceAdapter(path)
    mdp = adapter.get_data("AAPL")
    assert isinstance(mdp, MarketDataPoint)
    assert mdp.symbol == "AAPL"
    assert mdp.price == 150.0
    assert isinstance(mdp.time, datetime)


def test_bloomberg_adapter(tmp_path: Path):
    path = tmp_path / "external_data_bloomberg.xml"
    path.write_text('<data symbol="AAPL" time="2020-01-01" price="150.0"/>', encoding="utf-8")

    adapter = BloombergXMLAdapter(path)
    mdp = adapter.get_data("AAPL")
    assert isinstance(mdp, MarketDataPoint)
    assert mdp.symbol == "AAPL"
    assert mdp.price == 150.0
    assert isinstance(mdp.time, datetime)