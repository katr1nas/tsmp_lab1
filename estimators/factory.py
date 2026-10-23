from abc import ABC, abstractmethod
from typing import Dict

from config import BacktestConfig
from estimators.base import HedgeEstimator
from estimators.kalman import KalmanHedge
from estimators.rolling import RollingOLSHedge
from estimators.static import StaticOLSHedge


class EstimatorFactory(ABC):
    @abstractmethod
    def create(self, config: BacktestConfig) -> HedgeEstimator:
        ...


class StaticHedgeFactory(EstimatorFactory):
    def create(self, config: BacktestConfig) -> HedgeEstimator:
        return StaticOLSHedge()


class KalmanHedgeFactory(EstimatorFactory):
    def create(self, config: BacktestConfig) -> HedgeEstimator:
        return KalmanHedge(config.kalman_process_noise, config.kalman_observation_noise)


class RollingHedgeFactory(EstimatorFactory):
    def create(self, config: BacktestConfig) -> HedgeEstimator:
        return RollingOLSHedge(config.rolling_window)


_FACTORIES: Dict[str, EstimatorFactory] = {
    "static": StaticHedgeFactory(),
    "kalman": KalmanHedgeFactory(),
    "rolling": RollingHedgeFactory(),
}


def register_factory(kind: str, factory: EstimatorFactory) -> None:
    _FACTORIES[kind] = factory


def get_factory(kind: str) -> EstimatorFactory:
    try:
        return _FACTORIES[kind]
    except KeyError:
        raise ValueError(f"Estimator not supported: {kind}")
