# TSMP — Laboratory Work 1

## Overview

This project demonstrates the implementation of several **software design patterns** in Python using a pairs trading backtesting system.

The system supports different hedge ratio estimation methods, including Static OLS, Rolling OLS, and Kalman Filter.

## Design Patterns

### 1. Builder Pattern

The **Builder** pattern allows complex objects to be constructed step by step, separating their construction from their final representation.

Instead of passing all configuration parameters directly to a constructor, the Builder provides methods for configuring individual components.

Example:

```python
builder = BacktestBuilder()

builder.set_estimator("kalman")
builder.set_strategy("zscore")

backtest = builder.build()
```

**Advantages:**
- Makes complex object construction more readable.
- Allows flexible configuration.
- Separates construction logic from business logic.

### 2. Singleton Pattern

The **Singleton** pattern ensures that a class has only one instance and provides a global access point to it.

In this project, it is used for centralized storage of backtesting results.

Example:

```python
import threading

class ResultsRegistry:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
        return cls._instance
```

The `__new__` method controls object creation, while `threading.Lock` prevents multiple threads from creating separate instances simultaneously.

**Advantages:**
- Provides a single shared instance.
- Centralizes access to results.
- Prevents duplicate instance creation.

### 3. Factory Pattern

The **Factory** pattern encapsulates object creation and allows the program to instantiate different implementations through a common interface.

In this project, it is used to create different hedge ratio estimators.

Example:

```python
class EstimatorFactory:
    @staticmethod
    def create(method):
        if method == "static":
            return StaticOLS()
        elif method == "rolling":
            return RollingOLS()
        elif method == "kalman":
            return KalmanFilter()

        raise ValueError("Unknown estimator")
```

Usage:

```python
estimator = EstimatorFactory.create("kalman")
```

**Advantages:**
- Centralizes object creation.
- Reduces dependencies on concrete classes.
- Makes adding new estimator types easier.

## Installation

Clone the repository:

```bash
git clone https://github.com/katr1nas/tsmp_lab1.git
cd tsmp_lab1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run:

```bash
python main.py
```

## Technologies

- Python
- NumPy
- Object-Oriented Programming
- Design Patterns

## Author

[katr1nas](https://github.com/katr1nas)
