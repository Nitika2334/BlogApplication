import pytest
from unittest.mock import MagicMock
from flask_jwt_extended import create_access_token
from uuid import UUID

@pytest.fixture
def mock_get_comments(mocker):
    return mocker.patch('App.api.wrapper.utils.get_comments', autospec=True)



def test_get_comments_success(mock_get_comments, test_client):
    # Prepare test data
    post_uid = '40cba3fd-8341-470b-946c-f778a75e03aa'
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
                    'comment_id': str(UUID(post_uid)),
                    'content': 'Nice',
                }
            ]
        }, 200
    )
    # Perform a GET request to the comments retrieval endpoint
    response = test_client.get(f'api/v1/posts/{post_uid}/comments', headers=headers)

    print(f"Mock get_comments call args: {mock_get_comments.call_args_list}")
    print(f"Response: {response.get_json()}")

    # Ensure the mock was called with the correct arguments
    mock_get_comments.assert_called_once_with(UUID(post_uid))

    # Check the response status code and content
    assert response.status_code == 200
    assert response.json['message'] == 'Comments retrieved successfully'
    assert len(response.json['data']) == 1
    assert response.json['data'][0]['comment_id'] == str(UUID(post_uid))
    assert response.json['data'][0]['content'] == 'Nice'


def test_get_no_token(mock_get_comments, test_client):
    # Prepare test data
    post_uid = '40cba3fd-8341-470b-946c-f778a75e03aa'

    # Perform a GET request to the comments retrieval endpoint without an Authorization header
    response = test_client.get(f'/api/v1/posts/{post_uid}/comments')

    # Ensure the mock was not called
    mock_get_comments.assert_not_called()

    # Check the response status code and content
    assert response.status_code == 401  # Unauthorized
    assert response.json['msg'] == 'Missing Authorization Header'
