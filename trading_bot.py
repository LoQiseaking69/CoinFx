import threading
import time
import tkinter as tk
from tkinter import messagebox
from model import predict_price
from config import get_logger
from data_handler import start_live_data_listener

logger = get_logger()

class TradingBotGUI:
    def __init__(self, root):
        """Initialize the GUI and bot settings."""
        self.root = root
        self.root.title("Trading Dashboard")
        self.root.geometry("800x500")
        self.trading_active = False
        self.trade_thread = None

        # UI Elements
        self.start_button = tk.Button(root, text="Start Trading", command=self.start_trading)
        self.start_button.pack(pady=10)

        self.stop_button = tk.Button(root, text="Stop Trading", command=self.stop_trading)
        self.stop_button.pack(pady=10)

        self.status_label = tk.Label(root, text="Status: Idle", font=("Arial", 12))
        self.status_label.pack(pady=10)

    def start_trading(self):
        """Start trading in a separate thread."""
        if not self.trading_active:
            self.trading_active = True
            self.trade_thread = threading.Thread(target=self.execute_trades, daemon=True)
            self.trade_thread.start()
            self.status_label.config(text="Status: Trading Active")
            messagebox.showinfo("Trading Bot", "Trading Started.")

    def execute_trades(self):
        """Continuously execute trades while trading is active."""
        while self.trading_active:
            try:
                prediction = predict_price()
                if prediction is not None:
                    logger.info(f"Predicted Price: {prediction}")
                else:
                    logger.warning("Prediction returned None. Skipping trade cycle.")
                
                time.sleep(5)

            except Exception as e:
                logger.error(f"Error during trade execution: {e}")
                self.status_label.config(text="Status: Error")

    def stop_trading(self):
        """Stop the trading process."""
        self.trading_active = False
        self.status_label.config(text="Status: Stopped")
        messagebox.showinfo("Trading Bot", "Trading Stopped.")

if __name__ == "__main__":
    root = tk.Tk()
    app = TradingBotGUI(root)
    root.mainloop()