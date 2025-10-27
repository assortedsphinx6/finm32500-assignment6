# Design Report — FINM32500 Assignment 6

## Overview
This project implements a **modular financial analytics and trading simulation platform** using key *object-oriented design patterns* across three categories:
- **Creational Patterns** — for object instantiation and configuration.
- **Structural Patterns** — for system composition and extensibility.
- **Behavioral Patterns** — for dynamic runtime behavior and interaction.

The goal is to demonstrate how classical design patterns enable flexibility, reusability, and maintainability in a finance context.

---

## 🏗️ Creational Patterns

### 1. Factory Pattern
**Module:** `patterns/factory.py`

**Purpose:**  
Creates different financial instrument objects (`Stock`, `Bond`, `ETF`) dynamically from raw data in `instruments.csv`.

**Rationale:**  
Encapsulates object creation logic so new instruments can be added without changing existing code.

**Trade-offs:**
- ✅ Centralizes instantiation and enforces consistent interface.  
- ⚠️ Adds one layer of indirection; small overhead for simple objects.

---

### 2. Singleton Pattern
**Module:** `patterns/singleton.py`

**Purpose:**  
Provides a single shared configuration instance (`Config`) across modules for settings, logging, and parameters.

**Rationale:**  
Global configuration ensures consistent access without passing config objects through every constructor.

**Trade-offs:**
- ✅ Guarantees one global config point.  
- ⚠️ Reduces test isolation (shared global state).

---

### 3. Builder Pattern
**Module:** `patterns/builder.py`

**Purpose:**  
Constructs complex hierarchical `Portfolio` objects with nested sub-portfolios and positions.

**Rationale:**  
Simplifies creation of deeply nested portfolio structures (e.g., from `portfolio_structure.json`) using a fluent interface.

**Trade-offs:**
- ✅ Clear, chainable portfolio construction.  
- ⚠️ Adds extra abstraction over direct dictionary construction.

---

## 🧱 Structural Patterns

### 4. Decorator Pattern
**Module:** `analytics.py`

**Purpose:**  
Adds analytics such as volatility, beta, and drawdown to instruments without modifying their core implementation.

**Implementation:**  
`VolatilityDecorator`, `BetaDecorator`, `DrawdownDecorator` wrap base `Instrument` objects and extend their `get_metrics()` method.

**Rationale:**  
Allows flexible extension of analytics computations at runtime (stackable decorators).

**Trade-offs:**
- ✅ Enables composable metrics.  
- ⚠️ Deep decorator chains can be harder to debug.

---

### 5. Adapter Pattern
**Module:** `data_loader.py`

**Purpose:**  
Unifies external data sources (Yahoo JSON, Bloomberg XML) into a common internal `MarketDataPoint` interface.

**Rationale:**  
Allows the system to treat heterogeneous data feeds uniformly when ingesting prices and symbols.

**Trade-offs:**
- ✅ Decouples data sources from engine logic.  
- ⚠️ Slight parsing overhead; must maintain adapters for each new data format.

---

### 6. Composite Pattern
**Module:** `models.py`

**Purpose:**  
Represents portfolios as recursive trees of `PortfolioGroup` (composites) and `Position` (leaves).

**Rationale:**  
Allows uniform treatment of portfolios and single positions when computing aggregate value.

**Trade-offs:**
- ✅ Simplifies recursive value calculation.  
- ⚠️ Slightly more complex structure traversal.

---

## 🔁 Behavioral Patterns

### 7. Strategy Pattern
**Module:** `patterns/strategy.py`

**Purpose:**  
Encapsulates trading signal logic behind a uniform interface (`generate_signals`).  
Implements `MeanReversionStrategy` and `BreakoutStrategy`.

**Integration:**  
The `Engine` (in `engine.py`) accepts any strategy implementing this interface.  
`StrategyTickAdapter` (in `main.py`) bridges tick-based data to the price-series interface expected by the strategy.

**Rationale:**  
Makes trading logic interchangeable and easily extendable.

**Trade-offs:**
- ✅ Encourages experimentation with new models.  
- ⚠️ Slight performance cost from indirection.

---

### 8. Observer Pattern
**Module:** `patterns/observer.py`

**Purpose:**  
Decouples event publication (`SignalPublisher`) from subscribers (`LoggerObserver`, `AlertObserver`).

**Integration:**  
`Engine` notifies observers when signals are generated or trades executed.

**Rationale:**  
Allows multiple independent modules (logging, alerts, analytics) to react to trade events.

**Trade-offs:**
- ✅ Enables extensible event handling.  
- ⚠️ Observer ordering and duplicate notifications must be managed carefully.

---

### 9. Command Pattern
**Module:** `patterns/command.py`

**Purpose:**  
Encapsulates order execution as command objects (`ExecuteOrderCommand`) with support for undo/redo via `CommandInvoker`.

**Integration:**  
Used in `Engine` to execute trades and maintain transaction history.

**Rationale:**  
Provides a reversible, auditable trade-execution mechanism.

**Trade-offs:**
- ✅ Enables undo/redo functionality and separation of command logic.  
- ⚠️ Slightly more verbose than direct method calls.

---

## ⚙️ Integration Summary

| Layer | Module | Pattern | Role |
|-------|---------|----------|------|
| Data Ingestion | `data_loader.py` | Adapter | Converts raw feeds into unified objects |
| Analytics | `analytics.py` | Decorator | Adds metrics dynamically |
| Models | `models.py` | Composite | Hierarchical portfolios |
| Engine | `engine.py` | Command, Observer | Executes orders, notifies observers |
| Strategy | `patterns/strategy.py` | Strategy | Interchangeable trading logic |
| Configuration | `patterns/singleton.py` | Singleton | Shared config instance |
| Portfolio Builder | `patterns/builder.py` | Builder | Constructs portfolios programmatically |
| Factory | `patterns/factory.py` | Factory | Creates instrument instances |
| Orchestration | `main.py` | — | Integrates all modules, runs simulation |

---

## 🧩 Design Rationale

The system was designed with **modularity and extensibility** as the highest priority.  
Each major concept (data, analytics, execution, portfolio) is isolated via one or more classical patterns.  
This design makes it straightforward to:

- Plug in new data adapters or strategies.
- Extend analytics without modifying core instrument classes.
- Reuse the same components in simulation or live trading.

---

## ⚖️ Trade-offs and Future Work

| Aspect | Benefit | Cost / Limitation |
|--------|----------|------------------|
| **Pattern clarity** | Improves readability and educational value | Adds boilerplate to small examples |
| **Extensibility** | Easy to add new analytics, strategies, adapters | Requires consistent interfaces |
| **Undo/Redo** | Safe, testable trade management | Slight complexity in command history |
| **Loose coupling** | Enables unit testing and reusability | Harder to trace runtime flow |

**Future Enhancements:**
- Add more robust market-data caching and persistence (e.g., TimescaleDB).
- Support asynchronous strategy execution for multiple instruments.
- Extend observer layer to include reporting or GUI dashboards.

---