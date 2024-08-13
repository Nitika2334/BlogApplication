import pytest
from flask_jwt_extended import create_access_token
from unittest.mock import patch, MagicMock
from uuid import UUID

@pytest.fixture
def mock_update_post(mocker):
    return mocker.patch('App.api.wrapper.utils.update_post', autospec=True)


def test_update_post_success(mock_update_post, test_client):
    post_id = UUID('a243d45d-4281-4c8f-bfb2-276ebdc55276')
    user_id = '56d65ec9-db08-42d5-9a56-303affb4fd81'  # The user making the update request

    access_token = create_access_token(identity=user_id)

    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    # Data to be updated
    data = {
        'title': 'Updated Title',
        'content': 'Updated content'
    }

    # Simulate a successful update
    mock_update_post.return_value = (
        {
            'message': 'Post updated successfully.',
            'status': True,
            'type': 'success_message',
            'error_status': {'error_code': '00000'}
        },
        200
    )

    # Perform the PUT request
    response = test_client.put(f'/api/v1/post/{post_id}', headers=headers, json=data)

    # Ensure the mock was called once with the correct parameters
    mock_update_post.assert_called_once_with(post_id, data)

    # Check the response status code and content
    assert response.status_code == 200
    assert response.json['message'] == 'Post updated successfully.'

# def test_update_post_unauthorized(mock_update_post, test_client):
#     post_id = UUID('a243d45d-4281-4c8f-bfb2-276ebdc55276')
#     user_id = '56d65ec9-db08-42d5-9a56-303affb4fd81'

#     access_token = create_access_token(identity=user_id)

#     headers = {
#         'Authorization': f'Bearer {access_token}'
#     }

#     mock_update_post.return_value = (
#         {
#             'message': 'You are not authorized to update this post.',
#             'status': False,
#             'type': 'custom_error',
#             'error_status': {'error_code': '40006'}
#         },
#         400
#     )

#     data = {
#         'title': 'Updated Title',
#         'content': 'Updated content'
#     }

#     response = test_client.put(f'/api/v1/post/{post_id}', headers=headers, json=data)

#     # assert mock_update_post.call_count == 1, "The update_post function was not called."

#     mock_update_post.assert_called_once_with(post_id, data)
#     assert response.status_code == 400
#     assert response.json['message'] == 'You are not authorized to update this post.'
    
# def test_update_post_missing_data(mock_update_post, test_client):
#     post_id = UUID('a243d45d-4281-4c8f-bfb2-276ebdc55276')
#     user_id = '56d65ec9-db08-42d5-9a56-303affb4fd81'  # The user making the update request

#     access_token = create_access_token(identity=user_id)

#     headers = {
#         'Authorization': f'Bearer {access_token}'
#     }

#     # Simulate missing data
#     data = {}

#     mock_update_post.return_value = (
#         {
#             'message': 'Title, content, or image is required.',
#             'status': False,
#             'type': 'custom_error',
#             'error_status': {'error_code': '40007'}
#         },
#         400
#     )

#     # Perform the PUT request
#     response = test_client.put(f'/api/v1/post/{post_id}', headers=headers, json=data)

#     # Ensure the mock was called once with the correct parameters
#     mock_update_post.assert_called_once_with(post_id, data)

#     # Check the response status code and content
#     assert response.status_code == 400
#     assert response.json['message'] == 'Title, content, or image is required.'
