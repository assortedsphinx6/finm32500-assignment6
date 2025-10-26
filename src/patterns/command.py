class ExecuteOrderCommand:
    """Simple command: executes and undoes a trade on a broker dict."""
    def __init__(self, broker, symbol, side, qty, price):
        self.broker = broker
        self.symbol = symbol
        self.side = side.upper()
        self.qty = qty
        self.price = price
        self._done = False

    def execute(self):
        if self._done:
            return
        if self.side == "BUY":
            self.broker["cash"] -= self.qty * self.price
            self.broker["positions"][self.symbol] = self.broker["positions"].get(self.symbol, 0) + self.qty
        elif self.side == "SELL":
            self.broker["cash"] += self.qty * self.price
            self.broker["positions"][self.symbol] = self.broker["positions"].get(self.symbol, 0) - self.qty
        self._done = True

    def undo(self):
        if not self._done:
            return
        if self.side == "BUY":
            self.broker["cash"] += self.qty * self.price
            self.broker["positions"][self.symbol] -= self.qty
        elif self.side == "SELL":
            self.broker["cash"] -= self.qty * self.price
            self.broker["positions"][self.symbol] += self.qty
        self._done = False


class CommandInvoker:
    """Handles undo/redo for executed commands."""
    def __init__(self):
        self.done = []
        self.undone = []

    def do(self, cmd):
        cmd.execute()
        self.done.append(cmd)
        self.undone.clear()

    def undo(self):
        if not self.done:
            return
        cmd = self.done.pop()
        cmd.undo()
        self.undone.append(cmd)

    def redo(self):
        if not self.undone:
            return
        cmd = self.undone.pop()
        cmd.execute()
        self.done.append(cmd)