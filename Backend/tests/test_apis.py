import pytest
from unittest.mock import patch
from flask_jwt_extended import create_access_token
from uuid import UUID


# Register 
def test_register_success(test_client, mocker):
    # Mock the user_register function to simulate a successful registration
    mock_user_register = mocker.patch('App.api.wrapper.apis.user_register', return_value=({
        'message': 'User registered successfully',
        'status': True,
        'type': 'success_message',
        'error_status': {'error_code': '00000'}
    }, 200))

    # Prepare test data
    data = {
        'username': 'test_user',
        'email': 'test@example.com',
        'password': 'password123'
    }

    # Send POST request to RegisterResource endpoint
    response = test_client.post('api/v1/register', json=data)
    
    # Assert response and status code
    assert response.status_code == 200
    assert response.json == {
        'message': 'User registered successfully',
        'status': True,
        'type': 'success_message',
        'error_status': {'error_code': '00000'}
    }

    # Ensure the user_register function was called with the correct data
    mock_user_register.assert_called_once_with(data)

def test_register_failure(test_client, mocker):
    # Mock the user_register function to simulate a registration failure
    mock_user_register = mocker.patch('App.api.wrapper.apis.user_register', side_effect=Exception("Registration failed"))

    # Prepare test data
    data = {
        'username': 'test_user',
        'email': 'test@example.com',
        'password': 'password123'
    }

    # Send POST request to RegisterResource endpoint
    response = test_client.post('/api/v1/register', json=data)
    
    # Assert response and status code
    assert response.status_code == 400
    assert response.json == {
        'message': 'Registration failed',
        'status': False,
        'type': 'custom_error',
        'error_status': {'error_code': '40003'}
    }

    # Ensure the user_register function was called with the correct data
    mock_user_register.assert_called_once_with(data)


# Login 
def test_login_success(test_client, mocker):
    # Mocking the user_login function to return a successful response
    mock_user_login = mocker.patch('App.api.wrapper.apis.user_login', return_value=(
        {
            'message': 'Login successful',
            'status': True,
            'data': {
                'access_token': 'test_token',
            }
        }, 200
    ))

    # Simulate a POST request to the login endpoint
    response = test_client.post('/api/v1/login', json={'username': 'testuser', 'password': 'testpassword'})

    # Assertions
    assert response.status_code == 200
    assert response.json['message'] == 'Login successful'
    assert response.json['status'] is True
    assert 'access_token' in response.json['data']

    # Ensure that user_login was called with the correct data
    mock_user_login.assert_called_once_with({'username': 'testuser', 'password': 'testpassword'})


def test_login_failure(test_client, mocker):
    # Mocking the user_login function to raise an exception
    mock_user_login = mocker.patch('App.api.wrapper.apis.user_login', side_effect=Exception('Login failed'))

    # Simulate a POST request to the login endpoint
    response = test_client.post('/api/v1/login', json={'username': 'testuser', 'password': 'wrongpassword'})

    # Assertions
    assert response.status_code == 400
    assert response.json['message'] == 'Login failed'
    assert response.json['status'] is False
    assert response.json['type'] == 'custom_error'
    assert response.json['error_status']['error_code'] == '40003'

    # Ensure that user_login was called with the correct data
    mock_user_login.assert_called_once_with({'username': 'testuser', 'password': 'wrongpassword'})


# User logout 
def test_logout_success(test_client, mocker):
    # Mocking the user_logout function to return a successful response
    mock_user_logout = mocker.patch('App.api.wrapper.apis.user_logout', return_value=(
        {
            'message': 'Logout successful',
            'status': True
        }, 200
    ))

    # Creating a JWT token for testing
    access_token = create_access_token(identity='testuser')

    # Simulate a POST request to the logout endpoint with the JWT token
    response = test_client.post('/api/v1/logout', headers={'Authorization': f'Bearer {access_token}'})

    # Assertions
    assert response.status_code == 200
    assert response.json['message'] == 'Logout successful'
    assert response.json['status'] is True

    # Ensure that user_logout was called once
    mock_user_logout.assert_called_once()


