# 🚀 **CoinFx: AI-Powered Genetic Algorithm Trading Bot**
**CoinFx** is an **AI-driven, fully automated trading system** that integrates **Genetic Algorithm (GA) optimization** with **LSTM-based AI prediction** to maximize trading efficiency. It supports **real-time trading**, **backtesting**, and **performance analytics** on both **OANDA (Forex)** and **Coinbase (Crypto)**.

---

## 🌟 **Key Features**
✔ **Hybrid AI & Genetic Algorithm** – Combines **LSTM-based AI predictions** with **GA-driven trading strategies**.  
✔ **Live Trading Execution** – Supports real-time trading on:  
   - **OANDA (Forex)**  
   - **Coinbase (Crypto)**  
✔ **Backtesting Engine** – Evaluates strategy performance using key metrics:  
   - **Final Capital**  
   - **Sharpe Ratio** (Risk-Adjusted Return)  
   - **Max Drawdown** (Worst Peak-to-Trough Loss)  
   - **Profit Factor** (Total Gains / Total Losses)  
✔ **Risk & Performance Management** – Implements **stop-loss, take-profit, position sizing, and cooldown periods**.  
✔ **Adaptive Trading Strategies** – Supports multiple decision models:  
   - **Binary Signals** – Buy/Sell only.  
   - **Continuous Signals** – Buy/Sell with position sizing.  
   - **Multi-Class Signals** – Hold/Buy/Sell.  
✔ **Modular & Scalable Architecture** – Designed for **Docker-based deployment** and **automated CI/CD integration**.  

---

## 📌 **Installation Guide**
### 1️⃣ **Clone the Repository**
```sh
git clone https://github.com/LoQiseaking69/CoinFx.git
cd CoinFx
```

### 2️⃣ **Install Docker**
Ensure **Docker** is installed:
```sh
sudo apt update && sudo apt install docker.io -y
```
Verify installation:
```sh
docker --version
```

### 3️⃣ **Build & Run the Bot in a Container**
```sh
docker build -t coinfx-trading-bot .
docker run --rm -it --name coinfx-trading-bot coinfx-trading-bot
```

---

## 📌 **One-Command Execution (`fxcbot`)**
After installation, **run the bot anywhere** with:
```sh
fxcbot
```

✅ **The bot will automatically launch inside Docker.**

---

## 🚀 **Automated Deployment with GitHub Actions**
Each push to **GitHub** triggers an **automated build & deployment**.

### 📌 **Setup GitHub Actions**
1️⃣ Navigate to `.github/workflows/`  
2️⃣ Create `deploy.yml`:
```sh
mkdir -p .github/workflows
nano .github/workflows/deploy.yml
```
3️⃣ Paste this **GitHub Actions CI/CD** workflow:

```yaml
name: Deploy CoinFx Trading Bot with Docker

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]
  workflow_dispatch:

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
      - name: 🛠️ Checkout Repository
        uses: actions/checkout@v4

      - name: 🐳 Install Docker
        run: |
          sudo apt update
          sudo apt install -y docker.io

      - name: 🔧 Build Docker Image
        run: |
          docker build -t coinfx-trading-bot .

      - name: 🚀 Create Executable for Linux
        run: |
          echo "#!/bin/bash" > fxcbot
          echo "docker run --rm -it --name coinfx-trading-bot coinfx-trading-bot "\$@"" >> fxcbot
          chmod +x fxcbot
          sudo mv fxcbot /usr/local/bin/

      - name: ✅ Verify Installation
        run: |
          which fxcbot
          fxcbot --help || echo "Bot is installed successfully!"
```

### 📌 **Push & Deploy**
```sh
git add .github/workflows/deploy.yml
git commit -m "Added Docker-based GitHub Actions deployment"
git push origin main
```
Now, the bot will **automatically rebuild** when you push updates to GitHub. ✅  

---

## 📊 **Performance Metrics**
| Metric           | Description                                    |
|-----------------|--------------------------------|
| **Final Capital** | Money left after backtesting |
| **Sharpe Ratio**  | Risk-adjusted return         |
| **Max Drawdown**  | Largest peak-to-trough loss  |
| **Profit Factor** | Total gains / total losses  |

---

## 🛡 **Risk Management Features**
✅ **Stop-Loss** – Automatically exits losing trades to protect capital.  
✅ **Take-Profit** – Locks in gains by closing profitable trades.  
✅ **Position Sizing** – Dynamically adjusts trade sizes based on market conditions.  
✅ **Cooldown Periods** – Prevents excessive trading in volatile markets.  

---

## 🚀 **Quick Start Summary**
| **Task** | **Command** |
|----------|------------|
| **Clone the repository** | `git clone https://github.com/LoQiseaking69/CoinFx.git && cd CoinFx` |
| **Install Docker** | `sudo apt update && sudo apt install docker.io -y` |
| **Build the Docker image** | `docker build -t coinfx-trading-bot .` |
| **Run the bot inside Docker** | `docker run --rm -it --name coinfx-trading-bot coinfx-trading-bot` |
| **Make `fxcbot` command globally available** | `echo "docker run --rm -it --name coinfx-trading-bot coinfx-trading-bot" > fxcbot && chmod +x fxcbot && sudo mv fxcbot /usr/local/bin/` |
| **Run the bot from anywhere** | `fxcbot` |

---

## ⚠ **Disclaimer**
🚨 **This is an experimental trading bot. Use at your own risk.**  
📉 **There are NO guarantees of profit.** Always backtest strategies thoroughly before deploying to real markets.

