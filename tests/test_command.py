from src.patterns.command import ExecuteOrderCommand, CommandInvoker

def test_execute_and_undo_buy():
    broker = {"cash": 1000, "positions": {}}
    invoker = CommandInvoker()
    cmd = ExecuteOrderCommand(broker, "AAPL", "BUY", 2, 100)

    invoker.do(cmd)
    assert broker["cash"] == 800
    assert broker["positions"]["AAPL"] == 2

    invoker.undo()
    assert broker["cash"] == 1000
    assert broker["positions"]["AAPL"] == 0

def test_redo_restores_buy():
    broker = {"cash": 1000, "positions": {}}
    invoker = CommandInvoker()
    cmd = ExecuteOrderCommand(broker, "AAPL", "BUY", 1, 200)

    invoker.do(cmd)
    invoker.undo()
    invoker.redo()

    assert broker["cash"] == 800
    assert broker["positions"]["AAPL"] == 1