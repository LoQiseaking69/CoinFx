# CoinFx
# Genetic Algorithm Trading Bot

This project implements an **automated trading system** using a **Genetic Algorithm (GA)** to optimize trading strategies. It supports **live trading** on **OANDA (forex) and Coinbase (crypto)**, as well as **backtesting** on historical market data.

## Features
- **Genetic Algorithm Optimization:** Evolves trading strategies over multiple generations.
- **Backtesting Engine:** Simulates trading performance and calculates key metrics:
  - Final Capital
  - Sharpe Ratio
  - Max Drawdown
  - Profit Factor
- **Live Trading Execution:** Supports real-time trade execution on:
  - **OANDA (Forex)**
  - **Coinbase (Crypto)**
- **Adaptive Strategy Types:**
  - **Binary Signals:** Buy/Sell only.
  - **Continuous Signals:** Buy/Sell with position sizing.
  - **Multi-Class Signals:** Hold/Buy/Sell.

## Installation

### 1. Clone the Repository
```sh
git clone https://github.com/LoQiseaking69/CoinFx.git
cd genetic-trading-bot
```

### 2. Install Dependencies
Ensure you have **Python 3.8+** and install required packages:
```sh
pip install numpy oandapyV20 cbpro
```

### 3. Set Up API Credentials
Create a `.env` file and add your **OANDA** and **Coinbase API credentials**:
```
OANDA_ACCESS_TOKEN=your_oanda_access_token
OANDA_ACCOUNT_ID=your_oanda_account_id
COINBASE_API_KEY=your_coinbase_api_key
COINBASE_API_SECRET=your_coinbase_api_secret
```
Then, load the environment variables:
```sh
export $(grep -v '^#' .env | xargs)
```

## Usage

### 1. Running a Backtest
Load historical **market data** into a Python list and run a backtest:
```python
from genetic_trading import GeneticTradingStrategy

market_data = [...]  # Load real market data
strategy = GeneticTradingStrategy(market_data)
best_strategy = strategy.evolve()

print("Optimized Strategy:", best_strategy)
```

### 2. Executing a Live Trade
Once the strategy is optimized, execute a trade using the last signal:
```python
from genetic_trading import APIManager

api_manager = APIManager()
signal = best_strategy[-1]  # Last trade signal from GA
api_manager.execute_trade("BTC-USD", signal, "coinbase")  # Or use "oanda"
```

## Code Overview

### **1. APIManager (Live Trading)**
Handles authentication and trade execution for **OANDA** and **Coinbase**.
```python
class APIManager:
    def __init__(self):
        self.oanda_client = self._initialize_oanda_client()
        self.coinbase_client = self._initialize_coinbase_client()
```
- **`execute_trade(symbol, signal, platform)`** â Places a market order.

### **2. TradeSimulator (Backtesting)**
Simulates trading on historical data and calculates **performance metrics**.
```python
class TradeSimulator:
    def backtest(self, chromosome):
        # Evaluates strategy performance
```
- **`backtest(chromosome)`** â Runs a simulation and returns:
  - `final_capital`
  - `sharpe_ratio`
  - `max_drawdown`
  - `profit_factor`

### **3. GeneticTradingStrategy (GA Optimization)**
Uses a **genetic algorithm** to find the best trading strategy.
```python
class GeneticTradingStrategy:
    def evolve(self):
        # Evolves trading strategies over generations
```
- **`_select_parents()`** â Selects the best strategies.
- **`_crossover(parent1, parent2)`** â Mixes strategies.
- **`_mutate(chromosome)`** â Introduces random mutations.
- **`evolve()`** â Runs the GA for **200 generations**.

## Performance Metrics

| Metric         | Description                                    |
|---------------|--------------------------------|
| **Final Capital** | Money left after backtesting |
| **Sharpe Ratio**  | Risk-adjusted return         |
| **Max Drawdown**  | Largest peak-to-trough loss  |
| **Profit Factor** | Total gains / total losses  |

## Roadmap
- [ ] Add **risk management** (stop-loss & position sizing).
- [ ] Implement **web dashboard** for real-time monitoring.
- [ ] Support **Binance & Kraken APIs**.

## Disclaimer
â  **This is an experimental trading bot. Use at your own risk.** Always backtest thoroughly before deploying to real markets.

---
