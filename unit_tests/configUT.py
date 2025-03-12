from config import validate_config

try:
    validate_config()
    print("✅ API configuration is valid.")
except Exception as e:
    print(f"❌ Config Error: {e}")