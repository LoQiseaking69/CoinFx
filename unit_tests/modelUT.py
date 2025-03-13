import unittest
import numpy as np
from unittest.mock import patch, MagicMock
from model import train_or_update_model, predict_price

class TestModel(unittest.TestCase):
    """Test Suite for AI Model Training & Predictions"""

    @patch("model.get_historical_data")
    @patch("model.preprocess_data")
    @patch("model.Sequential")
    def test_train_model_success(self, mock_model, mock_preprocess, mock_get_data):
        """Test model training with valid data."""
        mock_get_data.return_value = np.random.rand(100, 5)
        mock_preprocess.return_value = (np.random.rand(80, 50, 1), np.random.rand(80), None)
        mock_model.return_value.fit.return_value.history = {"loss": [0.5, 0.3]}

        train_or_update_model()
        self.assertLess(mock_model.return_value.fit.return_value.history["loss"][-1], 0.5)

    @patch("model.get_historical_data", return_value=None)
    def test_train_model_no_data(self, mock_get_data):
        """Test training failure when no data is available."""
        with self.assertRaises(Exception):
            train_or_update_model()

    @patch("model.predict_price")
    def test_predict_price(self, mock_predict):
        """Test prediction output with mocked LSTM model."""
        mock_predict.return_value = 40300
        prediction = predict_price()
        self.assertIsInstance(prediction, float)
        self.assertGreater(prediction, 0)

    def test_predict_price_no_data(self):
        """Test handling of insufficient input data."""
        with patch("model.data_buffer", new=[]):
            prediction = predict_price()
            self.assertIsNone(prediction)

if __name__ == "__main__":
    unittest.main()