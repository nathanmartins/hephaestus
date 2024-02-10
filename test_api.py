import json
import pytest
from api import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_hello(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.data.decode('utf-8') == 'Hello Palenca'


def test_valid_login(client):
    credentials = {'email': 'pierre@palenca.com', 'password': 'MyPwdChingon123'}
    response = client.post('/uber/login', json=credentials)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'access_token' in data


def test_invalid_email_format(client):
    invalid_credentials = {'email': 'invalidemail', 'password': 'MyPwdChingon123'}
    response = client.post('/uber/login', json=invalid_credentials)
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data['message'] == 'INVALID_EMAIL_FORMAT'


def test_invalid_password(client):
    invalid_credentials = {'email': 'pierre@palenca.com', 'password': '123'}
    response = client.post('/uber/login', json=invalid_credentials)
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data['message'] == 'INVALID_PASSWORD'


def test_invalid_credentials(client):
    invalid_credentials = {'email': 'invalid@palenca.com', 'password': 'InvalidPwd'}
    response = client.post('/uber/login', json=invalid_credentials)
    assert response.status_code == 401
    data = json.loads(response.data)
    assert data['message'] == 'CREDENTIALS_INVALID'


