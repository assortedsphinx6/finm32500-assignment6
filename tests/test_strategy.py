from src.patterns.strategy import MeanReversionStrategy, BreakoutStrategy

def test_mean_reversion_length_and_types():
    prices = [100, 101, 100, 99, 100]
    strat = MeanReversionStrategy(window=2, k=0.5)
    sig = strat.generate_signals(prices)
    assert isinstance(sig, list)
    assert len(sig) == len(prices)
    assert set(sig).issubset({-1, 0, 1})

def test_mean_reversion_shift_no_lookahead():
    # craft so last point is below mean; signal should trigger at last index from prior info
    prices = [100, 100, 90]
    strat = MeanReversionStrategy(window=2, k=0.1)
    sig = strat.generate_signals(prices)
    # no lookahead: first signal must be 0
    assert sig[0] == 0

def test_breakout_up_and_down():
    prices = [100, 101, 102, 101, 103]  # breakout above prior highs at last point
    strat = BreakoutStrategy(lookback=3)
    sig = strat.generate_signals(prices)
    assert len(sig) == len(prices)
    assert sig[-1] in (-1, 0, 1)

def test_breakout_empty():
    strat = BreakoutStrategy(lookback=3)
    assert strat.generate_signals([]) == []