import pytest
from flask_jwt_extended import create_access_token
from unittest.mock import MagicMock, patch
from uuid import UUID

@pytest.fixture
def mock_delete_post(mocker):
    return mocker.patch('App.api.wrapper.utils.delete_post', autospec=True)

# Test for successful deletion
def test_delete_post_successful(mock_delete_post, test_client):
    post_id = UUID('a243d45d-4281-4c8f-bfb2-276ebdc55276')  # Use UUID object
    user_id = 'bb87a1de-23fb-4a0b-8b4e-b85e4aaacdfa'

    access_token = create_access_token(identity=user_id)

    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    # Mock return value should be a tuple
    mock_delete_post.return_value = (
        {
            "message": "Post deleted successfully.",
            "status": True,
            "type": "success_message",
            "error_status": {"error_code": "00000"}
        },
        200
    )

    response = test_client.delete(f'/api/v1/post/{post_id}', headers=headers)

    print(response.data)

    mock_delete_post.assert_called_once_with(post_id, user_id)

    # Check the response status code and content
    assert response.status_code == 200
    assert response.json['message'] == 'Post deleted successfully.'

def test_delete_no_token(mock_delete_post, test_client):
    # Prepare test data
    post_id = '9a5a1ab5-e305-455b-9735-13e90e346256'

    # Perform a DELETE request to the delete comment endpoint without an Authorization header
    response = test_client.delete(f'/api/v1/comments/{post_id}')

    # Ensure the mock was not called
    mock_delete_post.assert_not_called()

    # Check the response status code and content
    assert response.status_code == 401  # Unauthorized
    assert response.json['msg'] == 'Missing Authorization Header'

from unittest.mock import patch

@patch('App.api.wrapper.utils.delete_post')
def test_delete_post_unauthorized(mock_delete_post, test_client):
    post_id = UUID('a243d45d-4281-4c8f-bfb2-276ebdc55276')
    user_id = '56d65ec9-db08-42d5-9a56-303affb4fd81'

    access_token = create_access_token(identity=user_id)

    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    # Mock return value for unauthorized access
    mock_delete_post.return_value = (
        {
            'message': 'You are not authorized to delete this post.',
            'status': False,
            'type': 'custom_error',
            'error_status': {'error_code': '40006'}
        },
        400
    )

    response = test_client.delete(f'/api/v1/post/{post_id}', headers=headers)

    assert response.status_code == 400
    assert response.json['message'] == 'You are not authorized to delete this post.'
