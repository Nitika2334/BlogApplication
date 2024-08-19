import pytest
from unittest.mock import MagicMock
from flask_jwt_extended import create_access_token
from uuid import UUID
from datetime import datetime
from App.Models.Comment.CommentModel import Comment

@pytest.fixture
def mock_update_comment(mocker):
    return mocker.patch('App.api.wrapper.utils.update_comment', autospec=True)

# @pytest.fixture
# def mock_get_comment_by_comment_id(mocker):
#     return mocker.patch('App.api.wrapper.schema.get_comment_by_comment_id', autospec=True)

@pytest.fixture
def mock_get_comment_by_comment_id(mocker):
    return mocker.patch('App.api.wrapper.schema.get_comment_by_comment_id', autospec=True)


def test_update_comment_success(mock_update_comment, test_client):
    # Prepare test data
    comment_uid = '853d4bc5-88fe-4408-bf3f-194e78d76057'
    user_uid = '2ce3f6ff-0420-455f-853d-13bdd1df3121'
    data = {'content': 'Updated comment'}

    # Generate a JWT token using user_uid
    access_token = create_access_token(identity=user_uid)

    # Set the headers with the JWT token
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    # Mock the function to return a success response
    mock_update_comment.return_value = (
        {
            'message': 'Comment updated successfully',
            'status': True,
            'type': 'success_message',
            'error_status': {'error_code': '00000'},
            'data': {
                'comment_id': str(comment_uid),
                'content': 'Updated comment',
                'updated_at': '2024-08-09T07:32:29Z'
            }
        }, 200
    )

    # Perform a PUT request to the comment update endpoint
    response = test_client.put(f'api/v1/comments/{comment_uid}', json=data, headers=headers)

    # Ensure the mock was called with correct arguments
    mock_update_comment.assert_called_once_with(data, UUID(comment_uid), user_uid)

    # Check the response status code and content
    assert response.status_code == 200
    assert response.json['message'] == 'Comment updated successfully'



def test_create_comment_missing_content(mock_update_comment, test_client):
    # Prepare test data
    comment_uid = '853d4bc5-88fe-4408-bf3f-194e78d76057'
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
    response = test_client.put(f'/api/v1/comments/{comment_uid}', json=data, headers=headers)

    # Ensure the mock was not called since content is missing
    mock_update_comment.assert_not_called()

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


def test_update_no_token(mock_update_comment, test_client):
    # Prepare test data
    comment_uid = '853d4bc5-88fe-4408-bf3f-194e78d76057'
    data = {'content': 'Updated comment'}

    # Perform a PUT request to the update comment endpoint without an Authorization header
    response = test_client.put(f'/api/v1/comments/{comment_uid}', json=data)

    # Ensure the mock was not called
    mock_update_comment.assert_not_called()

    # Check the response status code and content
    assert response.status_code == 401  # Unauthorized
    assert response.json['msg'] == 'Missing Authorization Header'


