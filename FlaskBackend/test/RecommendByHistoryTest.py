import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
from app import create_app
from app.models.db import get_db
from app.models import Product, Category, ProductHistory
import json
from datetime import datetime

@pytest.fixture
def app():
    app = create_app({
        'TESTING': True,
    })
    return app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def auth_client(client):
    # Login as test user
    response = client.post('/api/auth/login', 
        json={'username': 'user1', 'password': 'user1'})
    assert response.status_code == 200
    return client

@pytest.fixture
def auth_client_no_history(client):
    # Login as test user
    response = client.post('/api/auth/login', 
        json={'username': 'user2', 'password': 'user2'})
    assert response.status_code == 200
    return client

def test_recommend_products_no_history(auth_client_no_history):
    """Test recommendations when user has no history"""
    response = auth_client_no_history.get('/api/product/recommend_products_by_history')
    assert response.status_code == 404
    assert response.json['success'] == False
    assert response.json['message'] == "No products found."

def test_recommend_products_with_history(auth_client):
    response = auth_client.get('/api/product/recommend_products_by_history')
    
    assert response.status_code == 200
    assert response.json['success'] == True
    assert 'data' in response.json
    
    # Verify response data structure
    products = response.json['data']
    assert len(products) > 0
    
    # Check first product has all required fields
    product = products[0]
    required_fields = ['productId', 'origin', 'imgURL', 'name', 'link', 
                      'quantitySold', 'price', 'reviewCount', 'rating',
                      'sellerName', 'brandName']
    
    for field in required_fields:
        assert field in product

def test_recommend_products_invalid_auth(client):
    """Test recommendations without authentication"""
    response = client.get('/api/product/recommend_products_by_history')
    assert response.status_code == 401

if __name__ == "__main__":
    pytest.main([__file__])