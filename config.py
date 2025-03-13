import os
import dotenv
import logging
import time
import threading

# ✅ Load Environment Variables Securely
dotenv.load_dotenv(override=True)

# ✅ Logging Configuration
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    filename=os.path.join(LOG_DIR, "trading.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

# ✅ Ensure logger function is correctly defined
def get_logger():
    """Returns the global logger instance."""
    return logger

# ✅ Define Required & Optional API Credentials
REQUIRED_ENV_VARS = {
    "OANDA_ACCESS_TOKEN": "OANDA_API_KEY",  # Fallback key
    "OANDA_ACCOUNT_ID": None,
}
OPTIONAL_ENV_VARS = ["COINBASE_API_KEY", "COINBASE_API_SECRET", "COINBASE_API_PASSPHRASE"]

def load_env():
    """Loads and validates environment variables securely."""
    dotenv.load_dotenv(override=True)
    
    env_values = {}
    missing_vars = []

    # ✅ Validate Required Variables
    for key, fallback in REQUIRED_ENV_VARS.items():
        env_values[key] = os.getenv(key) or (os.getenv(fallback) if fallback else None)
        if not env_values[key]:
            missing_vars.append(key)

    if missing_vars:
        logger.critical(f"❌ Missing required environment variables: {', '.join(missing_vars)}")
        raise SystemExit(f"❌ Configuration Error: {', '.join(missing_vars)}")

    # ✅ Validate Optional Variables
    optional_values = {var: os.getenv(var, "").strip() for var in OPTIONAL_ENV_VARS}
    if any(optional_values.values()):
        missing_optional = [var for var, value in optional_values.items() if not value]
        if missing_optional:
            logger.warning(f"⚠️ Missing optional API credentials: {', '.join(missing_optional)}")

    logger.info("✅ Environment variables loaded successfully.")
    return {**env_values, **optional_values}  # Merge required & optional variables

# ✅ Load Environment Variables
env = load_env()

# ✅ Secure API Credentials
OANDA_ACCESS_TOKEN, OANDA_ACCOUNT_ID = env["OANDA_ACCESS_TOKEN"], env["OANDA_ACCOUNT_ID"]
COINBASE_API_KEY, COINBASE_API_SECRET, COINBASE_API_PASSPHRASE = (
    env.get("COINBASE_API_KEY"), env.get("COINBASE_API_SECRET"), env.get("COINBASE_API_PASSPHRASE")
)

# ✅ Define Trading & Risk Management Configurations
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

TRADING_CONFIG = {
    "LOOKBACK": int(os.getenv("LOOKBACK", 50)),
    "STOP_LOSS_PERCENT": float(os.getenv("STOP_LOSS_PERCENT", 0.02)),
    "TAKE_PROFIT_PERCENT": float(os.getenv("TAKE_PROFIT_PERCENT", 0.05)),
    "LEARNING_RATE": float(os.getenv("LEARNING_RATE", 0.001)),
    "EPOCHS": int(os.getenv("EPOCHS", 5)),
    "BATCH_SIZE": int(os.getenv("BATCH_SIZE", 16)),
    "SCALER_FILE": os.getenv("SCALER_FILE", os.path.join(BASE_DIR, "scaler.pkl")),
    "MODEL_FILE": os.getenv("MODEL_FILE", os.path.join(BASE_DIR, "lstm_model.h5")),
    "DB_FILE": os.getenv("DB_FILE", os.path.join(BASE_DIR, "trades.db")),
    "TRADE_LOG_FILE": os.getenv("TRADE_LOG_FILE", os.path.join(BASE_DIR, "trade_log.csv")),
}

RISK_MANAGEMENT = {
    "MAX_POSITION_SIZE": float(os.getenv("MAX_POSITION_SIZE", 0.1)),
    "MAX_CONCURRENT_TRADES": int(os.getenv("MAX_CONCURRENT_TRADES", 5)),
    "POSITION_COOLDOWN": int(os.getenv("POSITION_COOLDOWN", 60)),
}

# ✅ Ensure Required Files Exist
for file_path in [TRADING_CONFIG["SCALER_FILE"], TRADING_CONFIG["MODEL_FILE"], TRADING_CONFIG["DB_FILE"], TRADING_CONFIG["TRADE_LOG_FILE"]]:
    if not os.path.exists(file_path):
        open(file_path, "a").close()  # Create empty files if missing

# ✅ Safe Environment Reload
def reload_env():
    """Securely reloads environment variables."""
    global env, OANDA_ACCESS_TOKEN, OANDA_ACCOUNT_ID, COINBASE_API_KEY, COINBASE_API_SECRET, COINBASE_API_PASSPHRASE
    env = load_env()
    OANDA_ACCESS_TOKEN, OANDA_ACCOUNT_ID = env["OANDA_ACCESS_TOKEN"], env["OANDA_ACCOUNT_ID"]
    COINBASE_API_KEY, COINBASE_API_SECRET, COINBASE_API_PASSPHRASE = (
        env.get("COINBASE_API_KEY"), env.get("COINBASE_API_SECRET"), env.get("COINBASE_API_PASSPHRASE")
    )
    logger.info("🔄 Environment variables reloaded successfully.")

# ✅ Automatic Environment Reload (Runs in Background)
def auto_reload_env(interval=60):
    """Periodically reloads environment variables in the background."""
    while True:
        reload_env()
        time.sleep(interval)

# ✅ Start Background Thread for Auto-Reloading
threading.Thread(target=auto_reload_env, daemon=True).start()
