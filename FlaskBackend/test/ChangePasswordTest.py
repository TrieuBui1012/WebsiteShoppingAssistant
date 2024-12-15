import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import unittest
import json
from flask import Flask, session
from app.auth import bp as auth_bp
from werkzeug.security import generate_password_hash

class MockUser:
    """Mock user class to mimic the structure of g.user in the app."""
    def __init__(self, accountId, username, password, isAdmin):
        self.accountId = accountId
        self.username = username
        self.password = password
        self.isAdmin = isAdmin

    def __repr__(self):
        return f"<MockUser {self.username}>"

class ChangePasswordTest(unittest.TestCase):
    def setUp(self):
        """Set up a test Flask application and register the auth blueprint."""
        self.app = Flask(__name__)
        self.app.config['SECRET_KEY'] = 'testsecret'
        self.app.register_blueprint(auth_bp)

        self.client = self.app.test_client()

        # Mock user object
        self.mock_user = MockUser(
            accountId=1,
            username="testuser",
            password=generate_password_hash("old_password"),  # Store the hash of the password
            isAdmin=False
        )

        # Mock the session and g variables
        self.app.before_request(self.mock_before_request)

    def mock_before_request(self):
        """Mock the `g.user` object for tests."""
        from flask import g
        g.user = self.mock_user

    def test_change_password_successful(self):
        """Test changing the password successfully."""
        # Mock new and old passwords
        old_password = "old_password"
        new_password = "new_password"

        # Create a PATCH request
        response = self.client.patch('/api/auth/change_password', json={
            "oldPassword": old_password,
            "newPassword": new_password
        })

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.get_json()['success'])
        self.assertEqual(response.get_json()['message'], "Change password successful!")

    def test_change_password_incorrect_old_password(self):
        """Test changing the password with incorrect old password."""
        # Mock new and old passwords
        old_password = "wrong_password"
        new_password = "new_password"

        # Create a PATCH request
        response = self.client.patch('/api/auth/change_password', json={
            "oldPassword": old_password,
            "newPassword": new_password
        })

        self.assertEqual(response.status_code, 401)
        self.assertFalse(response.get_json()['success'])
        self.assertEqual(response.get_json()['message'], "Incorrect old password.")

if __name__ == "__main__":
    unittest.main(verbosity=2)
