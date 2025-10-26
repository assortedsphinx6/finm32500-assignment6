from pathlib import Path
import json
import xml.etree.ElementTree as ET
from datetime import datetime
from src.models import MarketDataPoint


class YahooFinanceAdapter:
    """Adapter for JSON-based market data."""

    def __init__(self, filepath: str | Path):
        self.filepath = Path(filepath)

    def get_data(self, symbol: str) -> MarketDataPoint:
        with open(self.filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        # assume JSON shape: { "symbol": "AAPL", "time": "2020-01-01", "price": 100 }
        return MarketDataPoint(
            symbol=data["symbol"],
            time=datetime.fromisoformat(data["time"]),
            price=float(data["price"]),
            meta={"source": "yahoo"}
        )


class BloombergXMLAdapter:
    """Adapter for XML-based market data."""

    def __init__(self, filepath: str | Path):
        self.filepath = Path(filepath)

    def get_data(self, symbol: str) -> MarketDataPoint:
        tree = ET.parse(self.filepath)
        root = tree.getroot()
        # assume XML shape: <data symbol="AAPL" time="2020-01-01" price="100.0"/>
        node = root.find(".")
        return MarketDataPoint(
            symbol=node.get("symbol"),
            time=datetime.fromisoformat(node.get("time")),
            price=float(node.get("price")),
            meta={"source": "bloomberg"}
        )