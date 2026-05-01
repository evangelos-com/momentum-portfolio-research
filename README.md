# Momentum Portfolio Research

A momentum-based equity strategy that selects the top 3 performers by 90-day price momentum with monthly rebalancing, implemented as a modular Python data pipeline using pandas and vectorized time-series transformations for backtesting.

## Technical Write-Up

A detailed explanation of the system design, data pipeline architecture, and pandas-based implementation:

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

## Architecture

The system is implemented as a modular data pipeline that processes historical equity prices and evaluates a momentum-based trading strategy.

- Downloads historical price data for 10 equities (AAPL, MSFT, GOOG, AMZN, META, NVDA, TSLA, JPM, UNH, HD)
- Computes a 90-day momentum signal using rolling time-series transformations
- Ranks assets cross-sectionally at each monthly rebalance date
- Constructs an equal-weight portfolio from the top 3 ranked assets
- Simulates portfolio performance over time using event-driven rebalancing logic
- Compares strategy performance against SPY (a broad US stock market benchmark)

The system is structured into three core components:

- **Signal Engine**: Generates momentum signals from time-series price data using vectorized pandas operations
- **Portfolio Builder**: Performs cross-sectional ranking and constructs portfolio weights at each rebalance point
- **Backtest Engine**: Simulates portfolio performance over time using forward-filled weights and return aggregation

Each component operates as a deterministic transformation over pandas DataFrames, improving testability, reproducibility, and making data flow explicit and traceable.

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