def test_logout_failure(test_client, mocker):
    # Mocking the user_logout function to raise an exception
    mock_user_logout = mocker.patch('App.api.wrapper.apis.user_logout', side_effect=Exception('Logout failed'))

    # Creating a JWT token for testing
    access_token = create_access_token(identity='testuser')

    # Simulate a POST request to the logout endpoint with the JWT token
    response = test_client.post('/api/v1/logout', headers={'Authorization': f'Bearer {access_token}'})

    # Assertions
    assert response.status_code == 400
    assert response.json['message'] == 'Logout failed'
    assert response.json['status'] is False
    assert response.json['type'] == 'custom_error'
    assert response.json['error_status']['error_code'] == '40003'

    # Ensure that user_logout was called once
    mock_user_logout.assert_called_once()


# Comments 

def test_get_comments_success(test_client, mocker):
    # Define a UUID object for testing
    test_post_id = UUID('123e4567-e89b-12d3-a456-426614174000')

    # Mocking the get_comments function to return a successful response
    mock_get_comments = mocker.patch('App.api.wrapper.apis.get_comments', return_value=(
        {
            'message': 'Comments retrieved successfully',
            'status': True,
            'data': [
                {'comment_id': '1', 'content': 'Test comment'}
            ]
        }, 200
    ))

    # Creating a JWT token for testing
    access_token = create_access_token(identity='testuser')

    # Simulate a GET request to the comments endpoint with UUID
    response = test_client.get(f'/api/v1/posts/{test_post_id}/comments', headers={'Authorization': f'Bearer {access_token}'})

    # Assertions
    assert response.status_code == 200
    assert response.json['message'] == 'Comments retrieved successfully'
    assert response.json['status'] is True
    assert len(response.json['data']) == 1

    # Ensure that get_comments was called with the correct UUID object
    mock_get_comments.assert_called_once_with(test_post_id)

def test_get_comments_failure(test_client, mocker):
    # Define a UUID object for testing
    test_post_id = UUID('123e4567-e89b-12d3-a456-426614174000')

    # Mocking the get_comments function to raise an exception
    mock_get_comments = mocker.patch('App.api.wrapper.apis.get_comments', side_effect=Exception('Failed to get comments'))

    # Creating a JWT token for testing
    access_token = create_access_token(identity='testuser')

    # Simulate a GET request to the comments endpoint with UUID
    response = test_client.get(f'/api/v1/posts/{test_post_id}/comments', headers={'Authorization': f'Bearer {access_token}'})

    # Assertions
    assert response.status_code == 400
    assert response.json['message'] == 'Failed to get comments'
    assert response.json['status'] is False
    assert response.json['type'] == 'custom_error'
    assert response.json['error_status']['error_code'] == '40005'

    # Ensure that get_comments was called with the correct UUID object
    mock_get_comments.assert_called_once_with(test_post_id)


def test_create_comment_success(test_client, mocker):
    # Define a UUID object for testing
    test_post_id = UUID('123e4567-e89b-12d3-a456-426614174000')

    # Mocking the create_comment function to return a successful response
    mock_create_comment = mocker.patch('App.api.wrapper.apis.create_comment', return_value=(
        {
            'message': 'Comment created successfully',
            'status': True,
            'data': {'comment_id': '1'}
        }, 201
    ))

    # Creating a JWT token for testing
    access_token = create_access_token(identity='testuser')

    # Simulate a POST request to the comments endpoint with UUID
    response = test_client.post(f'/api/v1/posts/{test_post_id}/comments', json={'content': 'Test comment'}, headers={'Authorization': f'Bearer {access_token}'})

    # Assertions
    assert response.status_code == 201
    assert response.json['message'] == 'Comment created successfully'
    assert response.json['status'] is True
    assert 'comment_id' in response.json['data']

    # Ensure that create_comment was called with the correct UUID object and data
    mock_create_comment.assert_called_once_with({'content': 'Test comment'}, test_post_id, 'testuser')
    
