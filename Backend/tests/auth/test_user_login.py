from unittest.mock import MagicMock
from App.Models.User.UserModel import User
import pytest
from flask_bcrypt import generate_password_hash

@pytest.fixture
def mock_user_model(mocker):
    mock_model = mocker.patch('App.Models.User.UserModel.User')
    return mock_model

def test_user_login_success(test_client, mock_user_model):
    response = test_client.post('/api/v1/login', json={'username': 'Sahil', 'password': 'Sahil@1234'})
    
    assert response.status_code == 200
    response_data = response.get_json()
    assert response_data['status'] is True
    assert response_data['message'] == 'User logged in successfully'
    assert response_data['type'] == 'success_message'
    assert response_data['error_status']['error_code'] == '00000'
    assert 'access_token' in response_data['data']
    assert response_data['data']['username'] == 'Sahil'

def test_user_login_invalid_credentials(test_client,mock_user_model):

    response = test_client.post('/api/v1/login', json={'username': 'Sahil', 'password': 'Sahil@12'})
    
    assert response.status_code == 400
    response_data = response.get_json()
    assert response_data['status'] is False
    assert response_data['message'] == 'Invalid credentials'
    assert response_data['type'] == 'custom_error'
    assert response_data['error_status']['error_code'] == '40004'

def test_user_login_user_not_found(test_client, mock_user_model):

    response = test_client.post('/api/v1/login', json={'username': 'Nitika', 'password': 'Nitika@1234'})
    
    assert response.status_code == 400
    response_data = response.get_json()
    assert response_data['status'] is False
    assert response_data['message'] == 'Invalid credentials'
    assert response_data['type'] == 'custom_error'
    assert response_data['error_status']['error_code'] == '40004'
