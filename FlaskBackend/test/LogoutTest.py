import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import unittest
from flask import Flask
from app import create_app

class TestLogoutFunction(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

    def test_logout_no_logged_in_user(self):
        response = self.client.get('/api/auth/logout')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.get_json(), {'success': False, 'message': 'You are not logged in.'})

    def test_logout_logged_in_user(self):
        with self.client.session_transaction() as sess:
            sess['accountId'] = 1
        response = self.client.get('/api/auth/logout')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {'success': True, 'message': 'Log out successful!'})
        with self.client.session_transaction() as sess:
            self.assertNotIn('accountId', sess)

if __name__ == '__main__':
    unittest.main(verbosity=2)