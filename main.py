#!/usr/bin/env python3

import threading
import asyncio
import tkinter as tk
from tkinter import ttk, messagebox

from styles import apply_style
from data_handler import get_historical_data, start_live_data_listener
from model import train_or_update_model, predict_price
from genetic_trading import GeneticTradingStrategy, APIManager
from config import get_logger, TRADING_CONFIG

logger = get_logger()

# ✅ Asynchronous Market Data Handling
async def async_market_data():
    """Runs market data listener asynchronously."""
    loop = asyncio.get_event_loop()
    try:
        await loop.run_in_executor(None, start_live_data_listener)
    except Exception as e:
        logger.error(f"Market Data Listener Error: {e}")

class CoinFxGUI:
    def __init__(self, root):
        """Initialize the AI Trading GUI."""
        self.root = root
        self.root.title("CoinFx - AI Trading Bot")
        self.root.geometry("1100x650")
        self.root.configure(bg="#121212")

        self.api_manager = APIManager()
        self.asset_selected = tk.StringVar(value="BTC-USD")
        self.trading_active = False  

        self.setup_ui()
        self.start_background_tasks()

    def start_background_tasks(self):
        """Start market data listener in a background thread."""
        threading.Thread(target=lambda: asyncio.run(async_market_data()), daemon=True).start()

    def setup_ui(self):
        """Set up the GUI with all components."""
        self.tab_control = ttk.Notebook(self.root)
        self.tabs = {
            "Dashboard": ttk.Frame(self.tab_control),
            "AI Model": ttk.Frame(self.tab_control),
            "Genetic Algorithm": ttk.Frame(self.tab_control),
            "Backtesting": ttk.Frame(self.tab_control),
            "Trade Logs": ttk.Frame(self.tab_control),
            "Settings": ttk.Frame(self.tab_control),
        }

        for name, frame in self.tabs.items():
            self.tab_control.add(frame, text=name)
        self.tab_control.pack(expand=1, fill="both")
        self.create_ui_components()

    def create_ui_components(self):
        """Create UI components for each tab."""
        self.create_dashboard()
        self.create_ai_tab()
        self.create_ga_tab()
        self.create_backtesting_tab()
        self.create_logs_tab()
        self.create_settings_tab()

    def create_dashboard(self):
        """Main Trading Dashboard."""
        frame = self.tabs["Dashboard"]
        tk.Label(frame, text="CoinFx Trading Dashboard", font=("Arial", 18, "bold"), bg="#121212", fg="#E0E0E0").pack(pady=10)

        assets = ["BTC-USD", "ETH-USD", "LTC-USD", "XRP-USD", "ADA-USD"]
        self.asset_dropdown = ttk.Combobox(frame, values=assets, textvariable=self.asset_selected)
        self.asset_dropdown.pack(pady=5)

        self.market_data_label = tk.Label(frame, text="Fetching market data...", font=("Arial", 12), bg="#121212", fg="#1DB954")
        self.market_data_label.pack(pady=5)

        self.prediction_label = tk.Label(frame, text="Predicted Price: --", font=("Arial", 12, "bold"), bg="#121212", fg="#E0E0E0")
        self.prediction_label.pack(pady=5)

        self.start_button = tk.Button(frame, text="Start Trading", command=self.start_trading)
        apply_style(self.start_button, "button")
        self.start_button.pack(pady=10)

        self.stop_button = tk.Button(frame, text="Stop Trading", command=self.stop_trading, state=tk.DISABLED)
        apply_style(self.stop_button, "button")
        self.stop_button.pack(pady=10)

    def start_trading(self):
        """Start AI-based trading session."""
        if self.trading_active:
            messagebox.showinfo("Trading Bot", "Trading is already running!")
            return

        self.trading_active = True
        self.update_ui_status("Trading Active", disable_start=True, enable_stop=True)

        threading.Thread(target=self.execute_trading_strategy, daemon=True).start()

    def stop_trading(self):
        """Stop trading session."""
        if not self.trading_active:
            messagebox.showinfo("Trading Bot", "Trading is not active!")
            return

        self.trading_active = False
        self.update_ui_status("Trading Stopped", disable_stop=True, enable_start=True)

    def execute_trading_strategy(self):
        """Run AI trading strategy with Genetic Algorithm Optimization."""
        if not self.trading_active:
            return

        asset = self.asset_selected.get()
        market_data = get_historical_data(asset.split("-")[0])

        if market_data is None:
            messagebox.showerror("Data Error", f"Failed to fetch market data for {asset}!")
            self.trading_active = False
            return

        strategy = GeneticTradingStrategy(market_data)
        best_strategy = strategy.evolve()

        signal = best_strategy[-1]
        logger.info(f"Executing trade with signal: {signal}")
        self.api_manager.execute_trade(asset, signal, "coinbase")

    def create_ai_tab(self):
        """Create AI Model tab."""
        frame = self.tabs["AI Model"]
        tk.Label(frame, text="AI Model Training & Prediction", font=("Arial", 14, "bold"), bg="#121212", fg="#E0E0E0").pack(pady=10)

        self.train_model_button = tk.Button(frame, text="Train Model", command=self.train_ai_model)
        apply_style(self.train_model_button, "button")
        self.train_model_button.pack(pady=10)

    def train_ai_model(self):
        """Train AI model asynchronously."""
        messagebox.showinfo("Training Started", "AI model training is in progress...")
        threading.Thread(target=self.async_train_model, daemon=True).start()

    def async_train_model(self):
        """Train AI model in a separate thread."""
        try:
            train_or_update_model()
            messagebox.showinfo("Training Complete", "AI model training finished!")
        except Exception as e:
            logger.error(f"AI Model training failed: {e}")
            messagebox.showerror("Training Failed", "An error occurred during training.")

    def create_ga_tab(self):
        """Create Genetic Algorithm tab."""
        frame = self.tabs["Genetic Algorithm"]
        tk.Label(frame, text="Genetic Algorithm Optimization", font=("Arial", 14, "bold"), bg="#121212", fg="#E0E0E0").pack(pady=10)

        tk.Button(frame, text="Run Genetic Algorithm", command=lambda: threading.Thread(target=self.execute_trading_strategy, daemon=True).start()).pack(pady=10)

    def create_backtesting_tab(self):
        """Create Backtesting tab."""
        frame = self.tabs["Backtesting"]
        tk.Label(frame, text="Backtesting Trading Strategies", font=("Arial", 14, "bold"), bg="#121212", fg="#E0E0E0").pack(pady=10)

        tk.Button(frame, text="Run Backtest", command=self.run_backtest).pack(pady=10)

    def run_backtest(self):
        """Run backtesting simulation."""
        asset = self.asset_selected.get()
        market_data = get_historical_data(asset.split("-")[0])
        
        if not market_data:
            messagebox.showerror("Backtest Error", "Failed to fetch market data!")
            return

        strategy = GeneticTradingStrategy(market_data)
        results = strategy.backtest()

        messagebox.showinfo("Backtest Complete", f"Backtest Results: {results}")

    def create_logs_tab(self):
        """Create Trade Logs tab."""
        frame = self.tabs["Trade Logs"]
        tk.Label(frame, text="Trade Logs", font=("Arial", 14, "bold"), bg="#121212", fg="#E0E0E0").pack(pady=10)

    def create_settings_tab(self):
        """Create Settings tab."""
        frame = self.tabs["Settings"]
        tk.Label(frame, text="Settings", font=("Arial", 14, "bold"), bg="#121212", fg="#E0E0E0").pack(pady=10)

    def update_ui_status(self, status_text, disable_start=False, enable_start=False, disable_stop=False, enable_stop=False):
        """Thread-safe method to update UI."""
        self.root.after(0, self.market_data_label.config, {"text": f"Status: {status_text}"})
        if disable_start:
            self.start_button.config(state=tk.DISABLED)
        if enable_start:
            self.start_button.config(state=tk.NORMAL)
        if disable_stop:
            self.stop_button.config(state=tk.DISABLED)
        if enable_stop:
            self.stop_button.config(state=tk.NORMAL)

if __name__ == "__main__":
    root = tk.Tk()
    app = CoinFxGUI(root)
    root.mainloop()