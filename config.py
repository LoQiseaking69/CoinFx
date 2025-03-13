import os
import dotenv
import logging
import time
import threading

# ✅ Load environment variables securely
dotenv.load_dotenv(override=True)

# ✅ Logging Configuration (Ensure logs directory exists)
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    filename=os.path.join(LOG_DIR, "trading.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

# ✅ Define Required & Optional API Credentials (Stored in Memory, Not Logged)
REQUIRED_ENV_VARS = ["OANDA_ACCESS_TOKEN", "OANDA_ACCOUNT_ID"]
OPTIONAL_ENV_VARS = ["COINBASE_API_KEY", "COINBASE_API_SECRET", "COINBASE_API_PASSPHRASE"]

def load_env():
    """Loads environment variables and validates them without exposing sensitive information."""
    dotenv.load_dotenv(override=True)
    env_values = {var: os.getenv(var) for var in REQUIRED_ENV_VARS + OPTIONAL_ENV_VARS}

    # 🚨 Validate Required Variables (Critical Failure if Missing)
    missing_vars = [var for var in REQUIRED_ENV_VARS if not env_values[var]]
    if missing_vars:
        logger.critical("❌ Missing required environment variables. Check your `.env` file or container settings.")
        raise SystemExit(f"❌ Critical Configuration Error: {', '.join(missing_vars)}")

    # ✅ Log partial Coinbase API config issues **without exposing secrets**
    if any(env_values[var] for var in OPTIONAL_ENV_VARS):
        missing_optional = [var for var in OPTIONAL_ENV_VARS if not env_values[var]]
        if missing_optional:
            logger.warning("⚠️ Some Coinbase API credentials are missing. Check your `.env` settings.")

    logger.info("✅ Environment variables loaded successfully.")
    
    # 🚨 NEVER log or print sensitive values for security reasons
    return env_values

# ✅ Initial Load (Stored in Memory, Not Logged)
env = load_env()

# ✅ Assign API Credentials (Kept in Memory Only)
OANDA_ACCESS_TOKEN, OANDA_ACCOUNT_ID = env["OANDA_ACCESS_TOKEN"], env["OANDA_ACCOUNT_ID"]
COINBASE_API_KEY, COINBASE_API_SECRET, COINBASE_API_PASSPHRASE = (
    env.get("COINBASE_API_KEY"), env.get("COINBASE_API_SECRET"), env.get("COINBASE_API_PASSPHRASE")
)

# ✅ Trading & Risk Parameters (Defaults are provided for safety)
TRADING_CONFIG = {
    "LOOKBACK": int(os.getenv("LOOKBACK", 50)),
    "STOP_LOSS_PERCENT": float(os.getenv("STOP_LOSS_PERCENT", 0.02)),
    "TAKE_PROFIT_PERCENT": float(os.getenv("TAKE_PROFIT_PERCENT", 0.05)),
    "LEARNING_RATE": float(os.getenv("LEARNING_RATE", 0.001)),
    "EPOCHS": int(os.getenv("EPOCHS", 5)),
    "BATCH_SIZE": int(os.getenv("BATCH_SIZE", 16)),
    "SCALER_FILE": os.getenv("SCALER_FILE", "scaler.pkl"),
    "MODEL_FILE": os.getenv("MODEL_FILE", "lstm_model.h5"),
    "DB_FILE": os.getenv("DB_FILE", "trades.db"),
    "TRADE_LOG_FILE": os.getenv("TRADE_LOG_FILE", "trade_log.csv"),
}

RISK_MANAGEMENT = {
    "MAX_POSITION_SIZE": float(os.getenv("MAX_POSITION_SIZE", 0.1)),
    "MAX_CONCURRENT_TRADES": int(os.getenv("MAX_CONCURRENT_TRADES", 5)),
    "POSITION_COOLDOWN": int(os.getenv("POSITION_COOLDOWN", 60)),
}

# ✅ Safe Environment Reload Function
def reload_env():
    """Securely reloads environment variables without exposing sensitive information."""
    global env, OANDA_ACCESS_TOKEN, OANDA_ACCOUNT_ID, COINBASE_API_KEY, COINBASE_API_SECRET, COINBASE_API_PASSPHRASE
    env = load_env()
    OANDA_ACCESS_TOKEN, OANDA_ACCOUNT_ID = env["OANDA_ACCESS_TOKEN"], env["OANDA_ACCOUNT_ID"]
    COINBASE_API_KEY, COINBASE_API_SECRET, COINBASE_API_PASSPHRASE = (
        env.get("COINBASE_API_KEY"), env.get("COINBASE_API_SECRET"), env.get("COINBASE_API_PASSPHRASE")
    )
    logger.info("🔄 Environment variables reloaded securely.")

# ✅ Automatic Environment Reload (Runs in the Background)
def auto_reload_env(interval=60):
    """Reloads environment variables every `interval` seconds securely."""
    while True:
        reload_env()
        time.sleep(interval)

# ✅ Start a background thread to refresh env variables securely
threading.Thread(target=auto_reload_env, daemon=True).start()