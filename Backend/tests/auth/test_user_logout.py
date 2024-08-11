import pytest
from flask_jwt_extended import create_access_token

@pytest.fixture
def mock_user_logout(mocker):
    return mocker.patch('App.api.wrapper.utils.user_logout', autospec=True)

def test_logout_success(mock_user_logout, test_client):
    # Prepare test data
    user_uid = '2ce3f6ff-0420-455f-853d-13bdd1df3121'

    # Generate a JWT token for the user
    access_token = create_access_token(identity=user_uid)

    # Set the headers with the JWT token
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    # Mock the function to return a success response
    mock_user_logout.return_value = (
        {
            'message': 'User logged out successfully',
            'status': True,
            'type': 'success_message',
            'error_status': {'error_code': '00000'}
        }, 200
    )

    # Perform a POST request to the logout endpoint
    response = test_client.post('/api/v1/logout', headers=headers)

    # Ensure the mock was called with the correct arguments (adjust if necessary)
    mock_user_logout.assert_called_once()

    # Check the response status code and content
    assert response.status_code == 200
    assert response.json['message'] == 'User logged out successfully'
    assert response.json['status'] is True
    assert response.json['type'] == 'success_message'
    assert response.json['error_status']['error_code'] == '00000'


def test_logout_no_token(mock_user_logout, test_client):
    # Prepare the test data
    user_uid = '2ce3f6ff-0420-455f-853d-13bdd1df3121'

    # Perform a POST request to the logout endpoint without an Authorization header
    response = test_client.post('/api/v1/logout')

    # Ensure the mock was not called
    mock_user_logout.assert_not_called()

    # Check the response status code
    assert response.status_code == 401  # Unauthorized

    assert response.json['msg'] == 'Missing Authorization Header'