import os
import time
import threading
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import LSTM, Dense, Dropout, LayerNormalization
from tensorflow.keras.callbacks import EarlyStopping
from config import TRADING_CONFIG, get_logger
from data_handler import get_historical_data, preprocess_data, SCALER_FILE, data_buffer
import pickle
import random

logger = get_logger()

def enable_dropout(model):
    """Enable dropout at inference (MC Dropout)."""
    for layer in model.layers:
        if isinstance(layer, Dropout):
            layer.trainable = True
    return model
    def train_or_update_model():
    """Train or update an LSTM model based on historical data."""
    try:
        df = get_historical_data("BTC")
        if df is None or df.empty:
            logger.warning("No valid historical data available. Skipping model training.")
            return

        result = preprocess_data(df)
        if result is None or len(result) != 3:
            logger.warning("Preprocessed data invalid or incomplete. Training aborted.")
            return

        X_train, y_train, scaler = result
        if X_train.shape[0] < TRADING_CONFIG["BATCH_SIZE"]:
            logger.warning("Not enough training samples. Model training skipped.")
            return

        model = Sequential([
            LSTM(64, return_sequences=True, input_shape=(X_train.shape[1], X_train.shape[2])),
            LayerNormalization(),
            Dropout(0.3),
            LSTM(64),
            Dense(32, activation="relu"),
            Dense(1)
        ])

        model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=TRADING_CONFIG["LEARNING_RATE"]), loss="mse")
        early_stop = EarlyStopping(monitor='loss', patience=5, restore_best_weights=True)

        model.fit(X_train, y_train,
                  epochs=TRADING_CONFIG["EPOCHS"],
                  batch_size=TRADING_CONFIG["BATCH_SIZE"],
                  callbacks=[early_stop],
                  verbose=0)

        model.save(TRADING_CONFIG["MODEL_FILE"], include_optimizer=False)
        with open(SCALER_FILE, "wb") as f:
            pickle.dump(scaler, f)

        logger.info("Model training complete and saved.")

    except Exception as e:
        logger.exception(f"Model training failed: {e}")

def predict_price(auto_retrain_threshold: float = 0.12, mc_runs: int = 20):
    """Predict price and return mean + confidence. Auto-retrain on high deviation."""
    try:
        if len(data_buffer) < TRADING_CONFIG["LOOKBACK"]:
            logger.warning("Insufficient recent data. Prediction skipped.")
            return None

        if not os.path.isfile(TRADING_CONFIG["MODEL_FILE"]):
            logger.info("No model found. Initiating training sequence.")
            train_or_update_model()

        if not (os.path.isfile(TRADING_CONFIG["MODEL_FILE"]) and os.path.isfile(SCALER_FILE)):
            logger.error("Prediction aborted. Required model or scaler missing.")
            return None

        model = load_model(TRADING_CONFIG["MODEL_FILE"])
        with open(SCALER_FILE, "rb") as f:
            scaler = pickle.load(f)

        model = enable_dropout(model)

        recent = np.array(data_buffer[-TRADING_CONFIG["LOOKBACK"]:]).reshape(-1, 1)
        scaled = scaler.transform(recent).reshape(1, TRADING_CONFIG["LOOKBACK"], 1)

        predictions = [model(scaled, training=True).numpy()[0][0] for _ in range(mc_runs)]
        mean_pred = np.mean(predictions)
        std_pred = np.std(predictions)
        predicted_price = scaler.inverse_transform([[mean_pred]])[0][0]

        last_known_price = float(recent[-1][0])
        delta = abs(predicted_price - last_known_price) / max(last_known_price, 1e-6)

        logger.info(f"Predicted Price: {predicted_price:.2f} ± {std_pred:.4f}, Δ%: {delta*100:.2f}")

        if delta > auto_retrain_threshold:
            logger.warning(f"Prediction deviation {delta:.2%} exceeds threshold. Retraining model.")
            train_or_update_model()

        return predicted_price

    except Exception as e:
        logger.exception(f"Price prediction failed: {e}")
        return None

def schedule_retrain(interval_minutes=30):
    def loop():
        while True:
            logger.info("Scheduled model retraining triggered.")
            train_or_update_model()
            time.sleep(interval_minutes * 60)

    t = threading.Thread(target=loop, daemon=True)
    t.start()


def stream_predict_on_update(poll_interval=10):
    """Trigger prediction every few seconds if new data appears in buffer."""
    last_seen_len = 0

    def loop():
        nonlocal last_seen_len
        while True:
            if len(data_buffer) != last_seen_len:
                last_seen_len = len(data_buffer)
                predict_price()
            time.sleep(poll_interval)

    t = threading.Thread(target=loop, daemon=True)
    t.start()