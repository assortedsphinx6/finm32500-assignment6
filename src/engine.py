from patterns.observer import SignalPublisher
from patterns.command import ExecuteOrderCommand, CommandInvoker
from data_loader import MarketDataPoint


class Engine:
    def __init__(self, strategy):
        self.strategy = strategy
        self.publisher = SignalPublisher()
        self.invoker = CommandInvoker()

        self.book = {
            "history": [],   
            "positions": {},  
            "cash": 1000000 
        }

    def on_tick(self, tick: MarketDataPoint):
        signals = self.strategy.generate_signals(tick)
        for signal in signals:
            signal.setdefault("qty", 1)
            signal.setdefault("price", tick.price)
            signal.setdefault("symbol", tick.symbol)

            # Notify external observers
            self.publisher.notify(signal)

            # Execute and record order command
            cmd = ExecuteOrderCommand(self.book, signal)
            self.invoker.execute(cmd)

    def attach_observer(self, observer):
        """Register an observer dynamically."""
        self.publisher.attach(observer)

    def get_position(self, symbol):
        """Return the current position for a symbol."""
        return self.book["positions"].get(symbol, 0)

    def get_portfolio_value(self, market_prices=None):
        """
        Compute current portfolio value given market prices.
        (market_prices: dict {symbol: price})
        """
        if market_prices is None:
            market_prices = {}
        value = self.book["cash"]
        for sym, qty in self.book["positions"].items():
            value += qty * market_prices.get(sym, 0)
        return value

    def undo_last_trade(self):
        """Undo the most recent trade command."""
        return self.invoker.undo()

    def redo_last_trade(self):
        """Redo a previously undone trade command."""
        return self.invoker.redo()
