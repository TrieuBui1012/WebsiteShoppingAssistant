import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import unittest
from flask import Flask
from app import create_app
from app.models import Product, Category
import numpy as np
import joblib
from unittest.mock import patch, MagicMock

class MockProduct:
    def __init__(self, productId, origin, name, sellerName, brandName, quantitySold, reviewCount, rating):
        self.productId = productId
        self.origin = origin
        self.name = name
        self.sellerName = sellerName
        self.brandName = brandName
        self.quantitySold = quantitySold
        self.reviewCount = reviewCount
        self.rating = rating

class MockCategory:
    def __init__(self, name):
        self.name = name

class TestRecommendProducts(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        
        # Mock product data
        self.mock_product = MockProduct(
            productId=1,
            origin="tiki",
            name="Test Product",
            sellerName="Test Seller",
            brandName="Test Brand",
            quantitySold=100,
            reviewCount=50,
            rating=4.5
        )
        
        # Mock categories
        self.mock_categories = [
            MockCategory(name="Category 1"),
            MockCategory(name="Category 2")
        ]

    @patch('app.product.Product.Product.get_product_by_productId_origin')
    @patch('app.product.Category.Category.get_categories_by_productId_origin')
    @patch('app.product.search_products_by_vector')
    def test_recommend_products_success(self, mock_search, mock_get_categories, mock_get_product):
        # Setup mocks
        mock_get_product.return_value = self.mock_product
        mock_get_categories.return_value = self.mock_categories
        
        # Mock search results
        mock_search.return_value = [
            {
                "productId": 2,
                "origin": "tiki",
                "name": "Recommended Product",
                "quantitySold": 80,
                "price": 100.0,
                "reviewCount": 40,
                "rating": 4.0
            }
        ]

        # Make request
        response = self.client.get('/api/product/recommend_products_by_product_id/tiki/1')
        
        # Assert response
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json['success'])
        self.assertIsInstance(response.json['data'], list)
        self.assertTrue(len(response.json['data']) > 0)

if __name__ == '__main__':
    unittest.main(verbosity=2)
