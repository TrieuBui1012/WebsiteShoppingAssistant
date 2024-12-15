import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import unittest
from unittest.mock import patch
from app import create_app
from app.models import Account

class TestLogin(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

    @patch.object(Account.Account, 'get_account_by_username_password')
    def test_successful_login(self, mock_get_account_by_username_password):
        # Mock the get_account_by_username_password method to return a valid account
        mock_account = Account.Account(username='test', password='test', isAdmin=False)
        mock_get_account_by_username_password.return_value = mock_account

        # Make a POST request to the login endpoint with the correct username and password
        response = self.client.post('/api/auth/login', json={'username': 'test', 'password': 'test'})

        # Assert that the response is a JSON response with the correct message and status code
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'success': True, 'message': 'Log in successful!'})

    @patch.object(Account.Account, 'get_account_by_username_password')
    def test_incorrect_username(self, mock_get_account_by_username_password):
        # Mock the get_account_by_username_password method to return None
        mock_get_account_by_username_password.return_value = None

        # Make a POST request to the login endpoint with an incorrect username
        response = self.client.post('/api/auth/login', json={'username': 'incorrect', 'password': 'test'})

        # Assert that the response is a JSON response with the correct message and status code
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json, {'success': False, 'message': 'Incorrect username or password.'})

    @patch.object(Account.Account, 'get_account_by_username_password')
    def test_incorrect_password(self, mock_get_account_by_username_password):
        # Mock the get_account_by_username_password method to return None
        mock_get_account_by_username_password.return_value = None

        # Make a POST request to the login endpoint with an incorrect password
        response = self.client.post('/api/auth/login', json={'username': 'test', 'password': 'incorrect'})

        # Assert that the response is a JSON response with the correct message and status code
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json, {'success': False, 'message': 'Incorrect username or password.'})

if __name__ == '__main__':
    unittest.main(verbosity=2)