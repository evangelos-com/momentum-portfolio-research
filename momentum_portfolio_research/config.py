# momentum_portfolio_research/config.py
class Config:
    """Strategy configuration parameters."""
    
    TICKERS = [
        "AAPL", "MSFT", "GOOG", "AMZN", "META",
        "NVDA", "TSLA", "JPM", "UNH", "HD"
    ]
    START_DATE = "2020-01-01"
    MOMENTUM_WINDOW = 90  # days
    TOP_N = 3  # number of stocks to hold
    REBALANCE_FREQ = "ME"  # month end
    BENCHMARK_TICKER = "SPY"