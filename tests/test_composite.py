from src.models import Position, PortfolioGroup, PortfolioComponent

def test_position_value_and_leaf():
    p = Position("AAPL", 10, 150.0)
    assert isinstance(p, PortfolioComponent)
    assert p.get_value() == 1500.0
    assert p.get_positions() == [p]

def test_group_aggregation():
    g = PortfolioGroup("Tech")
    g.add(Position("AAPL", 10, 150.0))  # 1500
    g.add(Position("MSFT", 5, 300.0))   # 1500
    assert g.get_value() == 3000.0
    syms = {pos.symbol for pos in g.get_positions()}
    assert syms == {"AAPL", "MSFT"}

def test_nested_groups_recursive():
    main = PortfolioGroup("Main")
    tech = PortfolioGroup("Tech")
    bonds = PortfolioGroup("Bonds")

    tech.add(Position("NVDA", 2, 500.0))   # 1000
    tech.add(Position("MSFT", 1, 300.0))   # 300
    bonds.add(Position("US10Y", 10, 95.0)) # 950

    main.add(tech)
    main.add(bonds)

    assert main.get_value() == 1000 + 300 + 950
    all_pos = main.get_positions()
    assert len(all_pos) == 3
    assert {p.symbol for p in all_pos} == {"NVDA", "MSFT", "US10Y"}