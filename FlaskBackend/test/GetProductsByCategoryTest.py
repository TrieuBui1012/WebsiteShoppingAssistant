import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import unittest
from flask import Flask, json
from app.product import bp as product_bp
from unittest.mock import patch
from app.models.Product import Product

class TestGetProductsByCategory(unittest.TestCase):
    def setUp(self):
        """Set up test client and register blueprint"""
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
        self.app.register_blueprint(product_bp)
        self.client = self.app.test_client()

    @patch('app.models.Product.Product.get_products_by_category')
    def test_get_products_by_category_success(self, mock_get_products):
        """Test successful product retrieval by category"""
        # Mock product data
        mock_products = [
            Product(
                productId=1,
                origin='tiki',
                imgURL='http://example.com/1.jpg',
                name='Test Product 1',
                link='http://example.com/product1',
                quantitySold=100,
                price=199.99,
                reviewCount=50,
                rating=4.5,
                sellerName='Seller1',
                brandName='Brand1',
                createAt='2024-01-01'
            )
        ]
        mock_get_products.return_value = mock_products

        # Test request
        response = self.client.get(
            '/api/product/tiki/category/123/1',
            json={'order_by': 'normal', 'type': 'asc'}
        )
        
        # Verify response
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertEqual(data['current_page'], 1)
        self.assertEqual(data['per_page'], 40)
        self.assertEqual(len(data['data']), 1)
        
        # Verify product data
        product = data['data'][0]
        self.assertEqual(product['productId'], 1)
        self.assertEqual(product['origin'], 'tiki')
        self.assertEqual(product['name'], 'Test Product 1')

    def test_get_products_invalid_page(self):
        """Test invalid page number"""
        response = self.client.get(
            '/api/product/tiki/category/123/0',
            json={'order_by': 'normal', 'type': 'asc'}
        )
        
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Invalid page number.')

    @patch('app.models.Product.Product.get_products_by_category')
    def test_get_products_empty_result(self, mock_get_products):
        """Test empty product list"""
        mock_get_products.return_value = []
        
        response = self.client.get(
            '/api/product/tiki/category/123/1',
            json={'order_by': 'normal', 'type': 'asc'}
        )
        
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'No products found.')

    @patch('app.models.Product.Product.get_products_by_category_order')
    def test_get_products_price_sort(self, mock_get_products):
        """Test products sorted by price"""
        # Step 1: Create mock products in the order they should be returned
        mock_products_asc = [
            Product(productId=1, origin='tiki', imgURL='http://example.com/1.jpg',
                    name='Cheap Product', link='http://example.com/1', 
                    quantitySold=100, price=100.00, reviewCount=50, rating=4.5,
                    sellerName='Seller1', brandName='Brand1', createAt='2024-01-01'),
            Product(productId=2, origin='tiki', imgURL='http://example.com/2.jpg',
                    name='Expensive Product', link='http://example.com/2', 
                    quantitySold=200, price=200.00, reviewCount=40, rating=4.0,
                    sellerName='Seller2', brandName='Brand2', createAt='2024-01-01')
        ]
        
        mock_products_desc = list(reversed(mock_products_asc))

        # Step 2: Test ascending order
        mock_get_products.return_value = mock_products_asc
        response = self.client.get(
            '/api/product/tiki/category/123/1',
            json={'order_by': 'price', 'type': 'asc'}
        )
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertEqual(data['data'][0]['price'], 100.00)
        self.assertEqual(data['data'][1]['price'], 200.00)

        # Step 3: Test descending order
        mock_get_products.return_value = mock_products_desc
        response = self.client.get(
            '/api/product/tiki/category/123/1',
            json={'order_by': 'price', 'type': 'desc'}
        )
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertEqual(data['data'][0]['price'], 200.00)
        self.assertEqual(data['data'][1]['price'], 100.00)

    @patch('app.models.Product.Product.get_products_by_category_order')
    def test_get_products_rating_sort(self, mock_get_products):
        """Test products sorted by rating"""
        # Step 1: Create mock products pre-sorted by rating
        mock_products_desc = [
            Product(productId=2, origin='tiki', imgURL='http://example.com/2.jpg',
                    name='High Rated', link='http://example.com/2', 
                    quantitySold=200, price=200.00, reviewCount=40, rating=4.5,
                    sellerName='Seller2', brandName='Brand2', createAt='2024-01-01'),
            Product(productId=1, origin='tiki', imgURL='http://example.com/1.jpg',
                    name='Low Rated', link='http://example.com/1', 
                    quantitySold=100, price=100.00, reviewCount=50, rating=3.5,
                    sellerName='Seller1', brandName='Brand1', createAt='2024-01-01')
        ]

        # Step 2: Test descending rating sort
        mock_get_products.return_value = mock_products_desc
        response = self.client.get(
            '/api/product/tiki/category/123/1',
            json={'order_by': 'rating', 'type': 'desc'}
        )
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertEqual(data['data'][0]['rating'], 4.5)
        self.assertEqual(data['data'][1]['rating'], 3.5)


if __name__ == '__main__':
    unittest.main(verbosity=2)
