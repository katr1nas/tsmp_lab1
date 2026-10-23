from abc import ABC, abstractmethod

from backtest.backtester import Backtester
from config import BacktestConfig
from estimators.base import HedgeEstimator
from infra.trade_logger import TradeLogger
from strategy.signal_strategy import SignalStrategy


class BacktestBuilder(ABC):
    @abstractmethod
    def set_estimator(self, estimator: HedgeEstimator) -> "BacktestBuilder":
        ...

    @abstractmethod
    def set_strategy(self, strategy: SignalStrategy) -> "BacktestBuilder":
        ...

    @abstractmethod
    def set_config(self, config: BacktestConfig) -> "BacktestBuilder":
        ...

    @abstractmethod
    def set_logger(self, logger: TradeLogger) -> "BacktestBuilder":
        ...

    @abstractmethod
    def build(self) -> Backtester:
        ...


class StandardBacktestBuilder(BacktestBuilder):
    def __init__(self) -> None:
        self.reset()

    def reset(self) -> "StandardBacktestBuilder":
        self._estimator = None
        self._strategy = None
        self._config = None
        self._logger = None
        return self

    def set_estimator(self, estimator: HedgeEstimator) -> "StandardBacktestBuilder":
        self._estimator = estimator
        return self

    def set_strategy(self, strategy: SignalStrategy) -> "StandardBacktestBuilder":
        self._strategy = strategy
        return self

    def set_config(self, config: BacktestConfig) -> "StandardBacktestBuilder":
        self._config = config
        return self

    def set_logger(self, logger: TradeLogger) -> "StandardBacktestBuilder":
        self._logger = logger
        return self

    def build(self) -> Backtester:
        parts = {
            "estimator": self._estimator,
            "strategy": self._strategy,
            "config": self._config,
            "logger": self._logger,
        }
        missing = [name for name, value in parts.items() if value is None]
        if missing:
            raise ValueError(f"Backtest is not fully configured, missing: {', '.join(missing)}")
        backtester = Backtester(self._estimator, self._strategy, self._config, self._logger)
        self.reset()
        return backtester
