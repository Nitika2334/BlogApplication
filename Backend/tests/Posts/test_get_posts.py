import pytest
from flask_jwt_extended import create_access_token
from unittest.mock import MagicMock
from uuid import UUID

@pytest.fixture
def mock_get_post_by_id(mocker):
    return mocker.patch('App.api.wrapper.utils.get_post', autospec=True)

def test_get_post_successful(mock_get_post_by_id, test_client):
    post_id = UUID('fe60736f-6251-4f8d-a0c5-308830ddc4a9')
    user_id = 'bb87a1de-23fb-4a0b-8b4e-b85e4aaacdfa'

    access_token = create_access_token(identity=user_id)

    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    mock_get_post_by_id.return_value = (
        {
            "message": "Post retrieved successfully",
            "status": True,
            "type": "success_message",
            "error_status": {
                "error_code": "00000"
            },
            "data": {
                "uid": str(post_id),
                "title": "Post23",
                "content": "content",
                "user_uid": user_id,
                "created_at": "2024-08-13T10:59:42.999714",
                "updated_at": "2024-08-13T10:59:42.999724",
                "image": None
            }
        },
        200
    )

    response = test_client.get(f'/api/v1/post/{post_id}', headers=headers)

    assert response.status_code == 200
    assert response.json['message'] == 'Post retrieved successfully'
    assert 'data' in response.json
    assert response.json['data']['uid'] == str(post_id)
    assert response.json['data']['title'] == 'Post23'
    assert response.json['data']['content'] == 'content'
    assert response.json['data']['user_uid'] == user_id
    assert response.json['data']['image'] is None

def test_delete_no_token(mock_get_post_by_id, test_client):
    # Prepare test data
    post_id = '9a5a1ab5-e305-455b-9735-13e90e346256'

    # Perform a DELETE request to the delete comment endpoint without an Authorization header
    response = test_client.delete(f'/api/v1/post')

    # Ensure the mock was not called
    mock_get_post_by_id.assert_not_called()

    # Check the response status code and content
    assert response.status_code == 401  # Unauthorized
    assert response.json['msg'] == 'Missing Authorization Header'


# def test_get_post_not_found(mock_get_post_by_id, test_client):
#     post_id = UUID('a243d45d-4281-4c8f-bfbb-276ebdc5527b')
#     user_id = 'bb87a1de-23fb-4a0b-8b4e-b85e4aaacdfa'

#     access_token = create_access_token(identity=user_id)

#     headers = {
#         'Authorization': f'Bearer {access_token}'
#     }

#     # Simulate post not found
#     mock_get_post_by_id.return_value = (
#         {
#             "message": "Post not found",
#             "status": False,
#             "type": "custom_error",
#             "error_status": {
#                 "error_code": "40008"
#             }
#         },
#         404
#     )

#     response = test_client.get(f'/api/v1/post/{post_id}', headers=headers)

#     print("Response status code:", response.status_code)
#     print("Response JSON:", response.json)

#     # Check the response status code and content
#     assert response.status_code == 400
#     assert response.json['message'] == 'Post not found'
