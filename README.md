# Momentum Portfolio Research

A momentum-based portfolio strategy that selects the top 3 performers by 90-day price momentum and rebalances monthly.

## Technical Write-Up

A detailed explanation of the system design, data pipeline, and pandas-based implementation is available here:

[Building a Simple Momentum Portfolio in Python](https://www.evangelos.com/posts/building-a-simple-momentum-portfolio-in-python--from-market-data-to-backtesting)

## Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd momentum-portfolio-research
```

### 2. Create a virtual environment (recommended)

```bash
python3 -m venv venv
```

Activate the virtual environment:

**On macOS/Linux:**
```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Run the backtest

```bash
python scripts/run_backtest.py
```

## Strategy

- Downloads historical price data for 10 stocks (AAPL, MSFT, GOOG, AMZN, META, NVDA, TSLA, JPM, UNH, HD)
- Computes 90-day momentum signal
- Selects top 3 stocks by momentum
- Equal-weight portfolio, rebalance monthly
- Compares against SPY benchmark

## Results (2020-2026)

[![Figure 1](/output/momentum_backtest.png)](/output/momentum_backtest.png)

| Metric | Value |
|--------|-------|
| **Momentum Portfolio** | 13.5x |
| **SPY Benchmark** | 2.5x |
| **Outperformance** | 11x |

## Key Limitations

- Backtested only (2020-2026 tech bull market)
- No transaction costs, slippage, or taxes modeled
- Limited to 10 stocks, single signal

## Disclaimer

For educational and research purposes only. Not financial advice. Past performance does not guarantee future results.