def test_create_comment_failure(test_client, mocker):
    # Define a UUID object for testing
    test_post_id = UUID('123e4567-e89b-12d3-a456-426614174000')

    # Mocking the create_comment function to raise an exception
    mock_create_comment = mocker.patch('App.api.wrapper.apis.create_comment', side_effect=Exception('Failed to create comment'))

    # Creating a JWT token for testing
    access_token = create_access_token(identity='testuser')

    # Simulate a POST request to the comments endpoint with UUID
    response = test_client.post(f'/api/v1/posts/{test_post_id}/comments', json={'content': 'Test comment'}, headers={'Authorization': f'Bearer {access_token}'})

    # Assertions
    assert response.status_code == 400
    assert response.json['message'] == 'Failed to create comment'
    assert response.json['status'] is False
    assert response.json['type'] == 'custom_error'
    assert response.json['error_status']['error_code'] == '40005'

    # Ensure that create_comment was called with the correct UUID object and data
    mock_create_comment.assert_called_once_with({'content': 'Test comment'}, test_post_id, 'testuser')


def test_update_comment_success(test_client, mocker):
    # Define a UUID object for testing
    test_comment_id = UUID('123e4567-e89b-12d3-a456-426614174000')

    # Mocking the update_comment function to return a successful response
    mock_update_comment = mocker.patch('App.api.wrapper.apis.update_comment', return_value=(
        {
            'message': 'Comment updated successfully',
            'status': True
        }, 200
    ))

    # Creating a JWT token for testing
    access_token = create_access_token(identity='testuser')

    # Simulate a PUT request to the comment endpoint with UUID
    response = test_client.put(f'/api/v1/comments/{test_comment_id}', json={'content': 'Updated comment'}, headers={'Authorization': f'Bearer {access_token}'})

    # Assertions
    assert response.status_code == 200
    assert response.json['message'] == 'Comment updated successfully'
    assert response.json['status'] is True

    # Ensure that update_comment was called with the correct UUID object and data
    mock_update_comment.assert_called_once_with({'content': 'Updated comment'}, test_comment_id, 'testuser')

def test_update_comment_failure(test_client, mocker):
    # Define a UUID object for testing
    test_comment_id = UUID('123e4567-e89b-12d3-a456-426614174000')

    # Mocking the update_comment function to raise an exception
    mock_update_comment = mocker.patch('App.api.wrapper.apis.update_comment', side_effect=Exception('Failed to update comment'))

    # Creating a JWT token for testing
    access_token = create_access_token(identity='testuser')

    # Simulate a PUT request to the comment endpoint with UUID
    response = test_client.put(f'/api/v1/comments/{test_comment_id}', json={'content': 'Updated comment'}, headers={'Authorization': f'Bearer {access_token}'})

    # Assertions
    assert response.status_code == 400
    assert response.json['message'] == 'Failed to update comment'
    assert response.json['status'] is False
    assert response.json['type'] == 'custom_error'
    assert response.json['error_status']['error_code'] == '40005'

    # Ensure that update_comment was called with the correct UUID object and data
    mock_update_comment.assert_called_once_with({'content': 'Updated comment'}, test_comment_id, 'testuser')


