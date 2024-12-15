import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import unittest
from unittest.mock import patch, MagicMock
from flask import Flask, g, json
from app.tracking import bp
from app.models import BrowseHistory
from datetime import datetime

class BrowseHistoryTestCase(unittest.TestCase):

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

    @patch('app.tracking.BrowseHistory')
    @patch('app.tracking.datetime')
    def test_browse_success(self, mock_datetime, mock_browse_history):
        # Mock datetime to control `createAt`
        mock_now = datetime(2024, 12, 9, 12, 0, 0)
        mock_datetime.now.return_value = mock_now

        # Mock the add method of BrowseHistory
        mock_instance = MagicMock()
        mock_browse_history.BrowseHistory.return_value = mock_instance

        # Create test data
        test_data = {
            'browse': 'Test search query'
        }
        response = self.client.post('/api/tracking/browse', json=test_data)

        # Check the response
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        self.assertEqual(response_data['success'], True)
        self.assertEqual(response_data['message'], 'Save browse history successful!')

        # Ensure the BrowseHistory model is called with correct arguments
        mock_browse_history.BrowseHistory.assert_called_with(
            content='Test search query',
            accountId=1,
            createAt=mock_now  # This is the mocked datetime value
        )
        mock_instance.add.assert_called_once()

    @patch('app.tracking.BrowseHistory')
    @patch('app.tracking.datetime')
    def test_browse_exception_handling(self, mock_datetime, mock_browse_history):
        mock_now = datetime(2024, 12, 9, 12, 0, 0)
        mock_datetime.now.return_value = mock_now

        # Mock the add method of BrowseHistory
        mock_instance = MagicMock()
        mock_browse_history.BrowseHistory.return_value = mock_instance

        response = self.client.post('/api/tracking/browse')

        # Check the response
        self.assertEqual(response.status_code, 415)

if __name__ == '__main__':
    unittest.main(verbosity=2 )

