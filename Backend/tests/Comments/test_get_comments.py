import pytest
from unittest.mock import MagicMock
from flask_jwt_extended import create_access_token
from uuid import UUID

@pytest.fixture
def mock_get_comments(mocker):
    return mocker.patch('App.api.wrapper.utils.get_comments', autospec=True)

def test_get_comments_success(mock_get_comments, test_client):
    # Prepare test data
    post_uid = 'c6d8f7a6-fd60-4a6b-9478-d6a2f21b6f5f'
    user_uid = '2ce3f6ff-0420-455f-853d-13bdd1df3121'

    # Generate a JWT token using user_uid
    access_token = create_access_token(identity=user_uid)

    # Set the headers with the JWT token
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    # Mock the function to return a success response
    mock_get_comments.return_value = (
        {
            'message': 'Comments retrieved successfully',
            'status': True,
            'type': 'success_message',
            'error_status': {'error_code': '00000'},
            'data': [
                {
                    'comment_id': str(UUID('9a5a1ab5-e305-455b-9735-13e90e346256')),
                    'content': 'Good',
                }
            ]
        }, 200
    )

    # Perform a GET request to the comments retrieval endpoint
    response = test_client.get(f'api/v1/posts/{post_uid}/comments', headers=headers)

    # Ensure the mock was called with the correct arguments
    mock_get_comments.assert_called_once_with(UUID(post_uid))

    # Check the response status code and content
    assert response.status_code == 200
    assert response.json['message'] == 'Comments retrieved successfully'
    assert len(response.json['data']) == 1
    assert response.json['data'][0]['comment_id'] == str(UUID('9a5a1ab5-e305-455b-9735-13e90e346256'))
    assert response.json['data'][0]['content'] == 'Good'


def test_get_no_token(mock_get_comments, test_client):
    # Prepare test data
    post_uid = 'c6d8f7a6-fd60-4a6b-9478-d6a2f21b6f5f'

    # Perform a GET request to the comments retrieval endpoint without an Authorization header
    response = test_client.get(f'/api/v1/posts/{post_uid}/comments')

    # Ensure the mock was not called
    mock_get_comments.assert_not_called()

    # Check the response status code and content
    assert response.status_code == 401  # Unauthorized
    assert response.json['msg'] == 'Missing Authorization Header'
