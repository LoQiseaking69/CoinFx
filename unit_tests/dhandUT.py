from data_handler import get_historical_data, start_live_data_listener
import threading

df = get_historical_data("BTC")
if df is not None and not df.empty:
    print("✅ Historical data fetched successfully.")
else:
    print("❌ Historical data fetch failed.")

# Start live data feed
threading.Thread(target=start_live_data_listener, daemon=True).start()
print("✅ Live data listener started.")