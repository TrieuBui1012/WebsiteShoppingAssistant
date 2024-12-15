import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
from app import create_app
from app.models.Product import Product
import json

@pytest.fixture
def app():
    app = create_app({
        'TESTING': True,
    })
    return app

@pytest.fixture
def client(app):
    return app.test_client()

def test_search_products_by_query_success(client):
    # Test successful search
    query = "laptop"
    order_data = {"order_by": "normal", "type": "asc"}
    
    response = client.get(
        f'/api/product/query/{query}', 
        json=order_data
    )
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] == True
    assert isinstance(data['data'], list)
    
    # Verify product structure
    if len(data['data']) > 0:
        product = data['data'][0]
        assert 'productId' in product
        assert 'origin' in product
        assert 'imgURL' in product
        assert 'name' in product
        assert 'quantitySold' in product
        assert 'price' in product
        assert 'reviewCount' in product
        assert 'rating' in product

def test_search_products_different_ordering(client):
    # Test different ordering options
    query = "laptop"
    order_options = [
        {"order_by": "price", "type": "desc"},
        {"order_by": "rating", "type": "desc"},
        {"order_by": "quantitySold", "type": "desc"},
        {"order_by": "reviewCount", "type": "desc"}
    ]
    
    for order_data in order_options:
        response = client.get(
            f'/api/product/query/{query}',
            json=order_data
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] == True
        
        # Verify ordering
        if len(data['data']) > 1:
            if order_data["order_by"] == "price":
                assert data['data'][0]['price'] >= data['data'][1]['price']
            elif order_data["order_by"] == "rating":
                assert data['data'][0]['rating'] >= data['data'][1]['rating']
            elif order_data["order_by"] == "quantitySold":
                assert data['data'][0]['quantitySold'] >= data['data'][1]['quantitySold']
            elif order_data["order_by"] == "reviewCount":
                assert data['data'][0]['reviewCount'] >= data['data'][1]['reviewCount']

if __name__ == '__main__':
    pytest.main([__file__])