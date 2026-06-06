# momentum_portfolio_research/data/loader.py
import pandas as pd


class DataLoader:
    """Handles fetching and processing price data."""
    
    @staticmethod
    def load_price_data(tickers: list[str], start_date: str) -> pd.DataFrame:
        """
        Download adjusted close prices from Yahoo Finance.
        
        Args:
            tickers: List of stock tickers to download
            start_date: Start date in YYYY-MM-DD format
            
        Returns:
            DataFrame with dates as index and tickers as columns
        """
        import yfinance as yf
        
        data = yf.download(tickers, start=start_date, group_by="column")
        
        # Extract adjusted close or close prices
        if isinstance(data.columns, pd.MultiIndex):
            if "Adj Close" in data.columns.levels[0]:
                data = data["Adj Close"]
            else:
                data = data["Close"]
        else:
            if "Adj Close" in data.columns:
                data = data["Adj Close"]
            else:
                data = data["Close"]
        
        # Forward fill for missing values (holidays) and drop all-NaN rows
        return data.ffill().dropna(how="all")
    
    @staticmethod
    def build_panel(price_df: pd.DataFrame) -> pd.DataFrame:
        """
        Convert wide price format to long panel format with returns.
        
        Args:
            price_df: DataFrame with dates as index and tickers as columns
            
        Returns:
            Long-format DataFrame with date, ticker, price, and returns
        """
        df = price_df.stack().reset_index()
        df.columns = ["date", "ticker", "price"]
        
        # Ensure dates are datetime
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
        df = df.dropna(subset=["date"])
        
        # Sort and calculate returns
        df = df.sort_values(["ticker", "date"])
        df["return"] = df.groupby("ticker")["price"].pct_change()
        
        return df