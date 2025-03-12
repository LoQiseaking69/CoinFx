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
from config import API_URL, LOOKBACK, SCALER_FILE, get_logger

logger = get_logger()
data_buffer = deque(maxlen=1000)

# Fetch historical data with error handling
def get_historical_data(asset, granularity=300):
    path = f"/products/{asset}-USD/candles?granularity={granularity}"
    max_retries = 3
    retry_delay = 5  # seconds

    for attempt in range(max_retries):
        try:
            response = requests.get(API_URL + path, timeout=10)
            response.raise_for_status()
            data = response.json()

            if not data:
                raise ValueError("Received empty historical data.")

            df = pd.DataFrame(data, columns=["time", "low", "high", "open", "close", "volume"])
            df["time"] = pd.to_datetime(df["time"], unit="s")
            df.sort_values("time", inplace=True)

            return df

        except (requests.RequestException, ValueError) as e:
            logger.error(f"Error fetching historical data (Attempt {attempt + 1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
            else:
                return None

# Preprocess data with validation
def preprocess_data(df):
    try:
        if df is None or df.empty:
            raise ValueError("DataFrame is empty or None. Cannot preprocess.")

        df["close"] = pd.to_numeric(df["close"], errors="coerce")
        if df["close"].isnull().any():
            raise ValueError("Invalid numerical values detected in 'close' column.")

        scaler = MinMaxScaler()
        scaled_data = scaler.fit_transform(df["close"].values.reshape(-1, 1))

        X, y = [], []
        for i in range(LOOKBACK, len(scaled_data)):
            X.append(scaled_data[i-LOOKBACK:i])
            y.append(scaled_data[i])

        pickle.dump(scaler, open(SCALER_FILE, "wb"))
        return np.array(X).reshape(-1, LOOKBACK, 1), np.array(y), scaler

    except ValueError as e:
        logger.error(f"Error in data preprocessing: {e}")
        return None, None, None

# WebSocket for live price updates with automatic reconnection
async def fetch_live_data():
    while True:
        try:
            async with websockets.connect("wss://ws-feed.pro.coinbase.com") as ws:
                await ws.send(json.dumps({"type": "subscribe", "channels": [{"name": "ticker", "product_ids": ["BTC-USD"]}]}))
                while True:
                    response = await ws.recv()
                    data = json.loads(response)
                    if "price" in data:
                        price = float(data["price"])
                        data_buffer.append(price)

        except websockets.exceptions.ConnectionClosed as e:
            logger.warning(f"WebSocket disconnected: {e}. Reconnecting in 5 seconds...")
            await asyncio.sleep(5)
        except Exception as e:
            logger.error(f"Unexpected WebSocket error: {e}. Restarting in 5 seconds...")
            await asyncio.sleep(5)

# Start live data listener in an async-safe way
def start_live_data_listener():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(fetch_live_data())
