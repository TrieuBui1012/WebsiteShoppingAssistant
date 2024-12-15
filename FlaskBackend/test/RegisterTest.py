import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import unittest
from unittest.mock import patch
from app import create_app
from app.models.db import get_db

class TestRegister(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

    def test_successful_registration(self):
        data = {'username': 'test_user', 'password': 'test_password'}
        with patch('app.auth.Account') as mock_Account:
            mock_Account.return_value.add.return_value = None
            response = self.client.post('/api/auth/register', json=data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['success'], True)
        self.assertEqual(response.json['message'], 'Register successful!')

    def test_registration_with_missing_username(self):
        data = {'password': 'test_password'}
        response = self.client.post('/api/auth/register', json=data)
        self.assertEqual(response.status_code, 409)
        self.assertEqual(response.json['success'], False)
        self.assertEqual(response.json['message'], 'Username is required.')

    def test_registration_with_missing_password(self):
        data = {'username': 'test_user'}
        response = self.client.post('/api/auth/register', json=data)
        self.assertEqual(response.status_code, 409)
        self.assertEqual(response.json['success'], False)
        self.assertEqual(response.json['message'], 'Password is required.')

    def test_registration_with_existing_username(self):
        data = {'username': 'test_user', 'password': 'test_password'}
        # Create a test user
        with self.app.app_context():
            db = get_db()
            with db.cursor(dictionary=True) as cursor:
                self.client.post('/api/auth/register', json=data)
                # Try to register the same user again
                response = self.client.post('/api/auth/register', json=data)
                cursor.execute("DELETE FROM Account WHERE username = 'test_user'")
                db.commit()
        self.assertEqual(response.status_code, 409)
        self.assertEqual(response.json['success'], False)
        self.assertEqual(response.json['message'], 'User test_user is already registered.')

if __name__ == '__main__':
    unittest.main(verbosity=2)