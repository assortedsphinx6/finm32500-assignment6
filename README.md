# FINM 32500 – Assignment 6: Design Patterns in Financial Software Architecture

## Overview
This project implements a modular financial analytics and trading simulation system using object-oriented design patterns.
Each design pattern solves a realistic financial software problem and emphasizes modularity, flexibility, and maintainability.

---

## Architecture Summary
- **Creational Patterns:** Factory, Singleton, Builder  
- **Structural Patterns:** Decorator, Adapter, Composite  
- **Behavioral Patterns:** Strategy, Observer, Command

---

## Key Modules
- **data_loader.py:** Adapters for Yahoo and Bloomberg mock data.  
- **models.py:** Instrument classes (Stock, Bond, ETF) and MarketDataPoint structure.  
- **engine.py:** Core trade engine managing strategies, orders, and observers.  
- **reporting.py:** Simple analytics summaries and output formatting.  
- **main.py:** Orchestrates data loading, portfolio construction, and engine execution.

---

## Testing
Tests use `pytest` and `coverage` for validation.

Run all tests:
coverage run -m pytest -q


## Run Simulation
python -m src.main