def test_delete_comment_success(test_client, mocker):
    # Define a UUID object for testing
    test_comment_id = UUID('123e4567-e89b-12d3-a456-426614174000')

    # Mocking the delete_comment function to return a successful response
    mock_delete_comment = mocker.patch('App.api.wrapper.apis.delete_comment', return_value=(
        {
            'message': 'Comment deleted successfully',
            'status': True
        }, 200
    ))

    # Creating a JWT token for testing
    access_token = create_access_token(identity='testuser')

    # Simulate a DELETE request to the comment endpoint with UUID
    response = test_client.delete(f'/api/v1/comments/{test_comment_id}', headers={'Authorization': f'Bearer {access_token}'})

    # Assertions
    assert response.status_code == 200
    assert response.json['message'] == 'Comment deleted successfully'
    assert response.json['status'] is True

    # Ensure that delete_comment was called with the correct UUID object
    mock_delete_comment.assert_called_once_with(test_comment_id, 'testuser')

def test_delete_comment_failure(test_client, mocker):
    # Define a UUID object for testing
    test_comment_id = UUID('123e4567-e89b-12d3-a456-426614174000')

    # Mocking the delete_comment function to raise an exception
    mock_delete_comment = mocker.patch('App.api.wrapper.apis.delete_comment', side_effect=Exception('Failed to delete comment'))

    # Creating a JWT token for testing
    access_token = create_access_token(identity='testuser')

    # Simulate a DELETE request to the comment endpoint with UUID
    response = test_client.delete(f'/api/v1/comments/{test_comment_id}', headers={'Authorization': f'Bearer {access_token}'})

    # Assertions
    assert response.status_code == 400
    assert response.json['message'] == 'Failed to delete comment'
    assert response.json['status'] is False
    assert response.json['type'] == 'custom_error'
    assert response.json['error_status']['error_code'] == '40005'

    # Ensure that delete_comment was called with the correct UUID object
    mock_delete_comment.assert_called_once_with(test_comment_id, 'testuser')

#Post

def test_create_post_success(test_client, mocker):
    # Mock the create_new_post function to return a successful response
    mock_create_new_post = mocker.patch('App.api.wrapper.apis.create_new_post', return_value=({
        'message': 'Post created successfully',
        'status': True
    }, 200))

    # Create a JWT token for testing
    access_token = create_access_token(identity='testuser')

    # Simulate a POST request to the post endpoint with JSON data
    post_data = {
        'title': 'Test Post',
        'content': 'This is a test post.',
        'image': None  # Include 'image' in the post data to match the function signature
    }
    response = test_client.post('/api/v1/post', json=post_data, headers={'Authorization': f'Bearer {access_token}'})

    # Assertions
    assert response.status_code == 200
    assert response.json['message'] == 'Post created successfully'
    assert response.json['status'] is True

    # Ensure that create_new_post was called with the correct data
    mock_create_new_post.assert_called_once_with(post_data)


def test_create_post_failure(test_client, mocker):
    # Mock the create_new_post function to raise an exception
    mock_create_new_post = mocker.patch('App.api.wrapper.apis.create_new_post', side_effect=Exception('Error creating post'))

    # Create a JWT token for testing
    access_token = create_access_token(identity='testuser')

    # Simulate a POST request to the post endpoint with JSON data
    post_data = {
        'title': 'Test Post',
        'content': 'This is a test post.',
        'image': None  # Include 'image' to match the function signature
    }
    response = test_client.post('/api/v1/post', json=post_data, headers={'Authorization': f'Bearer {access_token}'})

    # Assertions
    assert response.status_code == 400
    assert response.json['message'] == 'Error creating post'
    assert response.json['status'] is False
    assert response.json['type'] == 'custom_error'
    assert response.json['error_status']['error_code'] == '40000'

    # Ensure that create_new_post was called with the correct data
    mock_create_new_post.assert_called_once_with(post_data)


