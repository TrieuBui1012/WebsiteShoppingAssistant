import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import unittest
import json
from flask import Flask, session
from app.auth import bp as auth_bp
from werkzeug.security import generate_password_hash, check_password_hash

class MockUser:
    """Mock user class to mimic the structure of g.user in the app."""
    def __init__(self, accountId, username, password, isAdmin):
        self.accountId = accountId
        self.username = username
        self.password = password
        self.isAdmin = isAdmin

    def __repr__(self):
        return f"<MockUser {self.username}>"

class AdminLoginTestCase(unittest.TestCase):
    def setUp(self):
        """Set up a test Flask application and register the auth blueprint."""
        self.app = Flask(__name__)
        self.app.config['SECRET_KEY'] = 'testsecret'
        self.app.register_blueprint(auth_bp)

        self.client = self.app.test_client()

        # Mock user data
        self.admin_user = MockUser(
            accountId=1,
            username="adminuser",
            password=generate_password_hash("admin_password"),
            isAdmin=True
        )

        self.non_admin_user = MockUser(
            accountId=2,
            username="regularuser",
            password=generate_password_hash("user_password"),
            isAdmin=False
        )

        # Mock the user database
        self.user_database = {
            "adminuser": self.admin_user,
            "regularuser": self.non_admin_user
        }

        # Mock Account methods
        self.mock_account_methods()

    def mock_account_methods(self):
        """Mock methods in the Account class."""
        import app.models.Account as Account

        def get_account_by_username_password(username, password):
            user = self.user_database.get(username)
            if user and check_password_hash(user.password, password):
                return user
            return None

        Account.Account.get_account_by_username_password = staticmethod(get_account_by_username_password)

    def test_admin_login_successful(self):
        """Test successful admin login."""
        response = self.client.post('/api/auth/admin_login', json={
            "username": "adminuser",
            "password": "admin_password"
        })

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.get_json()['success'])
        self.assertEqual(response.get_json()['message'], "Log in as an admin successful!")
        with self.client.session_transaction() as session:
            self.assertEqual(session.get('accountId'), 1)

    def test_admin_login_incorrect_credentials(self):
        """Test login attempt with incorrect credentials."""
        response = self.client.post('/api/auth/admin_login', json={
            "username": "adminuser",
            "password": "wrong_password"
        })

        self.assertEqual(response.status_code, 401)
        self.assertFalse(response.get_json()['success'])
        self.assertEqual(response.get_json()['message'], "Incorrect username or password.")

    def test_admin_login_non_admin_user(self):
        """Test login attempt by a non-admin user."""
        response = self.client.post('/api/auth/admin_login', json={
            "username": "regularuser",
            "password": "user_password"
        })

        self.assertEqual(response.status_code, 401)
        self.assertFalse(response.get_json()['success'])
        self.assertEqual(response.get_json()['message'], "You cannot log in as an admin.")

if __name__ == "__main__":
    unittest.main(verbosity=2)
