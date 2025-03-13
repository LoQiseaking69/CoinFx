"""
CoinFx Trading Bot Initialization Module 🚀

This module sets up the environment, loads configurations, and ensures that all 
dependencies are correctly initialized when the package is imported.
"""

import os
import sys
import dotenv

# ✅ Load environment variables from .env file
dotenv.load_dotenv()

# Define the package version
__version__ = "1.1.0"

# Set up the base directory for imports
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

# Import key components with structured error handling
try:
    from .config import settings
    from .utils.logger import setup_logger
    from .trading.bot import TradingBot
    from .api.client import CoinbaseClient, OandaClient
except ImportError as e:
    print(f"⚠️ Import Error in __init__.py: {e}")
    sys.exit(1)

# ✅ Initialize logging
logger = setup_logger()

# ✅ Load API credentials securely
COINBASE_API_KEY = os.getenv("COINBASE_API_KEY", "").strip()
COINBASE_API_SECRET = os.getenv("COINBASE_API_SECRET", "").strip()
OANDA_ACCESS_TOKEN = os.getenv("OANDA_ACCESS_TOKEN", "").strip()

# ✅ Validate API Credentials
missing_keys = []
if not COINBASE_API_KEY:
    missing_keys.append("COINBASE_API_KEY")
if not COINBASE_API_SECRET:
    missing_keys.append("COINBASE_API_SECRET")
if not OANDA_ACCESS_TOKEN:
    missing_keys.append("OANDA_ACCESS_TOKEN")

if missing_keys:
    logger.warning(f"⚠️ Missing API Credentials: {', '.join(missing_keys)}. Live trading may not function correctly.")

# ✅ Log initialization success
logger.info(f"✅ CoinFx Bot v{__version__} initialized successfully with secure configurations!")