def test_get_post_success(test_client, mocker):
    # Mock the get_post function to return a successful response
    mock_get_post = mocker.patch('App.api.wrapper.apis.get_post', return_value=({
        'message': 'Post retrieved successfully',
        'status': True,
        'data': {
            'title': 'Test Post',
            'content': 'This is a test post.'
        }
    }, 200))

    # Create a JWT token for testing
    access_token = create_access_token(identity='testuser')

    # Define a sample post_id
    post_id = UUID('123e4567-e89b-12d3-a456-426614174000')

    # Simulate a GET request to the post endpoint
    response = test_client.get(f'/api/v1/post/{post_id}', headers={'Authorization': f'Bearer {access_token}'})

    # Assertions
    assert response.status_code == 200
    assert response.json['message'] == 'Post retrieved successfully'
    assert response.json['status'] is True
    assert response.json['data']['title'] == 'Test Post'
    assert response.json['data']['content'] == 'This is a test post.'

    # Ensure that get_post was called with the correct post_id
    mock_get_post.assert_called_once_with(post_id)

def test_get_post_failure(test_client, mocker):
    # Mock the get_post function to raise an exception
    mock_get_post = mocker.patch('App.api.wrapper.apis.get_post', side_effect=Exception('Failed to get post'))

    # Create a JWT token for testing
    access_token = create_access_token(identity='testuser')

    # Define a sample post_id
    post_id = UUID('123e4567-e89b-12d3-a456-426614174000')

    # Simulate a GET request to the post endpoint
    response = test_client.get(f'/api/v1/post/{post_id}', headers={'Authorization': f'Bearer {access_token}'})

    # Assertions
    assert response.status_code == 400
    assert response.json['message'] == 'Failed to get post'
    assert response.json['status'] is False
    assert response.json['type'] == 'custom_error'
    assert response.json['error_status']['error_code'] == '40005'

    # Ensure that get_post was called with the correct post_id
    mock_get_post.assert_called_once_with(post_id)

def test_update_post_success(test_client, mocker):
    # Mock the update_post function to return a successful response
    mock_update_post = mocker.patch('App.api.wrapper.apis.update_post', return_value=({
        'message': 'Post updated successfully',
        'status': True
    }, 200))

    # Create a JWT token for testing
    access_token = create_access_token(identity='testuser')

    # Define a sample post_id and post data
    post_id = UUID('123e4567-e89b-12d3-a456-426614174000')
    post_data = {
        'title': 'Updated Test Post',
        'content': 'This is an updated test post.',
        'image': None  # Include 'image' to match the function signature
    }

    # Simulate a PUT request to the post endpoint
    response = test_client.put(f'/api/v1/post/{post_id}', json=post_data, headers={'Authorization': f'Bearer {access_token}'})

    # Assertions
    assert response.status_code == 200
    assert response.json['message'] == 'Post updated successfully'
    assert response.json['status'] is True

    # Ensure that update_post was called with the correct data
    mock_update_post.assert_called_once_with(post_id, post_data)


def test_update_post_success(test_client, mocker):
    # Mock the update_post function to return a successful response
    mock_update_post = mocker.patch('App.api.wrapper.apis.update_post', return_value=({
        'message': 'Post updated successfully',
        'status': True
    }, 200))

    # Create a JWT token for testing
    access_token = create_access_token(identity='testuser')

    # Define a sample post_id and post data
    post_id = UUID('123e4567-e89b-12d3-a456-426614174000')
    post_data = {
        'title': 'Updated Test Post',
        'content': 'This is an updated test post.'
    }

    # Simulate a PUT request to the post endpoint
    response = test_client.put(f'/api/v1/post/{post_id}', json=post_data, headers={'Authorization': f'Bearer {access_token}'})

    # Assertions
    assert response.status_code == 200
    assert response.json['message'] == 'Post updated successfully'
    assert response.json['status'] is True

    # Ensure that update_post was called with the correct data
    mock_update_post.assert_called_once_with(post_id, {**post_data, 'image': None})


