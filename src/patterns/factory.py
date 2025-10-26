import csv
from pathlib import Path
from src.models import Stock, Bond, ETF, Instrument


class InstrumentFactory:
    """Creates specific Instrument objects based on input dict or CSV row."""

    @staticmethod
    def create_instrument(data: dict) -> Instrument:
        itype = data.get("instrument_type", "").lower()

        if itype == "stock":
            return Stock(
                symbol=data["symbol"],
                name=data["name"],
                instrument_type="Stock",
                exchange=data.get("exchange", "N/A"),
                currency=data.get("currency", "USD"),
            )

        elif itype == "bond":
            return Bond(
                symbol=data["symbol"],
                name=data["name"],
                instrument_type="Bond",
                coupon=float(data.get("coupon", 0)),
                maturity=data.get("maturity", "N/A"),
            )

        elif itype == "etf":
            return ETF(
                symbol=data["symbol"],
                name=data["name"],
                instrument_type="ETF",
                underlying_index=data.get("underlying_index", "N/A"),
                expense_ratio=float(data.get("expense_ratio", 0)),
            )

        else:
            raise ValueError(f"Unknown instrument type: {itype}")

    @staticmethod
    def from_csv(csv_path: str | Path):
        """Demonstrate creation from instruments.csv"""
        instruments = []
        with open(csv_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                instruments.append(InstrumentFactory.create_instrument(row))
        return instruments