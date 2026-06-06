# momentum_portfolio_research/analysis/backtest_engine.py
import pandas as pd


class BacktestEngine:
    """Computes portfolio performance metrics."""
    
    @staticmethod
    def compute_portfolio_returns(df: pd.DataFrame) -> tuple[pd.Series, pd.DataFrame]:
        """
        Calculate daily portfolio returns.
        
        Args:
            df: Panel DataFrame with weight and return columns
            
        Returns:
            Tuple of (portfolio_returns Series, updated DataFrame)
        """
        df = df.copy()
        
        # Weight each stock's return by its portfolio weight
        df["weighted_return"] = df["weight"] * df["return"]
        
        # Sum weighted returns across all stocks for each day
        portfolio_returns = (
            df.groupby("date")["weighted_return"]
            .sum()
            .fillna(0)
        )
        
        return portfolio_returns, df
    
    @staticmethod
    def compute_cumulative_returns(returns: pd.Series) -> pd.Series:
        """
        Convert daily returns to cumulative returns.
        
        Args:
            returns: Series of daily returns
            
        Returns:
            Series of cumulative returns (compounded)
        """
        return (1 + returns).cumprod()