# main.py - Sophisticated GUI for CoinFx AI Trading System with Optional Coinbase Support

import threading
import tkinter as tk
from tkinter import ttk, messagebox
from styles import apply_style
from data_handler import get_historical_data, start_live_data_listener
from model import train_or_update_model, predict_price
from genetic_trading import GeneticTradingStrategy
from config import get_logger

# Optional Coinbase API Import
try:
    from config import COINBASE_API_KEY, COINBASE_API_SECRET, COINBASE_API_PASSPHRASE
    coinbase_enabled = bool(COINBASE_API_KEY and COINBASE_API_SECRET and COINBASE_API_PASSPHRASE)
except ImportError:
    coinbase_enabled = False

# Ask user if they want to disable Coinbase at runtime
if coinbase_enabled:
    use_coinbase = messagebox.askyesno("Coinbase API", "Would you like to enable Coinbase trading?")
    if not use_coinbase:
        coinbase_enabled = False
else:
    messagebox.showinfo("Coinbase API", "Coinbase API is not configured. Running with OANDA only.")

logger = get_logger()

class CoinFxGUI:
    def __init__(self, root):
        """Initialize the sophisticated trading GUI with tabs."""
        self.root = root
        self.root.title("CoinFx - AI Trading Bot")
        self.root.geometry("1000x600")
        self.root.configure(bg="#121212")

        # Tab Control
        self.tab_control = ttk.Notebook(root)

        # Create Tabs
        self.dashboard_tab = ttk.Frame(self.tab_control)
        self.ai_tab = ttk.Frame(self.tab_control)
        self.ga_tab = ttk.Frame(self.tab_control)
        self.backtest_tab = ttk.Frame(self.tab_control)
        self.logs_tab = ttk.Frame(self.tab_control)
        self.settings_tab = ttk.Frame(self.tab_control)

        # Add Tabs
        self.tab_control.add(self.dashboard_tab, text="📊 Dashboard")
        self.tab_control.add(self.ai_tab, text="🤖 AI Model")
        self.tab_control.add(self.ga_tab, text="🧬 Genetic Algorithm")
        self.tab_control.add(self.backtest_tab, text="📈 Backtesting")
        self.tab_control.add(self.logs_tab, text="📜 Trade Logs & Risk Management")
        self.tab_control.add(self.settings_tab, text="⚙ Settings")

        self.tab_control.pack(expand=1, fill="both")

        # Initialize UI Components in Tabs
        self.create_dashboard()
        self.create_ai_tab()
        self.create_ga_tab()
        self.create_backtesting_tab()
        self.create_logs_tab()
        self.create_settings_tab()

        # Start WebSocket for live market data
        threading.Thread(target=start_live_data_listener, daemon=True).start()

    ## 📌 DASHBOARD TAB
    def create_dashboard(self):
        """Main Trading Dashboard - Live Market Data & AI Predictions"""
        title_label = tk.Label(self.dashboard_tab, text="CoinFx Trading Dashboard", font=("Arial", 16, "bold"), bg="#121212", fg="#E0E0E0")
        title_label.pack(pady=10)

        self.market_data_label = tk.Label(self.dashboard_tab, text="Fetching live market data...", font=("Arial", 12), bg="#121212", fg="#1DB954")
        self.market_data_label.pack(pady=5)

        self.prediction_label = tk.Label(self.dashboard_tab, text="Predicted Price: --", font=("Arial", 12, "bold"), bg="#121212", fg="#E0E0E0")
        self.prediction_label.pack(pady=5)

        self.start_button = tk.Button(self.dashboard_tab, text="Start Trading", command=self.start_trading)
        apply_style(self.start_button, "button")
        self.start_button.pack(pady=10)

        self.stop_button = tk.Button(self.dashboard_tab, text="Stop Trading", command=self.stop_trading)
        apply_style(self.stop_button, "button")
        self.stop_button.pack(pady=10)

    ## 📌 AI MODEL TAB
    def create_ai_tab(self):
        """AI Model Training & Prediction"""
        title_label = tk.Label(self.ai_tab, text="AI Trading Model", font=("Arial", 16, "bold"), bg="#121212", fg="#E0E0E0")
        title_label.pack(pady=10)

        self.train_button = tk.Button(self.ai_tab, text="Train AI Model", command=train_or_update_model)
        apply_style(self.train_button, "button")
        self.train_button.pack(pady=10)

        self.predict_button = tk.Button(self.ai_tab, text="Predict Next Price", command=self.predict_price)
        apply_style(self.predict_button, "button")
        self.predict_button.pack(pady=10)

    ## 📌 GENETIC ALGORITHM TAB
    def create_ga_tab(self):
        """Genetic Algorithm Trading Strategy Optimization"""
        title_label = tk.Label(self.ga_tab, text="Genetic Algorithm Optimization", font=("Arial", 16, "bold"), bg="#121212", fg="#E0E0E0")
        title_label.pack(pady=10)

        self.optimize_button = tk.Button(self.ga_tab, text="Optimize Trading Strategy", command=self.run_ga)
        apply_style(self.optimize_button, "button")
        self.optimize_button.pack(pady=10)

    ## 📌 BACKTESTING TAB
    def create_backtesting_tab(self):
        """Run Backtesting on Historical Data"""
        title_label = tk.Label(self.backtest_tab, text="Backtesting Engine", font=("Arial", 16, "bold"), bg="#121212", fg="#E0E0E0")
        title_label.pack(pady=10)

        self.backtest_button = tk.Button(self.backtest_tab, text="Run Backtest", command=self.run_backtest)
        apply_style(self.backtest_button, "button")
        self.backtest_button.pack(pady=10)

    ## 📌 TRADE LOGS & RISK MANAGEMENT TAB
    def create_logs_tab(self):
        """View Trade Logs & Configure Risk Management"""
        title_label = tk.Label(self.logs_tab, text="Trade Logs & Risk Management", font=("Arial", 16, "bold"), bg="#121212", fg="#E0E0E0")
        title_label.pack(pady=10)

        self.view_logs_button = tk.Button(self.logs_tab, text="View Trade Logs", command=self.view_trade_logs)
        apply_style(self.view_logs_button, "button")
        self.view_logs_button.pack(pady=10)

    ## 📌 SETTINGS TAB
    def create_settings_tab(self):
        """Manage API Keys, UI Preferences, Logging Configuration"""
        title_label = tk.Label(self.settings_tab, text="System Settings", font=("Arial", 16, "bold"), bg="#121212", fg="#E0E0E0")
        title_label.pack(pady=10)

        self.api_key_button = tk.Button(self.settings_tab, text="Update API Keys", command=self.update_api_keys)
        apply_style(self.api_key_button, "button")
        self.api_key_button.pack(pady=10)

# Run the GUI
if __name__ == "__main__":
    root = tk.Tk()
    app = CoinFxGUI(root)
    root.mainloop()