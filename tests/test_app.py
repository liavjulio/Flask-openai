import pytest
import os
from app import create_app, db

@pytest.fixture
def app():
    # Set the testing configuration first
    os.environ['DATABASE_URL'] = 'sqlite:///mydatabase.db'  # Set a temporary database URI for testing
    app = create_app()

    with app.app_context():
        # Create the database and the database table
        db.create_all()

        yield app

        # Drop the database and the database table
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_ask_endpoint(client):
    response = client.post('/ask', json={'question': 'What is the capital of France?'})
    data = response.get_json()
    assert response.status_code == 200
    assert 'question' in data
    assert 'answer' in data
    print("Response data:", data)  # Debugging line
