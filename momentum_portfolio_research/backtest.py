# momentum_portfolio_research/backtest.py
from typing import Dict
from .config import Config
from .data.loader import DataLoader
from .signals.engine import SignalEngine
from .portfolio.builder import PortfolioBuilder
from .analysis.backtest_engine import BacktestEngine
from .analysis.plotting import plot_results
from .benchmark.loader import BenchmarkLoader


class MomentumBacktest:
    """Orchestrates the entire backtest workflow."""
    
    def __init__(self, config: Config):
        """
        Initialize backtest with configuration.
        
        Args:
            config: Config object with strategy parameters
        """
        self.config = config
        self.data_loader = DataLoader()
        self.signal_engine = SignalEngine()
        self.portfolio_builder = PortfolioBuilder()
        self.backtest_engine = BacktestEngine()
        self.benchmark_loader = BenchmarkLoader()
    
    def run(self) -> Dict:
        """
        Execute the backtest.
        
        Returns:
            Dictionary containing results
        """
        print("=" * 70)
        print("MOMENTUM PORTFOLIO BACKTEST")
        print("=" * 70)
        print(f"Period: {self.config.START_DATE} to present")
        print(f"Stocks: {', '.join(self.config.TICKERS)}")
        print(f"Momentum Window: {self.config.MOMENTUM_WINDOW} days")
        print(f"Portfolio Size: {self.config.TOP_N} stocks")
        print(f"Rebalance Frequency: {self.config.REBALANCE_FREQ}")
        print("=" * 70)
        print()
        
        # Data loading and preparation
        print("[1/6] Loading price data...")
        prices = self.data_loader.load_price_data(
            self.config.TICKERS, 
            self.config.START_DATE
        )
        
        print("[2/6] Building panel data...")
        df = self.data_loader.build_panel(prices)
        
        print("[3/6] Computing momentum signals...")
        df = self.signal_engine.compute_signals(df, self.config.MOMENTUM_WINDOW)
        
        print("[4/6] Ranking and selecting stocks...")
        df = self.signal_engine.rank_and_select(df, self.config.TOP_N)
        
        print("[5/6] Building portfolio with weights...")
        df = self.portfolio_builder.build_portfolio(df, self.config.REBALANCE_FREQ)
        
        print("[6/6] Computing returns...")
        portfolio_returns, df = self.backtest_engine.compute_portfolio_returns(df)
        portfolio_cum = self.backtest_engine.compute_cumulative_returns(portfolio_returns)
        
        benchmark_returns = self.benchmark_loader.load_benchmark(
            self.config.START_DATE,
            self.config.BENCHMARK_TICKER
        )
        benchmark_cum = self.backtest_engine.compute_cumulative_returns(benchmark_returns)
        
        print()
        
        # Calculate metrics
        total_return = portfolio_cum.iloc[-1].item() - 1
        benchmark_return = benchmark_cum.iloc[-1].item() - 1
        outperformance = total_return - benchmark_return
        
        # Print results
        print("=" * 70)
        print("RESULTS")
        print("=" * 70)
        print(f"Portfolio Total Return:    {total_return:>10.2%}")
        print(f"Benchmark Total Return:    {benchmark_return:>10.2%}")
        print(f"Outperformance:            {outperformance:>10.2%}")
        print("=" * 70)
        print()
        
        return {
            "portfolio_returns": portfolio_returns,
            "portfolio_cum": portfolio_cum,
            "benchmark_cum": benchmark_cum,
            "df": df,
            "total_return": total_return,
            "benchmark_return": benchmark_return,
            "outperformance": outperformance,
        }
    
    def plot_results(self, results: Dict) -> None:
        """
        Plot portfolio performance vs benchmark.
        
        Args:
            results: Dictionary returned from run()
        """
        portfolio_cum = results["portfolio_cum"]
        benchmark_cum = results["benchmark_cum"]
        
        plot_results(portfolio_cum, benchmark_cum)