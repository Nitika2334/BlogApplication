import pytest
from flask_jwt_extended import create_access_token
from unittest.mock import MagicMock

@pytest.fixture
def mock_create_post_db(mocker):
    return mocker.patch('App.api.wrapper.schema.create_post', autospec=True)

@pytest.fixture
def access_token():
    # Use a fixed user ID for testing
    return create_access_token(identity='user_id')

def test_create_post_successful(mock_create_post_db, test_client, access_token):
    data = {
        'title': 'New Post',
        'content': 'This is a new post.',
        'user_uid': 'bb87a1de-23fb-4a0b-8b4e-b85e4aaacdfa'
    }

    mock_create_post_db.return_value = MagicMock(uid='123', title='New Post', content='This is a new post.', image=None)

    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    response = test_client.post('/api/v1/post', json=data, headers=headers)

    # Check the create_post function is called with the correct arguments
    mock_create_post_db.assert_called_once_with(data['title'], data['content'], 'user_id', None)

    assert response.status_code == 200
    assert response.json['message'] == 'Post created successfully'
    assert response.json['status'] is True
    assert response.json['data']['title'] == 'New Post'
    assert response.json['data']['image_url'] is None

def test_create_post_missing_fields(mock_create_post_db, test_client, access_token):
    data = {
        'title': '',
        'content': ''
    }

    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    response = test_client.post('/api/v1/post', json=data, headers=headers)

    mock_create_post_db.assert_not_called()

    assert response.status_code == 400
    assert response.json == {
	"message": "Title and content are required",
	"status": False,
	"type": "custom_error",
	"error_status": {
		"error_code": "40012"
	}
}


def test_create_post_unauthorized(test_client):
    data = {
        'title': 'New Post',
        'content': 'This is a new post.'
    }

    response = test_client.post('/api/v1/post', json=data)

    assert response.status_code == 401
    assert response.json['msg'] == 'Missing Authorization Header'

def test_create_post_invalid_token(test_client):
    data = {
        'title': 'New Post',
        'content': 'This is a new post.'
    }

    headers = {
        'Authorization': 'Bearer invalid_token'
    }

    response = test_client.post('/api/v1/post', json=data, headers=headers)

    assert response.status_code == 422
    assert response.json['msg'] == 'Not enough segments'