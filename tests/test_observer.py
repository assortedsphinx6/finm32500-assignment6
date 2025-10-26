from src.patterns.observer import SignalPublisher, LoggerObserver, AlertObserver

def test_logger_and_alert_observers():
    pub = SignalPublisher()
    logger = LoggerObserver()
    alert = AlertObserver()
    pub.attach(logger)
    pub.attach(alert)

    # normal signal (no alert)
    sig1 = {"symbol": "AAPL", "qty": 10, "price": 150}
    pub.notify(sig1)
    assert logger.log[-1]["symbol"] == "AAPL"
    assert len(alert.alerts) == 0

    # high price triggers alert
    sig2 = {"symbol": "GOOG", "qty": 5, "price": 2000}
    pub.notify(sig2)
    assert alert.alerts[-1]["symbol"] == "GOOG"
    assert len(logger.log) == 2