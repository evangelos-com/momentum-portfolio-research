# momentum_portfolio_research/analysis/plotting.py
import matplotlib.pyplot as plt
import pandas as pd

from ..config import Config


def plot_results(portfolio_cum: pd.Series, benchmark_cum: pd.Series) -> None:
    """
    Plot portfolio performance vs benchmark.
    
    Args:
        portfolio_cum: Cumulative returns for momentum portfolio
        benchmark_cum: Cumulative returns for benchmark
    """
    plt.figure(figsize=(14, 7))
    plt.plot(portfolio_cum, label="Momentum Portfolio", linewidth=2, color="#1f77b4")
    plt.plot(benchmark_cum, label=f"{Config.BENCHMARK_TICKER} Benchmark", linestyle="--", linewidth=2, color="#ff7f0e")
    
    plt.title("Momentum Strategy vs Benchmark", fontsize=16, fontweight="bold")
    plt.xlabel("Date", fontsize=12)
    plt.ylabel("Cumulative Returns", fontsize=12)
    plt.legend(fontsize=11, loc="upper left")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    plt.savefig("output/momentum_backtest.png", dpi=300, bbox_inches="tight")
    print("Chart saved to output/momentum_backtest.png")
    plt.show()