import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
import asyncio
from data_handler import get_historical_data, preprocess_data, start_live_data_listener, data_buffer

class TestDataHandler(unittest.TestCase):
    """Test Suite for Market Data Retrieval & Processing"""

    @patch("data_handler.requests.get")
    def test_get_historical_data_success(self, mock_get):
        """Test successful API response with valid data."""
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = [
            [1700000000, 40000, 40500, 39800, 40300, 1500]
        ]

        df = get_historical_data("BTC")
        self.assertIsInstance(df, pd.DataFrame)
        self.assertIn("close", df.columns)
        self.assertGreater(len(df), 0)

    @patch("data_handler.requests.get")
    def test_get_historical_data_failure(self, mock_get):
        """Test failed API response handling."""
        mock_get.return_value.status_code = 500
        mock_get.return_value.json.return_value = {}

        df = get_historical_data("BTC")
        self.assertIsNone(df)

    def test_preprocess_data_valid(self):
        """Test preprocessing with valid data."""
        df_valid = pd.DataFrame({"close": list(range(50, 100))})
        X, y, scaler = preprocess_data(df_valid, save_scaler=False)
        lookback =  TRADING_CONFIG["LOOKBACK"]
        self.assertEqual(X.shape, (len(df_valid) - lookback, lookback, 1))
        self.assertEqual(y.shape[0], len(df_valid) - lookback)
        self.assertIsNotNone(scaler)

    def test_preprocess_data_invalid(self):
        """Test preprocessing with invalid numeric data."""
        df_invalid = pd.DataFrame({"close": ["invalid", None, "NaN"]})
        X, y, _ = preprocess_data(df_invalid, save_scaler=False)
        self.assertIsNone(X)
        self.assertIsNone(y)

    @patch("data_handler.fetch_live_data")
    def test_start_live_data_listener_runs(self, mock_fetch):
        """Test live listener starts an async event loop."""
        mock_fetch.return_value = asyncio.sleep(0)  # fake coroutine
        result = start_live_data_listener()
        self.assertIsNone(result)

    def test_data_buffer_structure(self):
        """Test that data buffer is a deque and behaves as expected."""
        data_buffer.clear()
        data_buffer.append(50000.0)
        self.assertEqual(len(data_buffer), 1)
        self.assertIsInstance(data_buffer[-1], float)

if __name__ == "__main__":
    unittest.main()