import pytest
import json
from os import environ
from app import create_app

API_TOKEN = environ.get('API_TOKEN')

headers = {
    'Authorization': f'Bearer {API_TOKEN}',
}

@pytest.fixture()
def app():
    app = create_app()
    app.config.update({
        'TESTING': True,
        'SECRET_KEY': 'mysecretkey'
    })
    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


def test_home(client):
    response = client.get('/')
    assert response.status_code == 200


def test_token(client):
    #Test the GET endpoint with API_TOKEN"
    response = client.get('/data', headers=headers)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, dict)

def test_batch(client):
    json_data = {
        "table": "employees",
        "rows": [
            {"id": 9998, "name": "John Doe", "datetime": "2009-09-27 18:00:00.000", "department_id": 1, "job_id": 2},
            {"id": 9999, "name": "Jane Smith", "datetime": "2011-02-22 13:32:00.000", "department_id": 1, "job_id": 3}
        ]
    }
    response = client.post('/batch_insert', json=json_data, headers=headers)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'Data successfully uploaded' in data.get('message')

def test_queries(client):
    response = client.get('/employees_by_quarter', headers=headers)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'Data from employees was queried succesfully' in data.get('message')
    response = client.get('/employees_hired', headers=headers)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'Data from employees was queried succesfully' in data.get('message')
