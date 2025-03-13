import os
import tensorflow as tf
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import LSTM, Dense, Dropout, LayerNormalization
from tensorflow.keras.callbacks import EarlyStopping
from config import TRADING_CONFIG, get_logger
from data_handler import get_historical_data, preprocess_data, SCALER_FILE, data_buffer
import pickle
import numpy as np

logger = get_logger()

def train_or_update_model():
    """Train or update an LSTM model."""
    try:
        df = get_historical_data("BTC")
        if df is None or df.empty:
            logger.warning("No valid historical data available. Skipping training.")
            return

        X_train, y_train, scaler = preprocess_data(df)
        if X_train is None or y_train is None:
            logger.warning("Preprocessed data is invalid. Training aborted.")
            return

        model = Sequential([
            LSTM(50, return_sequences=True, input_shape=(TRADING_CONFIG["LOOKBACK"], 1)),
            LayerNormalization(),
            Dropout(0.2),
            LSTM(50, return_sequences=False),
            Dense(25, activation="relu"),
            Dense(1)
        ])

        model.compile(optimizer=tf.keras.optimizers.Adam(TRADING_CONFIG["LEARNING_RATE"]), loss="mse")

        early_stop = EarlyStopping(monitor='loss', patience=3, restore_best_weights=True)
        model.fit(X_train, y_train, epochs=TRADING_CONFIG["EPOCHS"], batch_size=TRADING_CONFIG["BATCH_SIZE"], callbacks=[early_stop])

        model.save(TRADING_CONFIG["MODEL_FILE"])
        pickle.dump(scaler, open(SCALER_FILE, "wb"))
        logger.info("Model training complete and saved.")

    except Exception as e:
        logger.error(f"Model training failed: {e}")

def predict_price():
    """Predict the next price movement using the trained LSTM model."""
    try:
        if len(data_buffer) < TRADING_CONFIG["LOOKBACK"]:
            logger.warning("Not enough recent data for prediction.")
            return None

        if not os.path.exists(TRADING_CONFIG["MODEL_FILE"]):
            logger.info("Model file not found. Training a new model.")
            train_or_update_model()

        model = load_model(TRADING_CONFIG["MODEL_FILE"])
        scaler = pickle.load(open(SCALER_FILE, "rb"))

        recent_data = np.array(data_buffer)[-TRADING_CONFIG["LOOKBACK"]:].reshape(-1, 1)
        scaled_data = scaler.transform(recent_data)

        prediction = model.predict(np.array([scaled_data]))[0][0]
        predicted_price = scaler.inverse_transform([[prediction]])[0][0]

        logger.info(f"Predicted Price: {predicted_price}")
        return predicted_price

    except Exception as e:
        logger.error(f"Prediction failed: {e}")
        return None