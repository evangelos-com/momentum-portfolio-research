# momentum_portfolio_research/signals/engine.py
import pandas as pd


class SignalEngine:
    """Generates trading signals based on momentum."""
    
    @staticmethod
    def compute_signals(df: pd.DataFrame, window: int) -> pd.DataFrame:
        """
        Calculate momentum signal as price change over window.
        
        Args:
            df: Panel DataFrame with price data
            window: Lookback window in days for momentum calculation
            
        Returns:
            DataFrame with momentum column added
        """
        df = df.copy()
        df["momentum"] = df.groupby("ticker")["price"].pct_change(window)
        return df
    
    @staticmethod
    def rank_and_select(df: pd.DataFrame, top_n: int) -> pd.DataFrame:
        """
        Rank stocks by momentum and select top performers.
        
        IMPORTANT: We do NOT drop NaN momentum values. Instead, we keep them
        in the dataframe but mark them as not selected. This ensures all
        date-ticker combinations exist, which is critical for proper
        weight forward-filling in the portfolio construction.
        
        Args:
            df: Panel DataFrame with momentum column
            top_n: Number of top performers to select
            
        Returns:
            DataFrame with rank and selected columns added
        """
        df = df.copy()
        
        # Rank by momentum within each date, with NaN values ranked last
        df["rank"] = (
            df.groupby("date")["momentum"]
            .rank(ascending=False, method="first", na_option="bottom")
        )
        
        # Select only top N performers
        df["selected"] = df["rank"] <= top_n
        
        # Explicitly mark NaN momentum rows as not selected
        df.loc[df["momentum"].isna(), "selected"] = False

        sample_date = df["date"].drop_duplicates().iloc[100]

        print(f"\n=== Snapshot for {sample_date} ===")
        print(
            df[df["date"] == sample_date]
            .sort_values("rank")
            .loc[:, ["ticker", "price", "momentum", "rank", "selected"]]
        )
        
        return df