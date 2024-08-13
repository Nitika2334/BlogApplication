import pytest
from unittest.mock import MagicMock
from flask_jwt_extended import create_access_token

@pytest.fixture
def mock_register_user(mocker):
    return mocker.patch('App.api.wrapper.utils.user_register', autospec=True)

@pytest.fixture
def mock_validate_email(mocker):
    return mocker.patch('App.api.wrapper.utils.validate_email', autospec=True)

def test_register_success(mock_register_user, mock_validate_email, test_client):
    # Prepare test data
    data = {
        'username': 'newuser',
        'email': 'newuser@example.com',
        'password': 'StrongPassword123!'
    }

    # Mocks setup
    mock_validate_email.return_value = True
    mock_register_user.return_value = ({
        'message': 'User registered successfully.',
        'status': True,
        'type': 'success_message',
        'error_status': {'error_code': '00000'},
        'data': {
            'user_id': '1',
            'access_token': 'token',
            'username': 'newuser',
            'email': 'newuser@example.com'
        }
    }, 200)

    # Perform a POST request to the register endpoint
    response = test_client.post('/api/v1/register', json=data)

    # Ensure the mock was called with the correct data
    mock_register_user.assert_called_once_with(data)

    # Check the response status code and content
    assert response.status_code == 200
    assert response.json['message'] == 'User registered successfully.'

def test_register_missing_field(mock_register_user, mock_validate_email, test_client):
    # Prepare test data with a missing field
    data = {
        'username': 'new'
    }

    # Mocks setup
    mock_validate_email.return_value = {
        "message": "Title and content are required",
        "status": False,
        "type": "custom_error",
        "error_status": {
            "error_code": "40012"
        }
    }

    # Perform a POST request to the register endpoint with missing email
    response = test_client.post('/api/v1/register', json=data)

    print(response.status_code)

    # Ensure the mock was not called since the request is invalid
    mock_register_user.assert_not_called()

    # Check the response status code and content
    assert response.status_code == 400  # Bad Request
    assert response.json == {
        "message": "Please provide username, email, and password.",
        "status": False,
        "type": "custom_error",
        "error_status": {"error_code": "40001"}
    }

def test_register_username_exists(mock_register_user, mock_validate_email, test_client):
    # Prepare test data
    data = {
        'username': 'existinguser',
        'email': 'newuser@example.com',
        'password': 'StrongPassword123!'
    }

    # Mocks setup
    mock_validate_email.return_value = True
    mock_register_user.return_value = ({
        'message': 'Username already exists.',
        'status': False,
        'type': 'custom_error',
        'error_status': {'error_code': '40002'}
    }, 400)

    # Perform a POST request to the register endpoint
    response = test_client.post('/api/v1/register', json=data)

    # Ensure the mock was called with the correct data
    mock_register_user.assert_called_once_with(data)

    print(response.status_code)

    # Check the response status code and content
    assert response.status_code == 400  # Bad Request
    assert response.json == {
        "message": "Username already exists.",
        "status": False,
        "type": "custom_error",
        "error_status": {"error_code": "40002"}
    }

def test_register_email_exists(mock_register_user, mock_validate_email, test_client):
    # Prepare test data
    data = {
        'username': 'newuser',
        'email': 'existing@example.com',
        'password': 'StrongPassword123!'
    }

    # Mocks setup
    mock_validate_email.return_value = True
    mock_register_user.return_value = ({
        'message': 'Email already exists.',
        'status': False,
        'type': 'custom_error',
        'error_status': {'error_code': '40002'}
    }, 400)

    # Perform a POST request to the register endpoint
    response = test_client.post('/api/v1/register', json=data)

    # Ensure the mock was called with the correct data
    mock_register_user.assert_called_once_with(data)

    # Check the response status code and content
    assert response.status_code == 400  # Bad Request
    assert response.json == {
        "message": "Email already exists.",
        "status": False,
        "type": "custom_error",
        "error_status": {"error_code": "40002"}
    }
