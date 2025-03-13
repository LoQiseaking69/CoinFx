import unittest
from unittest.mock import patch, MagicMock
from api.client import CoinbaseClient, OandaClient

class TestCoinbaseClient(unittest.TestCase):
    """Test Suite for Coinbase Trade Execution"""

    @patch("api.client.cbpro.AuthenticatedClient")
    def test_place_order(self, mock_cbpro_client):
        """Test placing a Coinbase market order."""
        mock_cbpro_client.return_value.place_market_order.return_value = {"id": "test123"}
        client = CoinbaseClient(api_key="dummy", api_secret="dummy", api_passphrase="dummy")
        response = client.place_order("BTC-USD", "buy", 100)
        self.assertEqual(response["id"], "test123")

class TestOandaClient(unittest.TestCase):
    """Test Suite for OANDA Trade Execution"""

    @patch("api.client.oandapyV20.API")
    def test_execute_trade(self, mock_oanda_client):
        """Test placing an OANDA market order."""
        mock_oanda_client.return_value.request.return_value = {"orderCreateTransaction": {"id": "test456"}}
        client = OandaClient(access_token="dummy", account_id="12345")
        response = client.execute_trade("EUR_USD", 100, "buy")
        self.assertEqual(response["orderCreateTransaction"]["id"], "test456")

if __name__ == "__main__":
    unittest.main()