def test_delete_post_success(test_client, mocker):
    # Mock the delete_post function to return a successful response
    mock_delete_post = mocker.patch('App.api.wrapper.apis.delete_post', return_value=({
        'message': 'Post deleted successfully',
        'status': True
    }, 200))

    # Create a JWT token for testing
    access_token = create_access_token(identity='testuser')

    # Define a sample post_id
    post_id = UUID('123e4567-e89b-12d3-a456-426614174000')

    # Simulate a DELETE request to the post endpoint
    response = test_client.delete(f'/api/v1/post/{post_id}', headers={'Authorization': f'Bearer {access_token}'})

    # Assertions
    assert response.status_code == 200
    assert response.json['message'] == 'Post deleted successfully'
    assert response.json['status'] is True

    # Ensure that delete_post was called with the correct post_id and user_id
    mock_delete_post.assert_called_once_with(post_id, 'testuser')

def test_delete_post_failure(test_client, mocker):
    # Mock the delete_post function to raise an exception
    mock_delete_post = mocker.patch('App.api.wrapper.apis.delete_post', side_effect=Exception('Failed to delete post'))

    # Create a JWT token for testing
    access_token = create_access_token(identity='testuser')

    # Define a sample post_id
    post_id = UUID('123e4567-e89b-12d3-a456-426614174000')

    # Simulate a DELETE request to the post endpoint
    response = test_client.delete(f'/api/v1/post/{post_id}', headers={'Authorization': f'Bearer {access_token}'})

    # Assertions
    assert response.status_code == 400
    assert response.json['message'] == 'Failed to delete post'
    assert response.json['status'] is False
    assert response.json['type'] == 'custom_error'
    assert response.json['error_status']['error_code'] == '40005'

    # Ensure that delete_post was called with the correct post_id and user_id
    mock_delete_post.assert_called_once_with(post_id, 'testuser')

# Home 

def test_home_page_success(test_client, mocker):
    # Mock the get_home_page_data function to return a successful response
    mock_get_home_page_data = mocker.patch('App.api.wrapper.apis.get_home_page_data', return_value=({
        'message': 'Home page data retrieved successfully',
        'status': True,
        'data': []
    }, 200))

    # Create a JWT token for testing
    access_token = create_access_token(identity='testuser')

    # Simulate a GET request to the home page endpoint
    response = test_client.get('/api/v1/home?page=1&size=10', headers={'Authorization': f'Bearer {access_token}'})

    # Assertions
    assert response.status_code == 200
    assert response.json['message'] == 'Home page data retrieved successfully'
    assert response.json['status'] is True
    assert response.json['data'] == []

    # Ensure that get_home_page_data was called with the correct parameters
    mock_get_home_page_data.assert_called_once_with(1, 10, None)

def test_home_page_invalid_pagination(test_client, mocker):
    # Create a JWT token for testing
    access_token = create_access_token(identity='testuser')

    # Simulate a GET request with invalid page and size
    response = test_client.get('/api/v1/home?page=-1&size=0', headers={'Authorization': f'Bearer {access_token}'})

    # Assertions
    assert response.status_code == 400
    assert response.json['message'] == 'Invalid pagination parameters'
    assert response.json['status'] is False
    assert response.json['type'] == 'custom_error'
    assert response.json['error_status']['error_code'] == '40016'

def test_home_page_internal_server_error(test_client, mocker):
    # Mock the get_home_page_data function to raise a general exception
    mock_get_home_page_data = mocker.patch('App.api.wrapper.apis.get_home_page_data', side_effect=Exception('Failed to retrieve home page data'))

    # Create a JWT token for testing
    access_token = create_access_token(identity='testuser')

    # Simulate a GET request to the home page endpoint
    response = test_client.get('/api/v1/home?page=1&size=10', headers={'Authorization': f'Bearer {access_token}'})

    # Assertions
    assert response.status_code == 400
    assert response.json['message'] == 'Failed to retrieve home page data'
    assert response.json['status'] is False
    assert response.json['type'] == 'custom_error'
    assert response.json['error_status']['error_code'] == '40016'

    # Ensure that get_home_page_data was called with the correct parameters
    mock_get_home_page_data.assert_called_once_with(1, 10, None)