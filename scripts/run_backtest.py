# scripts/run_backtest.py
from momentum_portfolio_research import Config, MomentumBacktest


def main():
    """Run the momentum portfolio backtest."""
    config = Config()
    backtest = MomentumBacktest(config)
    results = backtest.run()
    backtest.plot_results(results)


if __name__ == "__main__":
    main()