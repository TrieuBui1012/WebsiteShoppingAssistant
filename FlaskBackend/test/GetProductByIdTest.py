import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import unittest
from unittest.mock import patch, MagicMock
from flask import Flask
from flask.testing import FlaskClient
from app.product import bp  # Assuming the blueprint is imported from app.product

class TestGetProductById(unittest.TestCase):
    def setUp(self):
        # Create a test Flask app and register the blueprint
        self.app = Flask(__name__)
        self.app.register_blueprint(bp)
        self.app.config['TESTING'] = True
        self.client: FlaskClient = self.app.test_client()

    @patch('app.product.Product.Product.get_product_by_productId_origin')
    def test_get_product_by_id_success(self, mock_get_product):
        """
        Test successful retrieval of a product by ID and origin
        """
        # Create a mock product
        mock_product = MagicMock()
        mock_product.productId = 123
        mock_product.origin = 'tiki'
        mock_product.imgURL = 'http://example.com/image.jpg'
        mock_product.name = 'Test Product'
        mock_product.link = 'http://example.com/product'
        mock_product.quantitySold = 100
        mock_product.price = 19.99
        mock_product.reviewCount = 50
        mock_product.rating = 4.5
        mock_product.sellerName = 'Test Seller'
        mock_product.brandName = 'Test Brand'

        # Configure the mock to return the mock product
        mock_get_product.return_value = mock_product

        # Send a GET request to the route
        response = self.client.get('/api/product/tiki/product/123')

        # Check the response
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        
        self.assertTrue(data['success'])
        self.assertEqual(data['data']['productId'], 123)
        self.assertEqual(data['data']['origin'], 'tiki')
        self.assertEqual(data['data']['name'], 'Test Product')
        
        # Verify that the mock method was called with correct arguments
        mock_get_product.assert_called_once_with(123, 'tiki')

    @patch('app.product.Product.Product.get_product_by_productId_origin')
    def test_get_product_by_id_not_found(self, mock_get_product):
        """
        Test retrieval of a non-existent product
        """
        # Configure the mock to return None
        mock_get_product.return_value = None

        # Send a GET request to the route
        response = self.client.get('/api/product/lazada/product/999')

        # Check the response
        self.assertEqual(response.status_code, 404)
        data = response.get_json()
        
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Product not found.')
        
        # Verify that the mock method was called with correct arguments
        mock_get_product.assert_called_once_with(999, 'lazada')

    def test_get_product_by_id_invalid_origin(self):
        """
        Test route with an invalid origin
        """
        # Send a GET request with an invalid origin
        response = self.client.get('/api/product/invalid_origin/product/123')

        # Flask routing should handle this, typically with a 404 Not Found
        self.assertEqual(response.status_code, 404)

    def test_get_product_by_id_invalid_product_id(self):
        """
        Test route with an invalid product ID
        """
        # Send a GET request with an invalid product ID
        response = self.client.get('/api/product/tiki/product/abc')

        # Flask routing should handle this, typically with a 404 Not Found
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main(verbosity=2)