import requests
import pandas as pd
import numpy as np
import websockets
import asyncio
import json
import pickle
import time
from collections import deque
from sklearn.preprocessing import MinMaxScaler
from config import TRADING_CONFIG, get_logger  # ✅ Fixed Import

logger = get_logger()
data_buffer = deque(maxlen=1000)

# ✅ Reference SCALER_FILE Correctly
SCALER_FILE = TRADING_CONFIG["SCALER_FILE"]

# ✅ Fetch Historical Data with Caching & Error Handling
def get_historical_data(asset, granularity=300, cache=None):
    """Fetch historical market data with caching and retry logic."""
    if cache is None:
        cache = {}

    if (asset, granularity) in cache:
        return cache[(asset, granularity)]

    url = f"https://api.pro.coinbase.com/products/{asset}-USD/candles?granularity={granularity}"
    max_retries = 3
    retry_delay = 5  # seconds

    for attempt in range(max_retries):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()

            if not data:
                raise ValueError("Received empty historical data.")

            df = pd.DataFrame(data, columns=["time", "low", "high", "open", "close", "volume"])
            df["time"] = pd.to_datetime(df["time"], unit="s")
            df.sort_values("time", inplace=True)

            cache[(asset, granularity)] = df  # Cache data
            return df

        except (requests.RequestException, ValueError) as e:
            logger.error(f"⚠️ Error fetching historical data (Attempt {attempt + 1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
            else:
                return None


# ✅ Preprocess Data & Save Scaler Correctly
def preprocess_data(df):
    """Preprocesses historical price data for AI model training."""
    try:
        if df is None or df.empty:
            raise ValueError("❌ DataFrame is empty or None. Cannot preprocess.")

        df["close"] = pd.to_numeric(df["close"], errors="coerce")

        if df["close"].isnull().any():
            raise ValueError("⚠️ Invalid numerical values detected in 'close' column.")

        scaler = MinMaxScaler()
        scaled_data = scaler.fit_transform(df["close"].values.reshape(-1, 1))

        X, y = [], []
        for i in range(TRADING_CONFIG["LOOKBACK"], len(scaled_data)):
            X.append(scaled_data[i - TRADING_CONFIG["LOOKBACK"]:i])
            y.append(scaled_data[i])

        # ✅ Save Scaler File
        try:
            with open(SCALER_FILE, "wb") as f:
                pickle.dump(scaler, f)
        except Exception as e:
            logger.error(f"⚠️ Failed to save SCALER_FILE: {e}")

        return np.array(X).reshape(-1, TRADING_CONFIG["LOOKBACK"], 1), np.array(y), scaler

    except ValueError as e:
        logger.error(f"❌ Error in data preprocessing: {e}")
        return None, None, None


# ✅ WebSocket for Live Data with Auto-Reconnect
async def fetch_live_data():
    """Fetch live market data using Coinbase WebSocket API with automatic reconnection."""
    while True:
        try:
            async with websockets.connect("wss://ws-feed.pro.coinbase.com") as ws:
                await ws.send(json.dumps({
                    "type": "subscribe",
                    "channels": [{"name": "ticker", "product_ids": ["BTC-USD"]}]
                }))

                while True:
                    response = await ws.recv()
                    data = json.loads(response)

                    if "price" in data:
                        price = float(data["price"])
                        data_buffer.append(price)

        except websockets.exceptions.ConnectionClosed as e:
            logger.warning(f"⚠️ WebSocket disconnected: {e}. Reconnecting in 5 seconds...")
            await asyncio.sleep(5)

        except Exception as e:
            logger.error(f"❌ Unexpected WebSocket error: {e}. Restarting in 5 seconds...")
            await asyncio.sleep(5)


# ✅ Start Live Data Listener in an Async-Safe Way
def start_live_data_listener():
    """Start the live data listener for real-time market updates."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(fetch_live_data())
