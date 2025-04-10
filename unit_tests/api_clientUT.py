import unittest
from unittest.mock import patch, MagicMock
from genetic_trading import APIManager

class TestAPIManagerCoinbase(unittest.TestCase):
    """Test Suite for Coinbase Execution via APIManager"""

    @patch("genetic_trading.cbpro.AuthenticatedClient")
    def test_execute_trade_buy(self, mock_cbpro_client):
        mock_cbpro_client.return_value.place_market_order.return_value = {"id": "mock_order"}
        os_env_patch = {
            "COINBASE_API_KEY": "dummy",
            "COINBASE_API_SECRET": "dummy",
            "COINBASE_API_PASSPHRASE": "dummy"
        }
        with patch.dict("os.environ", os_env_patch):
            manager = APIManager()
            result = manager.execute_trade("BTC-USD", 1, "coinbase", amount="50")
            self.assertIsNone(result)  # execute_trade logs result, does not return

    @patch("genetic_trading.cbpro.AuthenticatedClient")
    def test_execute_trade_sell(self, mock_cbpro_client):
        mock_cbpro_client.return_value.place_market_order.return_value = {"id": "mock_order"}
        with patch.dict("os.environ", {
            "COINBASE_API_KEY": "dummy",
            "COINBASE_API_SECRET": "dummy",
            "COINBASE_API_PASSPHRASE": "dummy"
        }):
            manager = APIManager()
            manager.execute_trade("ETH-USD", 0, "coinbase", amount="25")
            mock_cbpro_client.return_value.place_market_order.assert_called_once()

class TestAPIManagerOanda(unittest.TestCase):
    """Test Suite for OANDA Execution via APIManager"""

    @patch("genetic_trading.oandapyV20.API")
    @patch("genetic_trading.orders.OrderCreate")
    def test_execute_trade_buy(self, mock_order_create, mock_oanda_api):
        mock_oanda_api.return_value.request.return_value = {"orderCreateTransaction": {"id": "oanda123"}}
        with patch.dict("os.environ", {
            "OANDA_ACCESS_TOKEN": "dummy",
            "OANDA_ACCOUNT_ID": "acct_123"
        }):
            manager = APIManager()
            manager.execute_trade("EUR_USD", 1, "oanda", amount="100")
            mock_oanda_api.return_value.request.assert_called_once()

if __name__ == "__main__":
    unittest.main()