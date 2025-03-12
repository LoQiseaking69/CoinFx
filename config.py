import os
import dotenv
import logging

# Load environment variables
dotenv.load_dotenv()

# Ensure logs directory exists before logging setup
LOG_DIR = "logs"
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# Logging Configuration (Safe Initialization)
logging.basicConfig(
    filename=os.path.join(LOG_DIR, "trading.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def get_logger():
    """Returns a configured logger instance."""
    return logging.getLogger(__name__)

logger = get_logger()

# ✅ API Credentials (with Coinbase as optional)
OANDA_ACCESS_TOKEN = os.getenv("OANDA_ACCESS_TOKEN")
OANDA_ACCOUNT_ID = os.getenv("OANDA_ACCOUNT_ID")

COINBASE_API_KEY = os.getenv("COINBASE_API_KEY")
COINBASE_API_SECRET = os.getenv("COINBASE_API_SECRET")
COINBASE_API_PASSPHRASE = os.getenv("COINBASE_API_PASSPHRASE")

API_URL = "https://api.pro.coinbase.com"  # Ensure this is still valid

# ✅ Trading Parameters
LOOKBACK = 50
STOP_LOSS_PERCENT = 0.02
TAKE_PROFIT_PERCENT = 0.05
LEARNING_RATE = 0.001
EPOCHS = 5
BATCH_SIZE = 16
SCALER_FILE = "scaler.pkl"
MODEL_FILE = "lstm_model.h5"
DB_FILE = "trades.db"
TRADE_LOG_FILE = "trade_log.csv"

# ✅ Risk Management
MAX_POSITION_SIZE = 0.1  # Max % of portfolio allocated to a single trade
MAX_CONCURRENT_TRADES = 5
POSITION_COOLDOWN = 60  # Time (seconds) between trades

def validate_config():
    """Ensure all required environment variables are set correctly."""
    missing_vars = []

    # ✅ OANDA is **required**
    if not OANDA_ACCESS_TOKEN:
        missing_vars.append("OANDA_ACCESS_TOKEN")
    if not OANDA_ACCOUNT_ID:
        missing_vars.append("OANDA_ACCOUNT_ID")

    # ✅ Coinbase is **optional** (only validated if partially provided)
    if any([COINBASE_API_KEY, COINBASE_API_SECRET, COINBASE_API_PASSPHRASE]):
        if not all([COINBASE_API_KEY, COINBASE_API_SECRET, COINBASE_API_PASSPHRASE]):
            missing_vars.append("COINBASE_API_CREDENTIALS (some values are missing)")

    # 🚨 Raise an error if required credentials are missing
    if missing_vars:
        logger.error(f"Missing required environment variables: {', '.join(missing_vars)}")
        raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")

    logger.info("✅ Configuration validation passed. All required credentials are set.")

def reload_env():
    """Reloads environment variables (useful for runtime updates)."""
    dotenv.load_dotenv(override=True)
    logger.info("🔄 Environment variables reloaded.")

# ✅ Validate config at startup
try:
    validate_config()
except ValueError as e:
    logger.critical(f"Configuration Error: {e}")
    raise SystemExit(f"❌ Critical Configuration Error: {e}")