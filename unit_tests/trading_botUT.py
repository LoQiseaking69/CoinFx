import unittest
import tkinter as tk
from unittest.mock import patch, MagicMock
from trading_bot import TradingBotGUI

class TestTradingBotGUI(unittest.TestCase):
    """Test Suite for Trading Bot GUI"""

    def setUp(self):
        """Initialize a Tkinter root window for testing."""
        self.root = tk.Tk()
        self.bot = TradingBotGUI(self.root)

    def tearDown(self):
        """Destroy Tkinter window after each test."""
        self.root.destroy()

    def test_gui_elements_exist(self):
        """Ensure all GUI elements (buttons, labels) are present."""
        self.assertIsInstance(self.bot.start_button, tk.Button)
        self.assertIsInstance(self.bot.stop_button, tk.Button)
        self.assertIsInstance(self.bot.status_label, tk.Label)

    @patch("trading_bot.predict_price", return_value=40500)
    def test_start_trading(self, mock_predict):
        """Test start trading function."""
        self.bot.start_trading()
        self.assertTrue(self.bot.trading_active)
        self.assertEqual(self.bot.status_label.cget("text"), "Status: Trading Active")

    def test_stop_trading(self):
        """Test stop trading function."""
        self.bot.stop_trading()
        self.assertFalse(self.bot.trading_active)
        self.assertEqual(self.bot.status_label.cget("text"), "Status: Stopped")

if __name__ == "__main__":
    unittest.main()