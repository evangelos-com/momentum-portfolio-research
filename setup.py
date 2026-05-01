# setup.py
from setuptools import setup, find_packages

setup(
    name="momentum-portfolio-research",
    version="1.0.0",
    description="Momentum-based portfolio backtest strategy",
    author="Evangelos",
    packages=find_packages(),
    install_requires=[
        "pandas>=3.0.0",
        "numpy>=2.0.0",
        "yfinance>=1.3.0",
        "matplotlib>=3.9.0",
    ],
    python_requires=">=3.9",
)