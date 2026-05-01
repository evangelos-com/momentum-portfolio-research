# momentum_portfolio_research/benchmark/loader.py
import pandas as pd
import yfinance as yf


class BenchmarkLoader:
    """Loads benchmark data for comparison."""
    
    @staticmethod
    def load_benchmark(start_date: str, ticker: str = "SPY") -> pd.Series:
        """
        Download benchmark returns.
        
        Args:
            start_date: Start date in YYYY-MM-DD format
            ticker: Benchmark ticker (default: SPY)
            
        Returns:
            Series of daily returns
        """
        data = yf.download(ticker, start=start_date)
        
        # Extract adjusted close or close price
        if isinstance(data.columns, pd.MultiIndex):
            if "Adj Close" in data.columns.levels[0]:
                spy = data["Adj Close"]
            else:
                spy = data["Close"]
        else:
            if "Adj Close" in data.columns:
                spy = data["Adj Close"]
            else:
                spy = data["Close"]
        
        spy = spy.ffill()
        return spy.pct_change().fillna(0)