import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from data_handler import get_historical_data, preprocess_data, start_live_data_listener

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

    def test_preprocess_data(self):
        """Test preprocessing function with valid & invalid data."""
        df_valid = pd.DataFrame({"close": [40000, 40100, 40200, 40300, 40400]})
        X, y, _ = preprocess_data(df_valid)
        self.assertEqual(X.shape[0], len(df_valid) - 1)
        self.assertEqual(y.shape[0], len(df_valid) - 1)

        df_invalid = pd.DataFrame({"close": ["invalid", "data", None, 40400]})
        X, y, _ = preprocess_data(df_invalid)
        self.assertIsNone(X)
        self.assertIsNone(y)

    def test_start_live_data_listener(self):
        """Test that live data listener runs without immediate errors."""
        self.assertIsNone(start_live_data_listener())

if __name__ == "__main__":
    unittest.main()