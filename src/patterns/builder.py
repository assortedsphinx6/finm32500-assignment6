# patterns/builder.py
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Dict, Optional


@dataclass
class Portfolio:
    name: str
    owner: Optional[str] = None
    positions: List[Dict] = field(default_factory=list)
    subportfolios: List["Portfolio"] = field(default_factory=list)

    def total_value(self) -> float:
        """Recursively compute total market value."""
        value = sum(p["quantity"] * p["price"] for p in self.positions)
        for sp in self.subportfolios:
            value += sp.total_value()
        return value


class PortfolioBuilder:
    def __init__(self, name: str):
        self.name = name
        self.owner: Optional[str] = None
        self.positions: List[Dict] = []
        self.subportfolios: List[Portfolio] = []

    def set_owner(self, name: str) -> "PortfolioBuilder":
        self.owner = name
        return self

    def add_position(self, symbol: str, quantity: float, price: float) -> "PortfolioBuilder":
        self.positions.append({"symbol": symbol, "quantity": quantity, "price": price})
        return self

    def add_subportfolio(self, name: str, builder: "PortfolioBuilder") -> "PortfolioBuilder":
        self.subportfolios.append(builder.build())
        return self

    def build(self) -> Portfolio:
        return Portfolio(
            name=self.name,
            owner=self.owner,
            positions=self.positions,
            subportfolios=self.subportfolios,
        )