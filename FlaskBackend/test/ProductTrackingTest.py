import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import unittest
from unittest.mock import patch, MagicMock
from flask import Flask, g, json
from app.tracking import bp
from app.models import ProductHistory
from datetime import datetime

class ProductTrackingTestCase(unittest.TestCase):

    def setUp(self):
        # Set up a Flask application for testing
        self.app = Flask(__name__)
        self.app.register_blueprint(bp)
        self.app.testing = True
        self.client = self.app.test_client()

        # Push an application context to access `g`
        self.app_context = self.app.app_context()
        self.app_context.push()

        # Mock user context
        g.user = MagicMock()
        g.user.accountId = 1

    def tearDown(self):
        # Remove the application context
        self.app_context.pop()

    @patch('app.tracking.ProductHistory')
    @patch('app.tracking.datetime')
    def test_product_success(self, mock_datetime, mock_product_history):
        # Mock datetime to control `createAt`
        mock_now = datetime(2024, 12, 9, 12, 0, 0)
        mock_datetime.now.return_value = mock_now

        # Mock the add method of ProductHistory
        mock_instance = MagicMock()
        mock_product_history.ProductHistory.return_value = mock_instance

        # Simulate a valid product request
        origin = "tiki"
        product_id = 12345
        response = self.client.post(f'/api/tracking/product/{origin}/{product_id}')

        # Check the response
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        self.assertEqual(response_data['success'], True)
        self.assertEqual(response_data['message'], 'Save product history successful!')

        # Ensure the ProductHistory model is called with correct arguments
        mock_product_history.ProductHistory.assert_called_with(
            accountId=1,
            productId=product_id,
            origin=origin,
            createAt=mock_now  # This is the mocked datetime value
        )
        mock_instance.add.assert_called_once()

if __name__ == '__main__':
    unittest.main(verbosity=2)
