"""
CoinFx Trading Bot Initialization Module 🚀

This module sets up the environment, loads configurations, and ensures that all 
dependencies are correctly initialized when the package is imported.
"""

import os
import sys

# Define the package version
__version__ = "1.0.0"

# Set up the base directory for imports
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

# Import key components
try:
    from .config import settings
    from .utils.logger import setup_logger
    from .trading.bot import TradingBot
    from .api.client import CoinbaseClient
except ImportError as e:
    print(f"⚠️ Import Error in __init__.py: {e}")

# Initialize logging
logger = setup_logger()

# Load API credentials (if environment variables are set)
COINBASE_API_KEY = os.getenv("COINBASE_API_KEY", "")
COINBASE_API_SECRET = os.getenv("COINBASE_API_SECRET", "")

if not COINBASE_API_KEY or not COINBASE_API_SECRET:
    logger.warning("⚠️ API Credentials not found in environment variables!")

logger.info(f"✅ CoinFx Bot v{__version__} initialized successfully!")

