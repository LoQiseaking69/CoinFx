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
        self.root = root
        self.root.title("Trading Dashboard")
        self.root.geometry("800x500")
        self.trading_active = False
        self.trade_thread = None

        # UI Elements
        self.start_button = tk.Button(root, text="Start Trading", command=self.start_trading)
        self.start_button.pack(pady=10)

        self.stop_button = tk.Button(root, text="Stop Trading", command=self.stop_trading, state=tk.DISABLED)
        self.stop_button.pack(pady=10)

        self.status_label = tk.Label(root, text="Status: Idle", font=("Arial", 12))
        self.status_label.pack(pady=10)

        self.prediction_label = tk.Label(root, text="Predicted Price: -- ± --", font=("Arial", 12))
        self.prediction_label.pack(pady=10)

        threading.Thread(target=start_live_data_listener, daemon=True).start()

    def start_trading(self):
        if not self.trading_active:
            self.trading_active = True
            self.trade_thread = threading.Thread(target=self.execute_trades, daemon=True)
            self.trade_thread.start()
            self.root.after(0, self.update_status, "Trading Active")
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            messagebox.showinfo("Trading Bot", "Trading Started.")

    def execute_trades(self):
        while self.trading_active:
            try:
                prediction = predict_price()
                if prediction and isinstance(prediction, dict):
                    price = round(prediction['price'], 2)
                    std = round(prediction['std'], 2)
                    self.root.after(0, self.prediction_label.config, {"text": f"Predicted Price: {price} ± {std}"})
                    logger.info(f"Predicted Price: {price} ± {std}")
                else:
                    logger.warning("Prediction returned None. Skipping trade cycle.")
                time.sleep(5)
            except Exception as e:
                logger.error(f"Error during trade execution: {e}")
                self.root.after(0, self.update_status, "Error")
                self.trading_active = False
                break

    def stop_trading(self):
        self.trading_active = False
        self.root.after(0, self.update_status, "Stopped")
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        messagebox.showinfo("Trading Bot", "Trading Stopped.")

    def update_status(self, status_text):
        self.status_label.config(text=f"Status: {status_text}")

if __name__ == "__main__":
    root = tk.Tk()
    app = TradingBotGUI(root)
    root.mainloop()