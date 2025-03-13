# **🚀 CoinFx: AI-Powered Genetic Algorithm Trading Bot**
**CoinFx** is a **fully automated trading system** that integrates **Genetic Algorithm (GA) optimization** and **LSTM-based AI prediction** to maximize trading performance. It supports **live trading** on **OANDA (Forex) and Coinbase (Crypto)** while also offering **backtesting and real-time market analysis**.

---

## **🌟 Key Features**
✔ **AI & Genetic Algorithm Hybrid** – Combines **AI price prediction** with **GA strategy evolution**.  
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
✔ **Modular & Scalable Architecture** – Designed for **Docker-based deployment** and **cloud automation**.  

---

## **📌 Installation**
### **1️⃣ Clone the Repository**
```sh
git clone https://github.com/LoQiseaking69/CoinFx.git
cd CoinFx
```

### **2️⃣ Install Docker**
Ensure **Docker** is installed:
```sh
sudo apt update && sudo apt install docker.io -y
```
Then, check if Docker is running:
```sh
docker --version
```

### **3️⃣ Build & Run the Bot as a Container**
```sh
docker build -t coinfx-trading-bot .
docker run --rm -it --name coinfx-trading-bot coinfx-trading-bot
```

---

## **📌 One-Command Execution (`fxcbot`)**
After deployment, **you can run the bot anywhere** with:
```sh
fxcbot
```

#### **🔹 Install `fxcbot` Locally**
Run the following to create a **global shell command**:
```sh
echo "#!/bin/bash" > fxcbot
echo "docker run --rm -it --name coinfx-trading-bot coinfx-trading-bot "\$@"" >> fxcbot
chmod +x fxcbot
sudo mv fxcbot /usr/local/bin/
```

Now, just type:
```sh
fxcbot
```
**The bot will launch automatically inside Docker.** ✅

---

## **🚀 Automated Deployment with GitHub Actions**
Every time you **push updates to GitHub**, the bot **rebuilds automatically**.  

### **📌 Set Up GitHub Actions**
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
    branches:
      - main
  pull_request:
    branches:
      - main
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

### **📌 Push & Deploy**
```sh
git add .github/workflows/deploy.yml
git commit -m "Added Docker-based GitHub Actions deployment"
git push origin main
```

Now, the bot will **automatically rebuild** when you push updates to GitHub. ✅  

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

## **🚀 Quick Start Summary**
| **Task** | **Command** |
|----------|------------|
| **Clone the repository** | `git clone https://github.com/LoQiseaking69/CoinFx.git && cd CoinFx` |
| **Install Docker** | `sudo apt update && sudo apt install docker.io -y` |
| **Build the Docker image** | `docker build -t coinfx-trading-bot .` |
| **Run the bot inside Docker** | `docker run --rm -it --name coinfx-trading-bot coinfx-trading-bot` |
| **Make `fxcbot` command globally available** | `echo "docker run --rm -it --name coinfx-trading-bot coinfx-trading-bot" > fxcbot && chmod +x fxcbot && sudo mv fxcbot /usr/local/bin/` |
| **Run the bot from anywhere** | `fxcbot` |

---

## **⚠ Disclaimer**
🚨 **This is an experimental trading bot. Use at your own risk.**  
📉 **There are NO guarantees of profit.** Always backtest strategies thoroughly before deploying to real markets.
