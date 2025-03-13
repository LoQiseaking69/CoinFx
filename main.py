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

# ✅ Asynchronous Market Data Handling with Exception Handling
async def async_market_data():
    """Runs market data listener asynchronously."""
    loop = asyncio.get_event_loop()
    try:
        loop.run_in_executor(None, start_live_data_listener)
    except Exception as e:
        logger.error(f"Error in market data listener: {e}")

# ✅ Improved Trading System GUI
class CoinFxGUI:
    def __init__(self, root):
        """Initialize the AI Trading GUI."""
        self.root = root
        self.root.title("CoinFx - AI Trading Bot")
        self.root.geometry("1100x650")
        self.root.configure(bg="#121212")

        self.api_manager = APIManager()
        self.asset_selected = tk.StringVar(value="BTC-USD")
        self.trading_active = False  # New flag for better trading control

        self.setup_ui()
        self.market_data_thread = threading.Thread(target=lambda: asyncio.run(async_market_data()), daemon=True)
        self.market_data_thread.start()

    def setup_ui(self):
        """Set up the main GUI with all components."""
        self.tab_control = ttk.Notebook(self.root)
        self.tabs = {name: ttk.Frame(self.tab_control) for name in [
            "Dashboard", "AI Model", "Genetic Algorithm", "Backtesting", "Trade Logs", "Settings"
        ]}
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

        title_label = tk.Label(frame, text="CoinFx Trading Dashboard", font=("Arial", 18, "bold"), bg="#121212", fg="#E0E0E0")
        title_label.pack(pady=10)

        # ✅ Asset Selection Dropdown (Now Dynamic)
        assets = ["BTC-USD", "ETH-USD", "LTC-USD", "XRP-USD", "ADA-USD"]
        self.asset_dropdown = ttk.Combobox(frame, values=assets, textvariable=self.asset_selected)
        self.asset_dropdown.pack(pady=5)

        # ✅ Live Market Data Display
        self.market_data_label = tk.Label(frame, text="Fetching market data...", font=("Arial", 12), bg="#121212", fg="#1DB954")
        self.market_data_label.pack(pady=5)

        # ✅ AI Predicted Price Display
        self.prediction_label = tk.Label(frame, text="Predicted Price: --", font=("Arial", 12, "bold"), bg="#121212", fg="#E0E0E0")
        self.prediction_label.pack(pady=5)

        # ✅ Start Trading Button
        self.start_button = tk.Button(frame, text="Start Trading", command=self.start_trading)
        apply_style(self.start_button, "button")
        self.start_button.pack(pady=10)

        # ✅ Stop Trading Button
        self.stop_button = tk.Button(frame, text="Stop Trading", command=self.stop_trading)
        apply_style(self.stop_button, "button")
        self.stop_button.pack(pady=10)

    def start_trading(self):
        """Start AI-based trading session with checks."""
        if self.trading_active:
            messagebox.showinfo("Trading Bot", "Trading is already running!")
            return

        self.trading_active = True
        messagebox.showinfo("Trading Started", "AI Trading Bot is now active!")
        threading.Thread(target=self.execute_trading_strategy, daemon=True).start()

    def stop_trading(self):
        """Stop trading session with confirmation."""
        if not self.trading_active:
            messagebox.showinfo("Trading Bot", "Trading is not active!")
            return

        self.trading_active = False
        messagebox.showwarning("Trading Stopped", "Trading Bot has been halted.")

    def execute_trading_strategy(self):
        """Run the AI trading strategy using Genetic Algorithm Optimization."""
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

    def predict_price(self):
        """Predict the next price using the trained AI model."""
        try:
            predicted_price = predict_price()
            if predicted_price is not None:
                self.prediction_label.config(text=f"Predicted Price: {predicted_price:.2f}")
            else:
                self.prediction_label.config(text="Predicted Price: Unavailable")
        except Exception as e:
            logger.error(f"Prediction error: {e}")
            self.prediction_label.config(text="Prediction Error")

    def create_ai_tab(self):
        """Create AI Model tab."""
        frame = self.tabs["AI Model"]
        label = tk.Label(frame, text="AI Model Training & Prediction", font=("Arial", 14, "bold"), bg="#121212", fg="#E0E0E0")
        label.pack(pady=10)

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

if __name__ == "__main__":
    root = tk.Tk()
    app = CoinFxGUI(root)
    root.mainloop()