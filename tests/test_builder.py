from patterns.builder import PortfolioBuilder, Portfolio


def test_simple_portfolio_build():
    pb = PortfolioBuilder("Main")
    pb.set_owner("Alice").add_position("AAPL", 10, 150.0).add_position("MSFT", 5, 300.0)
    portfolio = pb.build()

    assert isinstance(portfolio, Portfolio)
    assert portfolio.owner == "Alice"
    assert len(portfolio.positions) == 2
    assert round(portfolio.total_value(), 2) == 10 * 150 + 5 * 300


def test_nested_subportfolio():
    main = PortfolioBuilder("Main").set_owner("Alice")
    sub = PortfolioBuilder("Tech").add_position("GOOG", 2, 2800)
    main.add_subportfolio("Tech", sub)
    portfolio = main.build()

    assert len(portfolio.subportfolios) == 1
    assert portfolio.subportfolios[0].name == "Tech"
    assert round(portfolio.total_value(), 2) == 2 * 2800


def test_fluent_interface_returns_self():
    pb = PortfolioBuilder("Test")
    result = pb.set_owner("Bob").add_position("TSLA", 1, 700)
    assert result is pb