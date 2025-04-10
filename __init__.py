"""
CoinFx Trading Bot Initialization Module 🚀

Sets up environment, loads .env, validates configurations, and prepares logging.
"""

import os
import sys
import dotenv

# Load environment variables
dotenv.load_dotenv()

__version__ = "1.1.0"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

try:
    from .config import TRADING_CONFIG, get_logger
    from .genetic_trading import APIManager
except ImportError as e:
    print(f"⚠️ Import Error in __init__.py: {e} — some components may not function.")

logger = get_logger()

# Validate API credentials
COINBASE_API_KEY = os.getenv("COINBASE_API_KEY", "").strip()
COINBASE_API_SECRET = os.getenv("COINBASE_API_SECRET", "").strip()
OANDA_ACCESS_TOKEN = os.getenv("OANDA_ACCESS_TOKEN", "").strip()

missing_keys = []
if not COINBASE_API_KEY:
    missing_keys.append("COINBASE_API_KEY")
if not COINBASE_API_SECRET:
    missing_keys.append("COINBASE_API_SECRET")
if not OANDA_ACCESS_TOKEN:
    missing_keys.append("OANDA_ACCESS_TOKEN")

if missing_keys:
    logger.warning(f"⚠️ Missing API credentials: {', '.join(missing_keys)} — live trading may not function.")

# Validate TRADING_CONFIG structure
required_config_keys = ["LOOKBACK", "LEARNING_RATE", "EPOCHS", "BATCH_SIZE", "MODEL_FILE", "SCALER_FILE"]
missing_config_keys = [key for key in required_config_keys if key not in TRADING_CONFIG]

if missing_config_keys:
    logger.error(f"❌ Missing TRADING_CONFIG keys: {', '.join(missing_config_keys)} — aborting configuration load.")
else:
    logger.info(f"✅ TRADING_CONFIG loaded with keys: {', '.join(required_config_keys)}")

logger.info(f"✅ CoinFx Bot v{__version__} initialized.")