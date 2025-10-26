class SignalPublisher:
    """Publishes signals to registered observers."""
    def __init__(self):
        self.observers = []

    def attach(self, observer):
        self.observers.append(observer)

    def notify(self, signal):
        for obs in self.observers:
            obs.update(signal)


class LoggerObserver:
    """Simply logs all signals."""
    def __init__(self):
        self.log = []

    def update(self, signal):
        self.log.append(signal)


class AlertObserver:
    """Raises an alert if price > 1000 or qty > 1000."""
    def __init__(self):
        self.alerts = []

    def update(self, signal):
        if signal.get("price", 0) > 1000 or signal.get("qty", 0) > 1000:
            self.alerts.append(signal)