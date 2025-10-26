# tests/test_factory.py
import pytest
from src.models import Stock, Bond, ETF
from patterns.factory import InstrumentFactory


def test_create_stock():
    data = {
        "symbol": "AAPL",
        "name": "Apple Inc.",
        "instrument_type": "Stock",
        "exchange": "NASDAQ",
        "currency": "USD",
    }
    inst = InstrumentFactory.create_instrument(data)
    assert isinstance(inst, Stock)
    assert inst.symbol == "AAPL"
    assert inst.exchange == "NASDAQ"


def test_create_bond():
    data = {
        "symbol": "US10Y",
        "name": "US Treasury 10Y",
        "instrument_type": "Bond",
        "coupon": 3.5,
        "maturity": "2033-01-01",
    }
    inst = InstrumentFactory.create_instrument(data)
    assert isinstance(inst, Bond)
    assert inst.coupon == 3.5


def test_create_etf():
    data = {
        "symbol": "SPY",
        "name": "SPDR S&P 500 ETF",
        "instrument_type": "ETF",
        "underlying_index": "S&P 500",
        "expense_ratio": 0.09,
    }
    inst = InstrumentFactory.create_instrument(data)
    assert isinstance(inst, ETF)
    assert "S&P" in inst.underlying_index


def test_invalid_type_raises():
    bad = {"symbol": "X", "name": "Bad", "instrument_type": "Crypto"}
    with pytest.raises(ValueError):
        InstrumentFactory.create_instrument(bad)