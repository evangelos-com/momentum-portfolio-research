# momentum_portfolio_research/portfolio/builder.py
import pandas as pd
import numpy as np


class PortfolioBuilder:
    """Constructs and manages portfolio weights."""
    
    @staticmethod
    def generate_rebalance_dates(df: pd.DataFrame, freq: str) -> np.ndarray:
        """
        Generate rebalance dates based on frequency.
        
        Args:
            df: DataFrame with date column
            freq: Rebalance frequency (e.g., "ME" for month-end)
            
        Returns:
            Array of rebalance dates
        """
        dates = pd.to_datetime(df["date"].unique())
        dates = pd.Series(dates).sort_values()
        dates.index = dates
        
        rebalance_dates = dates.resample(freq).last()
        return rebalance_dates.dropna().values
    
    @staticmethod
    def build_portfolio(df: pd.DataFrame, rebalance_freq: str) -> pd.DataFrame:
        """
        Assign portfolio weights with monthly rebalancing.
        
        Weights are set on rebalance dates for selected stocks (equal-weight),
        then carried forward to the next rebalance date. This ensures daily
        portfolio value changes based on daily price movements of holdings.
        
        Args:
            df: Panel DataFrame with selected column
            rebalance_freq: Rebalance frequency
            
        Returns:
            DataFrame with weight column added
        """
        df = df.copy()
        df = df.sort_values(["ticker", "date"]).reset_index(drop=True)
        
        rebalance_dates = PortfolioBuilder.generate_rebalance_dates(df, rebalance_freq)
        
        print(f"Generated {len(rebalance_dates)} rebalance dates")
        
        df["weight"] = 0.0
        portfolio_tickers: dict[pd.Timestamp, list[str]] = {}
        
        # Assign equal weights to selected stocks on rebalance dates
        for date in rebalance_dates:
            mask = (df["date"] == date) & (df["selected"] == True)
            selected = df.loc[mask]
            
            print(f"Rebalance {date}: {len(selected)} stocks selected")
            
            if len(selected) == 0:
                portfolio_tickers[date] = []
                continue
            
            tickers_in_portfolio = selected["ticker"].unique().tolist()
            portfolio_tickers[date] = tickers_in_portfolio
            
            weight = 1.0 / len(selected)
            df.loc[mask, "weight"] = weight
        
        # Forward fill weights for each rebalance period
        # This ensures weights persist until the next rebalance
        rebalance_dates_sorted = sorted(portfolio_tickers.keys())
        
        for i, rebal_date in enumerate(rebalance_dates_sorted):
            tickers = portfolio_tickers[rebal_date]
            
            # Determine next rebalance date (or end of data)
            if i + 1 < len(rebalance_dates_sorted):
                next_rebal_date = rebalance_dates_sorted[i + 1]
            else:
                next_rebal_date = df["date"].max()
            
            # For each ticker in current portfolio, carry weight forward
            for ticker in tickers:
                ticker_mask = (
                    (df["ticker"] == ticker) & 
                    (df["date"] >= rebal_date) & 
                    (df["date"] < next_rebal_date)
                )
                weight_on_rebal = df.loc[
                    (df["ticker"] == ticker) & (df["date"] == rebal_date), 
                    "weight"
                ].values
                
                if len(weight_on_rebal) > 0:
                    df.loc[ticker_mask, "weight"] = weight_on_rebal[0]
        
        return df