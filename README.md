# **CoinFx**
## **AI-Powered Genetic Algorithm Trading Bot**

**CoinFx** is a **fully automated trading system** that integrates **Genetic Algorithm (GA) optimization** and **LSTM-based AI prediction** to maximize trading performance. It supports **live trading** on **OANDA (Forex) and Coinbase (Crypto)** while also offering **backtesting and real-time market analysis**.

---

## **🚀 Features**
✔ **Hybrid AI & Genetic Algorithm** – Uses **AI price prediction** combined with **GA strategy evolution**.  
✔ **Live Trading Execution** – Supports real-time trading on:  
   - **OANDA (Forex)**  
   - **Coinbase (Crypto)**  
✔ **Backtesting Engine** – Simulates trading performance and calculates key metrics:  
   - **Final Capital**  
   - **Sharpe Ratio**  
   - **Max Drawdown**  
   - **Profit Factor**  
✔ **Risk & Performance Management** – Implements **stop-loss, take-profit, and position sizing**.  
✔ **Adaptive Trading Strategies** – Supports multiple trading signals:  
   - **Binary Signals** – Buy/Sell only.  
   - **Continuous Signals** – Buy/Sell with position sizing.  
   - **Multi-Class Signals** – Hold/Buy/Sell.  
✔ **Modular & Scalable Architecture** – Designed for **cloud deployment** and **high-frequency trading**.  

---

## **📌 Installation**

### **1️⃣ Clone the Repository**
```sh
git clone https://github.com/LoQiseaking69/CoinFx.git
cd CoinFx
```

### **2️⃣ Install Dependencies**
Ensure you have **Python 3.8+** and install the required packages:
```sh
pip install -r requirements.txt
```

### **3️⃣ Set Up API Credentials**
Create a `.env` file and add your **OANDA** and **Coinbase API credentials**:
```ini
OANDA_ACCESS_TOKEN=your_oanda_access_token
OANDA_ACCOUNT_ID=your_oanda_account_id
COINBASE_API_KEY=your_coinbase_api_key
COINBASE_API_SECRET=your_coinbase_api_secret
```
Then, load the environment variables:
```sh
export $(grep -v '^#' .env | xargs)
```

---

## **🛠 Unit Testing & Debugging**

### **1️⃣ Test API Configuration**
Run this script to check if API keys are correctly loaded:
```python
from config import validate_config

try:
    validate_config()
    print("✅ API configuration is valid.")
except Exception as e:
    print(f"❌ Config Error: {e}")
```

### **2️⃣ Test Data Handling (Historical Data & WebSocket)**
```python
from data_handler import get_historical_data, start_live_data_listener
import threading

df = get_historical_data("BTC")
if df is not None and not df.empty:
    print("✅ Historical data fetched successfully.")
else:
    print("❌ Historical data fetch failed.")

# Start live data feed
threading.Thread(target=start_live_data_listener, daemon=True).start()
print("✅ Live data listener started.")
```

### **3️⃣ Test Model Training & Prediction**
```python
from model import train_or_update_model, predict_price

train_or_update_model()
print("✅ Model trained successfully.")

prediction = predict_price()
if prediction:
    print(f"✅ Model prediction successful: {prediction}")
else:
    print("❌ Model prediction failed.")
```

### **4️⃣ Test Trading Execution**
```python
from trading_bot import TradingBotGUI
import tkinter as tk

root = tk.Tk()
app = TradingBotGUI(root)
root.mainloop()
```

Check **log files** for errors:
```sh
tail -f logs/trading.log
```

---

## **🚀 Deployment Plan**

### **1️⃣ Choose Deployment Type**
✅ **Local Machine (Development Mode)** – Run manually on your computer.  
✅ **Cloud Deployment (Production Mode)** – Deploy on **AWS, GCP, or DigitalOcean** for **24/7 trading**.  

### **2️⃣ Deploy on AWS EC2 (Example)**
#### **Step 1: Set Up EC2**
1️⃣ Launch an **Ubuntu 22.04 EC2 instance**.  
2️⃣ SSH into the instance:
```sh
ssh -i your-key.pem ubuntu@your-server-ip
```
3️⃣ Install Python and dependencies:
```sh
sudo apt update && sudo apt install python3-pip -y
pip3 install -r requirements.txt
```
4️⃣ Set up API credentials:
```sh
nano .env
```
Add:
```ini
OANDA_ACCESS_TOKEN=your_oanda_access_token
OANDA_ACCOUNT_ID=your_oanda_account_id
COINBASE_API_KEY=your_coinbase_api_key
COINBASE_API_SECRET=your_coinbase_api_secret
```

#### **Step 2: Start the Bot**
Run in **background mode**:
```sh
nohup python3 trading_bot.py &
```
Check logs:
```sh
tail -f logs/trading.log
```

---

## **📜 Code Overview**
### **1️⃣ APIManager (Live Trading)**
Handles authentication and trade execution for **OANDA** and **Coinbase**.
```python
class APIManager:
    def __init__(self):
        self.oanda_client = self._initialize_oanda_client()
        self.coinbase_client = self._initialize_coinbase_client()
```
- **`execute_trade(symbol, signal, platform)`** – Places a market order.

### **2️⃣ TradeSimulator (Backtesting)**
Simulates trading on historical data and calculates **performance metrics**.
```python
class TradeSimulator:
    def backtest(self, chromosome):
        # Evaluates strategy performance
```
- **`backtest(chromosome)`** – Runs a simulation and returns:
  - `final_capital`
  - `sharpe_ratio`
  - `max_drawdown`
  - `profit_factor`

### **3️⃣ GeneticTradingStrategy (GA Optimization)**
Uses a **genetic algorithm** to find the best trading strategy.
```python
class GeneticTradingStrategy:
    def evolve(self):
        # Evolves trading strategies over generations
```
- **`_select_parents()`** – Selects the best strategies.  
- **`_crossover(parent1, parent2)`** – Mixes strategies.  
- **`_mutate(chromosome)`** – Introduces random mutations.  
- **`evolve()`** – Runs the GA for **200 generations**.  

---

## **📊 Performance Metrics**
| Metric           | Description                                    |
|-----------------|--------------------------------|
| **Final Capital** | Money left after backtesting |
| **Sharpe Ratio**  | Risk-adjusted return         |
| **Max Drawdown**  | Largest peak-to-trough loss  |
| **Profit Factor** | Total gains / total losses  |

---

## **🛡 Risk Management**
✅ **Stop-Loss** – Automatically cuts losses at pre-set thresholds.  
✅ **Take-Profit** – Locks in gains at profitable price points.  
✅ **Position Sizing** – Adjusts trade sizes based on market conditions.  
✅ **Cooldown Periods** – Prevents overtrading in volatile markets.  

---

## **⚠ Disclaimer**
🚨 **This is an experimental trading bot. Use at your own risk.**  
📉 **There are NO guarantees of profit.** Always backtest strategies thoroughly before deploying to real markets.  

---