import pytest
from unittest.mock import MagicMock
from flask_jwt_extended import create_access_token
from uuid import UUID
@pytest.fixture
def mock_create_comment(mocker):
    return mocker.patch('App.api.wrapper.utils.create_comment', autospec=True)

def test_create_comment_is_success(mock_create_comment, test_client):
    # Prepare test data
    post_uid = 'c6d8f7a6-fd60-4a6b-9478-d6a2f21b6f5f'
    user_uid = '2ce3f6ff-0420-455f-853d-13bdd1df3121'
    data = {'content': 'Test comment'}

    # Generate a JWT token using user_uid
    access_token = create_access_token(identity=user_uid)

    # Set the headers with the JWT token
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    mock_create_comment.return_value = ({'message': 'Comment created successfully'}, 200)
    # Perform a POST request to the comment creation endpoint
    response = test_client.post(f'api/v1/posts/{post_uid}/comments', json=data, headers=headers)

     # Ensure the mock was called
    mock_create_comment.assert_called_once_with(data, UUID(post_uid), user_uid)

    assert response.status_code==200
    assert response.json['message'] == 'Comment created successfully'

def test_create_comment_missing_content(mock_create_comment, test_client):
    # Prepare test data
    post_uid = 'c6d8f7a6-fd60-4a6b-9478-d6a2f21b6f5f'
    user_uid = '2ce3f6ff-0420-455f-853d-13bdd1df3121'

    # Generate a JWT token using user_uid
    access_token = create_access_token(identity=user_uid)

    # Set the headers with the JWT token
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    # Data with missing content (empty JSON object)
    data = {}

    # Perform a POST request to the comment creation endpoint with empty JSON body
    response = test_client.post(f'/api/v1/posts/{post_uid}/comments', json=data, headers=headers)

    # Ensure the mock was not called since content is missing
    mock_create_comment.assert_not_called()

    # Print response for debugging
    print(response.get_json())

    # Check the response status code and content
    assert response.status_code == 400  # Bad Request
    assert response.json == {
        "message": "Content is required",
        "status": False,
        "type": "custom_error",
        "error_status": {"error_code": "40012"}
    }
   
def test_create_no_token(mock_create_comment, test_client):
    # Prepare test data
    data = {'content': 'New comment'}
    post_uid = 'c6d8f7a6-fd60-4a6b-9478-d6a2f21b6f5f'

    # Perform a POST request to the create comment endpoint without an Authorization header
    response = test_client.post(f'/api/v1/posts/{post_uid}/comments', json=data)

    # Ensure the mock was not called
    mock_create_comment.assert_not_called()

    # Check the response status code and content
    assert response.status_code == 401  # Unauthorized
    assert response.json['msg'] == 'Missing Authorization Header'

