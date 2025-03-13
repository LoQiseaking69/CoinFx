import unittest
import os
from unittest.mock import patch
from config import load_env

class TestConfig(unittest.TestCase):
    """Test Suite for Configuration & API Key Handling"""

    @patch.dict(os.environ, {"OANDA_ACCESS_TOKEN": "test_token", "OANDA_ACCOUNT_ID": "12345"})
    def test_env_loading_valid(self):
        """Test that environment variables are correctly loaded."""
        env = load_env()
        self.assertIn("OANDA_ACCESS_TOKEN", env)
        self.assertEqual(env["OANDA_ACCESS_TOKEN"], "test_token")
        self.assertIn("OANDA_ACCOUNT_ID", env)
        self.assertEqual(env["OANDA_ACCOUNT_ID"], "12345")

    @patch.dict(os.environ, {}, clear=True)
    def test_missing_env_variables(self):
        """Test handling of missing API credentials."""
        with self.assertRaises(SystemExit):
            load_env()

    @patch.dict(os.environ, {"OANDA_ACCESS_TOKEN": " "})
    def test_empty_env_variable(self):
        """Test handling of an empty API key."""
        env = load_env()
        self.assertEqual(env["OANDA_ACCESS_TOKEN"].strip(), "")

if __name__ == "__main__":
    unittest.main()