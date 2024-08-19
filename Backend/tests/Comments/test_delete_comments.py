import pytest
from unittest.mock import MagicMock
from flask_jwt_extended import create_access_token
from uuid import UUID

@pytest.fixture
def mock_delete_comment(mocker):
    return mocker.patch('App.api.wrapper.utils.delete_comment', autospec=True)

def test_delete_comment_success(mock_delete_comment, test_client):
    # Prepare test data
    comment_uid = '853d4bc5-88fe-4408-bf3f-194e78d76057'
    user_uid = '2ce3f6ff-0420-455f-853d-13bdd1df3121'

    # Generate a JWT token using user_uid
    access_token = create_access_token(identity=user_uid)

    # Set the headers with the JWT token
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    # Mock the function to return a success response
    mock_delete_comment.return_value = (
        {
            'message': 'Comment deleted successfully',
            'status': True,
            'type': 'success_message',
            'error_status': {'error_code': '00000'}
        }, 200
    )

    # Perform a DELETE request to the comment deletion endpoint
    response = test_client.delete(f'api/v1/comments/{comment_uid}', headers=headers)

    # Ensure the mock was called with correct arguments
    mock_delete_comment.assert_called_once_with(UUID(comment_uid), user_uid)

    # Check the response status code and content
    assert response.status_code == 200
    assert response.json['message'] == 'Comment deleted successfully'

def test_delete_no_token(mock_delete_comment, test_client):
    # Prepare test data
    comment_uid = '853d4bc5-88fe-4408-bf3f-194e78d76057'

    # Perform a DELETE request to the delete comment endpoint without an Authorization header
    response = test_client.delete(f'/api/v1/comments/{comment_uid}')

    # Ensure the mock was not called
    mock_delete_comment.assert_not_called()

    # Check the response status code and content
    assert response.status_code == 401  # Unauthorized
    assert response.json['msg'] == 'Missing Authorization Header'