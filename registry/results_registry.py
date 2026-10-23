import threading
from dataclasses import dataclass
from typing import Dict, List, Tuple

import numpy as np

from backtest.metrics import Performance


@dataclass(frozen=True)
class RunResult:
    pair: str
    method: str
    performance: Performance


class ResultsRegistry:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls) -> "ResultsRegistry":
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    instance = super().__new__(cls)
                    instance._results = []
                    cls._instance = instance
        return cls._instance

    @property
    def results(self) -> List[RunResult]:
        return list(self._results)

    def add(self, pair: str, method: str, performance: Performance) -> None:
        self._results.append(RunResult(pair, method, performance))

    def clear(self) -> None:
        self._results.clear()

    def mean_sharpe(self) -> Dict[str, float]:
        grouped: Dict[str, List[float]] = {}
        for run in self._results:
            grouped.setdefault(run.method, []).append(run.performance.sharpe)
        return {method: float(np.mean(values)) for method, values in grouped.items()}

    def wins(self, method: str, versus: str) -> Tuple[int, int]:
        by_pair: Dict[str, Dict[str, float]] = {}
        for run in self._results:
            by_pair.setdefault(run.pair, {})[run.method] = run.performance.sharpe
        comparable = [p for p in by_pair.values() if method in p and versus in p]
        won = sum(p[method] > p[versus] for p in comparable)
        return won, len(comparable)
