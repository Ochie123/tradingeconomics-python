import os
import unittest
from unittest.mock import patch
import json
from examples.market_forecasts.marketApp import app, fetch_market_forecasts, process_data, calculate_changes
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class TestMarketForecastsApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    @patch('examples.market_forecasts.marketApp.fetch_market_forecasts')
    def test_index_page(self, mock_fetch_data):
        # Load sample data from a file
        with open('tests/sample_data.json', 'r') as f:
            sample_data = json.load(f)

        mock_fetch_data.return_value = sample_data
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Market Forecasts Dashboard', response.data)
        self.assertIn(b'Forecast Values', response.data)
        self.assertIn(b'Percentage Changes', response.data)

    def test_fetch_market_forecasts(self):
        api_key = os.getenv('API_KEY')
        self.assertIsNotNone(api_key, "API_KEY environment variable is not set")

        with patch.dict(os.environ, {'API_KEY': api_key}):
            data = fetch_market_forecasts()
            self.assertIsInstance(data, list)
            self.assertTrue(len(data) > 0)
            self.assertIn('Symbol', data[0])

    def test_process_data(self):
        with open('tests/sample_data.json', 'r') as f:
            sample_data = json.load(f)

        processed_data = process_data(sample_data)
        self.assertIsInstance(processed_data, list)
        self.assertTrue(len(processed_data) > 0)
        self.assertIn('Country', processed_data[0])
        self.assertIn('Dec_2024', processed_data[0])

    def test_calculate_changes(self):
        with open('tests/sample_data.json', 'r') as f:
            sample_data = json.load(f)

        processed_data = process_data(sample_data)
        changes_data = calculate_changes(processed_data)
        self.assertIsInstance(changes_data, list)
        self.assertTrue(len(changes_data) > 0)
        self.assertIn('Country', changes_data[0])
        self.assertIn('Dec_2024', changes_data[0])
        self.assertIsInstance(changes_data[0]['Dec_2024'], float)

if __name__ == '__main__':
    unittest.main()