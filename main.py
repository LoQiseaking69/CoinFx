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

# Asynchronous Market Data Handling
async def async_market_data():
    loop = asyncio.get_event_loop()
    loop.run_in_executor(None, start_live_data_listener)

# Trading System GUI
class CoinFxGUI:
    def __init__(self, root):
        """Initialize the AI Trading GUI."""
        self.root = root
        self.root.title("CoinFx - AI Trading Bot")
        self.root.geometry("1000x600")
        self.root.configure(bg="#121212")

        self.api_manager = APIManager()
        self.asset_selected = tk.StringVar(value="BTC-USD")

        self.tab_control = ttk.Notebook(root)
        self.tabs = {name: ttk.Frame(self.tab_control) for name in [
            "Dashboard", "AI Model", "Genetic Algorithm", "Backtesting", "Trade Logs", "Settings"
        ]}
        for name, frame in self.tabs.items():
            self.tab_control.add(frame, text=name)
        self.tab_control.pack(expand=1, fill="both")

        self.create_ui_components()
        threading.Thread(target=lambda: asyncio.run(async_market_data()), daemon=True).start()

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

        title_label = tk.Label(frame, text="CoinFx Trading Dashboard", font=("Arial", 16, "bold"), bg="#121212", fg="#E0E0E0")
        title_label.pack(pady=10)

        self.asset_dropdown = ttk.Combobox(frame, values=["BTC-USD", "ETH-USD", "LTC-USD"], textvariable=self.asset_selected)
        self.asset_dropdown.pack(pady=5)

        self.market_data_label = tk.Label(frame, text="Fetching live market data...", font=("Arial", 12), bg="#121212", fg="#1DB954")
        self.market_data_label.pack(pady=5)

        self.prediction_label = tk.Label(frame, text="Predicted Price: --", font=("Arial", 12, "bold"), bg="#121212", fg="#E0E0E0")
        self.prediction_label.pack(pady=5)

        self.start_button = tk.Button(frame, text="Start Trading", command=self.start_trading)
        apply_style(self.start_button, "button")
        self.start_button.pack(pady=10)

        self.stop_button = tk.Button(frame, text="Stop Trading", command=self.stop_trading)
        apply_style(self.stop_button, "button")
        self.stop_button.pack(pady=10)

    def start_trading(self):
        """Start AI-based trading session."""
        messagebox.showinfo("Trading Started", "AI Trading Bot is now active!")
        threading.Thread(target=self.execute_trading_strategy, daemon=True).start()

    def stop_trading(self):
        """Stop trading session."""
        messagebox.showwarning("Trading Stopped", "Trading Bot has been halted.")

    def execute_trading_strategy(self):
        """Run the AI trading strategy using Genetic Algorithm Optimization."""
        asset = self.asset_selected.get()
        market_data = get_historical_data(asset.split("-")[0])
        if market_data is None:
            messagebox.showerror("Data Error", f"Failed to fetch market data for {asset}!")
            return

        strategy = GeneticTradingStrategy(market_data)
        best_strategy = strategy.evolve()

        signal = best_strategy[-1]
        self.api_manager.execute_trade(asset, signal, "coinbase")

    def predict_price(self):
        """Predict the next price using the trained AI model."""
        predicted_price = predict_price()
        if predicted_price is not None:
            self.prediction_label.config(text=f"Predicted Price: {predicted_price:.2f}")
        else:
            self.prediction_label.config(text="Predicted Price: Unavailable")

if __name__ == "__main__":
    root = tk.Tk()
    app = CoinFxGUI(root)
    root.mainloop()