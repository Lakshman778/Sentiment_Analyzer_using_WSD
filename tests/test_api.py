"""
API Tests
"""
import pytest
import json
import sys
from pathlib import Path

# Add Backend to path
backend_path = Path(__file__).parent.parent / 'Backend'
sys.path.insert(0, str(backend_path))

from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_check(client):
    """Test health endpoint"""
    response = client.get('/api/health')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'healthy'

def test_analyze_endpoint(client):
    """Test analyze endpoint"""
    response = client.post('/api/analyze',
        json={'text': 'This is amazing!'},
        content_type='application/json'
    )
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] == True

def test_analyze_product_endpoint(client):
    """Test product analysis"""
    response = client.post('/api/analyze-product',
        json={'text': 'Great quality! Fast shipping!'},
        content_type='application/json'
    )
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] == True

def test_analyze_social_endpoint(client):
    """Test social analysis"""
    response = client.post('/api/analyze-social',
        json={'text': 'Amazing! #blessed'},
        content_type='application/json'
    )
    assert response.status_code == 200

def test_batch_endpoint(client):
    """Test batch analysis"""
    response = client.post('/api/analyze-batch',
        json={'texts': ['Good!', 'Bad!', 'OK']},
        content_type='application/json'
    )
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['total'] == 3

def test_missing_text(client):
    """Test error handling"""
    response = client.post('/api/analyze',
        json={},
        content_type='application/json'
    )
    assert response.status_code == 400

def test_version_endpoint(client):
    """Test version endpoint"""
    response = client.get('/api/version')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['version'] == '2.0'

def test_invalid_mode(client):
    """Test invalid mode"""
    response = client.post('/api/analyze',
        json={'text': 'Test text'},
        content_type='application/json'
    )
    assert response.status_code == 200
