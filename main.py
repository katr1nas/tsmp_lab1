import dataclasses

from backtest.builder import StandardBacktestBuilder
from backtest.director import BacktestDirector
from config import BacktestConfig
from data.data_source import SyntheticPairSource
from estimators.factory import get_factory
from infra.trade_logger import TradeLogger
from registry.results_registry import ResultsRegistry
from strategy.signal_strategy import ZScoreStrategy


def main() -> None:
    config = BacktestConfig()
    logger = TradeLogger()

    builder = StandardBacktestBuilder()
    director = BacktestDirector(builder, config, logger)
    registry = ResultsRegistry()

    presets = (
        director.build_static_baseline,
        director.build_kalman_adaptive,
        director.build_rolling_benchmark,
    )

    for seed in config.pair_seeds:
        source = SyntheticPairSource(seed)
        for configure in presets:
            configure()
            backtester = builder.build()
            result = backtester.run(source)
            registry.add(source.label, backtester.estimator_name, result)

    print()
    print(f"{'Method':<18}{'Mean Sharpe':>12}")
    for method, sharpe in registry.mean_sharpe().items():
        print(f"{method:<18}{sharpe:>12.2f}")

    won, total = registry.wins("Kalman", "Static OLS")
    print(f"\nKalman beats Static on {won} of {total} pairs")

    fast = dataclasses.replace(config, kalman_process_noise=1e-5)
    custom = (
        builder.set_config(fast)
        .set_logger(logger)
        .set_strategy(ZScoreStrategy(fast.entry_z, fast.exit_z, fast.stop_z))
        .set_estimator(get_factory("kalman").create(fast))
        .build()
    )
    custom_result = custom.run(SyntheticPairSource(1))
    print(f"\nCustom Kalman (process noise 1e-5): sharpe={custom_result.sharpe:.2f} trades={custom_result.trades}")

    print(f"\nSingleton: {ResultsRegistry() is registry}, stored runs: {len(registry.results)}")


if __name__ == "__main__":
    main()
