import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import unittest
from unittest.mock import patch, MagicMock
from app.product import get_categories_by_origin

class TestGetCategoriesByOrigin(unittest.TestCase):
    @patch('app.product.get_categories')
    def test_tiki_origin_success(self, mock_get_categories):
        mock_get_categories.return_value = [
            {'categoryId': 1, 'name': 'Category 1', 'imgURL': 'img_url', 'isLeaf': False, 'children': []}
        ]
        response = get_categories_by_origin('tiki')
        self.assertEqual(response[0], {'success': True, 'data': mock_get_categories.return_value})
        self.assertEqual(response[1], 200)

    @patch('app.product.get_categories')
    def test_lazada_origin_success(self, mock_get_categories):
        mock_get_categories.return_value = [
            {'categoryId': 1, 'name': 'Category 1', 'imgURL': 'img_url', 'isLeaf': False, 'children': []}
        ]
        response = get_categories_by_origin('lazada')
        self.assertEqual(response[0], {'success': True, 'data': mock_get_categories.return_value})
        self.assertEqual(response[1], 200)

    @patch('app.product.get_categories')
    def test_tiki_origin_no_categories(self, mock_get_categories):
        mock_get_categories.return_value = []
        response = get_categories_by_origin('tiki')
        self.assertEqual(response[0], {'success': False, 'message': 'No categories found.'})
        self.assertEqual(response[1], 404)

    @patch('app.product.get_categories')
    def test_lazada_origin_no_categories(self, mock_get_categories):
        mock_get_categories.return_value = []
        response = get_categories_by_origin('lazada')
        self.assertEqual(response[0], {'success': False, 'message': 'No categories found.'})
        self.assertEqual(response[1], 404)

    @patch('app.product.get_categories')
    def test_invalid_origin(self, mock_get_categories):
        mock_get_categories.return_value = []
        response = get_categories_by_origin('invalid')
        self.assertEqual(response[0], {'success': False, 'message': 'No categories found.'})
        self.assertEqual(response[1], 404)

if __name__ == '__main__':
    unittest.main(verbosity=2)