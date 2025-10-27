from pathlib import Path
import sys, json, logging
from collections import defaultdict

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger("main")

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.engine import Engine
from src.data_loader import YahooFinanceAdapter, BloombergXMLAdapter
from src.patterns.strategy import MeanReversionStrategy
from src.patterns.observer import LoggerObserver, AlertObserver


class StrategyTickAdapter:
    def __init__(self, inner, history_max=500):
        self.inner = inner
        self.history = defaultdict(list)
        self.history_max = history_max

    def generate_signals(self, tick):
        sym = getattr(tick, "symbol", None) or (tick.get("symbol") if isinstance(tick, dict) else None)
        price = getattr(tick, "price", None) or (tick.get("price") if isinstance(tick, dict) else None)
        if sym is None or price is None:
            return []
        h = self.history[sym]
        h.append(float(price))
        if len(h) > self.history_max:
            h[:] = h[-self.history_max:]
        try:
            out = self.inner.generate_signals(h)
        except Exception:
            return []
        if not out:
            return []
        last = int(out[-1])
        if last == 0:
            return []
        side = "BUY" if last > 0 else "SELL"
        return [{"symbol": sym, "side": side, "qty": 1, "price": price}]


def load_config():
    p = PROJECT_ROOT / "config.json"
    if p.exists():
        try:
            return json.loads(p.read_text())
        except Exception:
            pass
    return {}


def main():
    cfg = load_config()
    symbols = cfg.get("symbols", ["AAPL", "MSFT", "TSLA"])
    sr_params = cfg.get("mean_reversion_params", {"lookback": 5})

    # build strategy safely
    try:
        inner = MeanReversionStrategy(params=sr_params)
    except TypeError:
        try:
            inner = MeanReversionStrategy(**(sr_params or {}))
        except TypeError:
            inner = MeanReversionStrategy()
    strategy = StrategyTickAdapter(inner)

    engine = Engine(strategy)
    # attach observers quietly
    try:
        engine.attach_observer(LoggerObserver())
    except Exception:
        pass
    try:
        engine.attach_observer(AlertObserver())
    except Exception:
        pass

    # adapters
    data_dir = PROJECT_ROOT / "data"
    y = YahooFinanceAdapter(data_dir / "external_data_yahoo.json")
    b = BloombergXMLAdapter(data_dir / "external_data_bloomberg.xml")

    ticks = []
    for s in symbols:
        try:
            t = y.get_data(s)
            if t: ticks.append(t)
        except Exception:
            pass
        try:
            t = b.get_data(s)
            if t: ticks.append(t)
        except Exception:
            pass

    if not ticks:
        ticks = [{"symbol": "AAPL", "price": 90}, {"symbol": "AAPL", "price": 110}]

    for t in ticks:
        engine.on_tick(t)

if __name__ == "__main__":
    main()
