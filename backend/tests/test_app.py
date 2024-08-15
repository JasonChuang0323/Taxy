import pytest
from app import create_app

@pytest.fixture
def client():
    # Create a Flask test client
    app = create_app()
    with app.test_client() as client:
        yield client

def test_home(client):
    # Test the home route
    rv = client.get('/')
    assert rv.status_code == 200
    assert rv.data == b'Hello, welcome!'

def test_greet(client):
    rv = client.post('/api/greet', json={'name': 'Jason'})
    assert rv.status_code == 200
    assert rv.json == {'message': 'Hello, Jason!'}

def test_greet_default_name(client):
    rv = client.post('/api/greet', json={})
    assert rv.status_code == 200
    assert rv.json == {'message': 'Hello, Stranger!'}
