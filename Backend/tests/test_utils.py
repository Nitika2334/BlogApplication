import pytest
from unittest.mock import MagicMock, patch

from pytest_mock import mocker
from App.api.wrapper.utils import delete_comment
from App.api.wrapper.utils import update_comment
from App.api.wrapper.utils import get_comments
from App.api.wrapper.utils import create_comment
from App.api.wrapper.utils import user_login
from App.api.wrapper.utils import user_register
from App.api.wrapper.utils import user_logout,REVOKED_TOKENS
from App.api.wrapper.utils import (
    create_new_post,
    get_post,
    update_post,
    delete_post,
    get_home_page_data,
    post_to_dict,
    save_image
)

# Mocks

#Auth
get_user_by_username_mock = "App.api.wrapper.utils.get_user_by_username"
check_password_hash_mock = "App.api.wrapper.utils.check_password_hash"
create_access_token_mock = "App.api.wrapper.utils.create_access_token"
validate_email_mock = "App.api.wrapper.utils.validate_email"
validate_password_mock = "App.api.wrapper.utils.validate_password"
get_user_by_email_mock = "App.api.wrapper.utils.get_user_by_email"
add_user_mock = "App.api.wrapper.utils.add_user"
generate_password_hash_mock = "App.api.wrapper.utils.generate_password_hash"
get_user_by_user_id_mock = "App.api.wrapper.utils.get_user_by_user_id"

#Comments
get_comment_by_comment_id_mock = "App.api.wrapper.utils.get_comment_by_comment_id"
create_new_comment_mock = "App.api.wrapper.utils.create_new_comment"
get_comments_by_post_id_mock = "App.api.wrapper.utils.get_comments_by_post_id"
comment_to_dict_mock = "App.api.wrapper.utils.comment_to_dict"
delete_existing_comment_mock = "App.api.wrapper.utils.delete_existing_comment"
update_existing_comment_mock = "App.api.wrapper.utils.update_existing_comment"

#Post
save_image_mock = "App.api.wrapper.utils.save_image"
get_post_by_id_mock = "App.api.wrapper.utils.get_post_by_id"
get_jwt_identity_mock="App.api.wrapper.utils.get_jwt_identity"
get_comment_count_for_post_mock="App.api.wrapper.utils.get_comment_count_for_post"
post_to_dict_mock="App.api.wrapper.utils.post_to_dict"
delete_post_db_mock = "App.api.wrapper.utils.delete_post_db"
extract_public_id_from_url_mock = "App.api.wrapper.utils.extract_public_id_from_url"
cloudinary_uploader_destroy_mock = "cloudinary.uploader.destroy"
cache_delete_mock = "App.api.wrapper.utils.cache.delete"
error_logger_mock = "App.api.logger.error_logger"
get_cached_image_mock = "App.api.wrapper.utils.get_cached_image"
update_post_db_mock = "App.api.wrapper.utils.update_post_db"
create_post_db_mock = "App.api.wrapper.utils.create_post_db"
get_user_by_user_id_mock = "App.api.wrapper.utils.get_user_by_user_id"
cloudinary_uploader_upload_mock = "cloudinary.uploader.upload"



# Mock paths
get_paginated_posts_db_mock = "App.api.wrapper.utils.get_paginated_posts_db"
post_to_dict_mock = "App.api.wrapper.utils.post_to_dict"

@pytest.fixture
def users():
    # Create a mock user object
    return MagicMock(
        uid='user_uid_456',
        username='testuser',
        email='test@example.com',
        password='hashed_password'
    )

@pytest.fixture
def user_mock():
    # Create a mock user object
    return MagicMock(username='test_user')

@pytest.fixture
def user():
    return MagicMock(uid="user_uid_456", username="testuser")

@pytest.fixture
def new_post():
    return MagicMock(
        uid="9a20366e-7b3c-4910-ac0c-6af3b6e82b6e",
        title="Test Post",
        content="This is a test post.",
        image_url="http://example.com/image.jpg",
        user_uid="user_id_123"
    )

@pytest.fixture
def post():
    return MagicMock(
        uid="9a20366e-7b3c-4910-ac0c-6af3b6e82b6e",
        title="Test Post",
        content="This is a test post.",
        user_uid="user_id_123",
        username="test_user",
        image="http://example.com/image.jpg"
    )

@pytest.fixture
def mock_posts():
    # Create a list of mock post objects
    return [
        {"uid": "1", "title": "First Post", "content": "Content of the first post"},
        {"uid": "2", "title": "Second Post", "content": "Content of the second post"},
    ]

@pytest.fixture
def new_image_file():
    return MagicMock()

@pytest.fixture
def data():
    return {
        'title': 'Updated Title',
        'content': 'Updated content',
        'image': 'new_image_file'
    }


@pytest.fixture
def new_post_data():
    return {
        'title': 'New Post Title',
        'content': 'This is the content of the new post.',
        'image': 'image_file'
    }


@pytest.fixture
def new_comment():
    # Create a mock comment object
    return MagicMock(
        uid='853d4bc5-88fe-4408-bf3f-194e78d76058',
        content='This is a comment',
        created_at='2024-08-20T00:00:00Z'
    )

@pytest.fixture
def gets_comments():
    # Create mock comment objects
    return [
        MagicMock(comment_uid='1', content='First comment'),
        MagicMock(comment_uid='2', content='Second comment')
    ]

@pytest.fixture
def comment():
    # Create a mock comment object
    return MagicMock(
        comment_uid='853d4bc5-88fe-4408-bf3f-194e78d76058',
        user_uid='2ce3f6ff-0420-455f-853d-13bdd1df3124'
    )

# User register 

def test_user_register_success(mocker):
    # Mock dependencies
    mocker.patch(validate_email_mock, return_value=True)
    mocker.patch(validate_password_mock, return_value=True)
    mocker.patch(get_user_by_username_mock, return_value=None)
    mocker.patch(get_user_by_email_mock, return_value=None)
    mocker.patch(generate_password_hash_mock, return_value='hashed_password')
    mocker.patch(add_user_mock, return_value=MagicMock(uid='user_uid_456', username='testuser'))
    mocker.patch(create_access_token_mock, return_value='mock_access_token')
    mocker.patch(error_logger_mock)

    # Call the function
    data = {'username': 'testuser', 'email': 'test@example.com', 'password': 'Test@123'}
    response, status_code = user_register(data)

    # Assertions
    assert status_code == 200
    assert response['message'] == 'User registered successfully.'
    assert response['status'] is True
    assert response['type'] == 'success_message'
    assert response['error_status']['error_code'] == '00000'
    assert response['data']['user_id'] == 'user_uid_456'
    assert response['data']['access_token'] == 'mock_access_token'
    assert response['data']['username'] == 'testuser'

def test_user_register_missing_fields(mocker):
    # Mock dependencies
    mocker.patch(validate_email_mock)
    mocker.patch(validate_password_mock)
    mocker.patch(get_user_by_username_mock)
    mocker.patch(get_user_by_email_mock)
    mocker.patch(generate_password_hash_mock)
    mocker.patch(add_user_mock)
    mocker.patch(create_access_token_mock)
    mocker.patch(error_logger_mock)

    # Call the function
    data = {'username': 'testuser', 'email': '', 'password': 'password'}
    response, status_code = user_register(data)

    # Assertions
    assert status_code == 400
    assert response['message'] == 'Please provide username, email, and password.'
    assert response['status'] is False
    assert response['type'] == 'custom_error'
    assert response['error_status']['error_code'] == '40001'

def test_user_register_invalid_email(mocker):
    # Mock dependencies
    mocker.patch(validate_email_mock, return_value=False)
    mocker.patch(validate_password_mock)
    mocker.patch(get_user_by_username_mock)
    mocker.patch(get_user_by_email_mock)
    mocker.patch(generate_password_hash_mock)
    mocker.patch(add_user_mock)
    mocker.patch(create_access_token_mock)
    mocker.patch(error_logger_mock)

    # Call the function
    data = {'username': 'testuser', 'email': 'invalid_email', 'password': 'password'}
    response, status_code = user_register(data)

    # Assertions
    assert status_code == 400
    assert response['message'] == 'Email format is invalid.'
    assert response['status'] is False
    assert response['type'] == 'custom_error'
    assert response['error_status']['error_code'] == '40013'

def test_user_register_invalid_password(mocker):
    # Mock dependencies
    mocker.patch(validate_email_mock, return_value=True)
    mocker.patch(validate_password_mock, return_value=False)
    mocker.patch(get_user_by_username_mock)
    mocker.patch(get_user_by_email_mock)
    mocker.patch(generate_password_hash_mock)
    mocker.patch(add_user_mock)
    mocker.patch(create_access_token_mock)
    mocker.patch(error_logger_mock)

    # Call the function
    data = {'username': 'testuser', 'email': 'test@example.com', 'password': 'short'}
    response, status_code = user_register(data)

    # Assertions
    assert status_code == 400
    assert response['message'] == 'Password does not meet criteria.'
    assert response['status'] is False
    assert response['type'] == 'custom_error'
    assert response['error_status']['error_code'] == '40011'

def test_user_register_username_exists(mocker, users):
    # Mock dependencies
    mocker.patch(validate_email_mock, return_value=True)
    mocker.patch(validate_password_mock, return_value=True)
    mocker.patch(get_user_by_username_mock, return_value=users)
    mocker.patch(get_user_by_email_mock)
    mocker.patch(generate_password_hash_mock)
    mocker.patch(add_user_mock)
    mocker.patch(create_access_token_mock)
    mocker.patch(error_logger_mock)

    # Call the function
    data = {'username': 'testuser', 'email': 'test@example.com', 'password': 'password'}
    response, status_code = user_register(data)

    # Assertions
    assert status_code == 400
    assert response['message'] == 'Username already exists.'
    assert response['status'] is False
    assert response['type'] == 'custom_error'
    assert response['error_status']['error_code'] == '40002'

def test_user_register_email_exists(mocker, users):
    # Mock dependencies
    mocker.patch(validate_email_mock, return_value=True)
    mocker.patch(validate_password_mock, return_value=True)
    mocker.patch(get_user_by_username_mock, return_value=None)
    mocker.patch(get_user_by_email_mock, return_value=users)
    mocker.patch(generate_password_hash_mock)
    mocker.patch(add_user_mock)
    mocker.patch(create_access_token_mock)
    mocker.patch(error_logger_mock)

    # Call the function
    data = {'username': 'testuser', 'email': 'test@example.com', 'password': 'password'}
    response, status_code = user_register(data)

    # Assertions
    assert status_code == 400
    assert response['message'] == 'Email already exists.'
    assert response['status'] is False
    assert response['type'] == 'custom_error'
    assert response['error_status']['error_code'] == '40002'

def test_user_register_exception(mocker):
    # Mock dependencies
    mocker.patch(validate_email_mock, return_value=True)
    mocker.patch(validate_password_mock, return_value=True)
    mocker.patch(get_user_by_username_mock, return_value=None)
    mocker.patch(get_user_by_email_mock, return_value=None)
    mocker.patch(generate_password_hash_mock)
    mocker.patch(add_user_mock, side_effect=Exception('Database error'))
    mocker.patch(create_access_token_mock)
    mocker.patch(error_logger_mock)

    # Call the function
    data = {'username': 'testuser', 'email': 'test@example.com', 'password': 'password'}
    response, status_code = user_register(data)

    # Assertions
    assert status_code == 400
    assert response['message'] == 'Registration failed'
    assert response['status'] is False
    assert response['type'] == 'custom_error'
    assert response['error_status']['error_code'] == '40000'


# User Login

def test_user_login_success(mocker, users):
    # Mock dependencies
    mocker.patch(get_user_by_username_mock, return_value=users)
    mocker.patch(check_password_hash_mock, return_value=True)
    mocker.patch(create_access_token_mock, return_value='mocked_access_token')
    mocker.patch(error_logger_mock)

    # Call the function
    data = {'username': 'testuser', 'password': 'correct_password'}
    response, status_code = user_login(data)

    # Assertions
    assert status_code == 200
    assert response['message'] == 'User logged in successfully'
    assert response['status'] is True
    assert response['type'] == 'success_message'
    assert response['error_status']['error_code'] == '00000'
    assert response['data']['user_id'] == 'user_uid_456'
    assert response['data']['username'] == 'testuser'
    assert response['data']['access_token'] == 'mocked_access_token'

def test_user_login_invalid_credentials(mocker):
    # Mock dependencies
    mocker.patch(get_user_by_username_mock, return_value=None)
    mocker.patch(error_logger_mock)

    # Call the function
    data = {'username': 'testuser', 'password': 'wrong_password'}
    response, status_code = user_login(data)

    # Assertions
    assert status_code == 400
    assert response['message'] == 'Invalid credentials'
    assert response['status'] is False
    assert response['type'] == 'custom_error'
    assert response['error_status']['error_code'] == '40004'

def test_user_login_exception(mocker):
    # Mock dependencies
    mocker.patch(get_user_by_username_mock, side_effect=Exception('Database error'))
    mocker.patch(error_logger_mock)

    # Call the function
    data = {'username': 'testuser', 'password': 'correct_password'}
    response, status_code = user_login(data)

    # Assertions
    assert status_code == 400
    assert response['message'] == 'Login failed'
    assert response['status'] is False
    assert response['type'] == 'custom_error'
    assert response['error_status']['error_code'] == '40000'


# User Logout

def test_user_logout_success(mocker):
    mock_jwt = {'jti': 'test_jti', 'exp': 1234567890}
    mocker.patch('App.api.wrapper.utils.get_jwt', return_value=mock_jwt)

    # Calling the user_logout function
    response, status_code = user_logout()

    # Assertions
    assert status_code == 200
    assert response['status'] is True
    assert response['message'] == 'User logged out successfully'
    assert mock_jwt['jti'] in REVOKED_TOKENS
    assert REVOKED_TOKENS[mock_jwt['jti']] == mock_jwt['exp']

def test_user_logout_exception(mocker):
    mocker.patch('App.api.wrapper.utils.get_jwt', side_effect=Exception("JWT error"))

    # Calling the user_logout function
    response, status_code = user_logout()

    # Assertions
    assert status_code == 400
    assert response['status'] is False
    assert response['message'] == 'Logout failed'



# Create Comments

def test_create_comment_success(mocker, user, new_comment):
    # Mock dependencies
    mocker.patch(get_user_by_user_id_mock, return_value=user)
    mocker.patch(create_new_comment_mock, return_value=new_comment)
    mocker.patch(error_logger_mock)

    # Call the function
    data = {'content': 'This is a comment'}
    response, status_code = create_comment(data, 'post_uid_123', 'user_uid_456')

    # Assertions
    assert status_code == 200
    assert response['message'] == 'Comment created successfully'
    assert response['status'] is True
    assert response['type'] == 'success_message'
    assert response['error_status']['error_code'] == '00000'
    assert response['data']['comment_id'] == '853d4bc5-88fe-4408-bf3f-194e78d76058'
    assert response['data']['post_id'] == 'post_uid_123'
    assert response['data']['username'] == 'testuser'
    assert response['data']['user_id'] == 'user_uid_456'
    assert response['data']['content'] == 'This is a comment'
    assert response['data']['created_at'] == '2024-08-20T00:00:00Z'

def test_create_comment_user_not_found(mocker, new_comment):
    # Mock dependencies
    mocker.patch(get_user_by_user_id_mock, return_value=None)
    mocker.patch(create_new_comment_mock, return_value=new_comment)
    mocker.patch(error_logger_mock)

    # Call the function
    data = {'content': 'This is a comment'}
    response, status_code = create_comment(data, 'post_uid_123', 'user_uid_456')

    # Assertions
    assert status_code == 400
    assert response['message'] == 'Failed to create comment'
    assert response['status'] is False
    assert response['type'] == 'custom_error'
    assert response['error_status']['error_code'] == '40013'

def test_create_comment_exception(mocker, user):
    # Mock dependencies
    mocker.patch(get_user_by_user_id_mock, return_value=user)
    mocker.patch(create_new_comment_mock, side_effect=Exception('Database error'))
    mocker.patch(error_logger_mock)

    # Call the function
    data = {'content': 'This is a comment'}
    response, status_code = create_comment(data, 'post_uid_123', 'user_uid_456')

    # Assertions
    assert status_code == 400
    assert response['message'] == 'Failed to create comment'
    assert response['status'] is False
    assert response['type'] == 'custom_error'
    assert response['error_status']['error_code'] == '40013'

# Get Comments
def test_get_comments_success(mocker, gets_comments):
    # Mock dependencies
    mocker.patch(get_comments_by_post_id_mock, return_value=gets_comments)
    mocker.patch(comment_to_dict_mock, side_effect=lambda gets_comments: {
        'uid': gets_comments.comment_uid,
        'content': gets_comments.content
    })
    mocker.patch(error_logger_mock)

    # Call the function
    response, status_code = get_comments('post_uid_123')

    # Assertions
    assert status_code == 200
    assert response['message'] == 'Comments retrieved successfully'
    assert response['status'] is True
    assert response['type'] == 'success_message'
    assert response['error_status']['error_code'] == '00000'
    assert len(response['data']['comments']) == 2
    assert response['data']['comments'][0]['uid'] == '1'
    assert response['data']['comments'][1]['uid'] == '2'

def test_get_comments_failure(mocker):
    # Mock dependencies
    mocker.patch(get_comments_by_post_id_mock, side_effect=Exception('Database error'))
    mocker.patch(error_logger_mock)

    # Call the function
    response, status_code = get_comments('post_uid_123')

    # Assertions
    assert status_code == 400
    assert response['message'] == 'Failed to get comments'
    assert response['status'] is False
    assert response['type'] == 'custom_error'
    assert response['error_status']['error_code'] == '40014'

def test_get_comments_empty(mocker):
    # Mock dependencies
    mocker.patch(get_comments_by_post_id_mock, return_value=[])
    mocker.patch(comment_to_dict_mock, side_effect=lambda gets_comments: {
        'uid': gets_comments.comment_uid,
        'content': gets_comments.content
    })
    mocker.patch(error_logger_mock)

    # Call the function
    response, status_code = get_comments('post_uid_123')

    # Assertions
    assert status_code == 200
    assert response['message'] == 'Comments retrieved successfully'
    assert response['status'] is True
    assert response['type'] == 'success_message'
    assert response['error_status']['error_code'] == '00000'
    assert response['data']['comments'] == []

def test_get_comments_exception(mocker):
    # Mock dependencies
    mocker.patch(get_comments_by_post_id_mock, side_effect=Exception('Database error'))
    mocker.patch(error_logger_mock)

    # Call the function
    response, status_code = get_comments('post_uid_123')

    # Assertions
    assert status_code == 400
    assert response['message'] == 'Failed to get comments'
    assert response['status'] is False
    assert response['type'] == 'custom_error'
    assert response['error_status']['error_code'] == '40014'

# Update Comment

def test_update_comment_success(mocker, comment):
    # Mock dependencies
    mocker.patch(get_comment_by_comment_id_mock, return_value=comment)
    mocker.patch(update_existing_comment_mock, return_value=True)
    mocker.patch(error_logger_mock)

    # Prepare test data
    data = {'content': 'Updated content'}

    # Call the function
    response, status_code = update_comment(data, '853d4bc5-88fe-4408-bf3f-194e78d76058', '2ce3f6ff-0420-455f-853d-13bdd1df3124')

    # Assertions
    assert status_code == 200
    assert response['message'] == 'Comment updated successfully.'
    assert response['status'] is True
    assert response['type'] == 'success_message'
    assert response['error_status']['error_code'] == '00000'

def test_update_comment_not_found(mocker):
    # Mock dependencies
    mocker.patch(get_comment_by_comment_id_mock, return_value=None)
    mocker.patch(error_logger_mock)

    # Prepare test data
    data = {'content': 'Updated content'}

    # Call the function
    response, status_code = update_comment(data, '853d4bc5-88fe-4408-bf3f-194e78d76058', '2ce3f6ff-0420-455f-853d-13bdd1df3124')

    # Assertions
    assert status_code == 400
    assert response['message'] == 'Comment not found.'
    assert response['status'] is False
    assert response['type'] == 'custom_error'
    assert response['error_status']['error_code'] == '40014'

def test_update_comment_unauthorized(mocker, comment):
    # Mock dependencies
    mocker.patch(get_comment_by_comment_id_mock, return_value=comment)
    mocker.patch(update_existing_comment_mock, return_value=False)
    mocker.patch(error_logger_mock)

    # Prepare test data
    data = {'content': 'Updated content'}

    # Call the function
    response, status_code = update_comment(data, '853d4bc5-88fe-4408-bf3f-194e78d76058', 'wrong_user_id')

    # Assertions
    assert status_code == 400
    assert response['message'] == 'You are not authorized to update this comment.'
    assert response['status'] is False
    assert response['type'] == 'custom_error'
    assert response['error_status']['error_code'] == '40017'

def test_update_comment_failure(mocker, comment):
    # Mock dependencies
    mocker.patch(get_comment_by_comment_id_mock, return_value=comment)
    mocker.patch(update_existing_comment_mock, return_value=False)
    mocker.patch(error_logger_mock)

    # Prepare test data
    data = {'content': 'Updated content'}

    # Call the function
    response, status_code = update_comment(data, '853d4bc5-88fe-4408-bf3f-194e78d76058', '2ce3f6ff-0420-455f-853d-13bdd1df3124')

    # Assertions
    assert status_code == 400
    assert response['message'] == 'Comment not Updated'
    assert response['status'] is False
    assert response['type'] == 'custom_error'
    assert response['error_status']['error_code'] == '40013'

def test_update_comment_exception(mocker, comment):
    # Mock dependencies
    mocker.patch(get_comment_by_comment_id_mock, return_value=comment)
    mocker.patch(update_existing_comment_mock, side_effect=Exception('Database error'))
    mocker.patch(error_logger_mock)

    # Prepare test data
    data = {'content': 'Updated content'}

    # Call the function
    response, status_code = update_comment(data, '853d4bc5-88fe-4408-bf3f-194e78d76058', '2ce3f6ff-0420-455f-853d-13bdd1df3124')

    # Assertions
    assert status_code == 400
    assert response['message'] == 'Failed to update comment'
    assert response['status'] is False
    assert response['type'] == 'custom_error'
    assert response['error_status']['error_code'] == '40016'



# Delete Comment

def test_delete_comment_success(mocker, comment):
    # Mock dependencies
    mocker.patch(get_comment_by_comment_id_mock, return_value=comment)
    mocker.patch(delete_existing_comment_mock, return_value=True)
    mocker.patch(error_logger_mock)

    # Call the function
    response, status_code = delete_comment('853d4bc5-88fe-4408-bf3f-194e78d76058', '2ce3f6ff-0420-455f-853d-13bdd1df3124')

    # Assertions
    assert status_code == 200
    assert response['message'] == 'Comment deleted successfully.'
    assert response['status'] is True
    assert response['type'] == 'success_message'
    assert response['error_status']['error_code'] == '00000'

def test_delete_comment_not_found(mocker):
    # Mock dependencies
    mocker.patch(get_comment_by_comment_id_mock, return_value=None)
    mocker.patch(error_logger_mock)

    # Call the function
    response, status_code = delete_comment('853d4bc5-88fe-4408-bf3f-194e78d76058', '2ce3f6ff-0420-455f-853d-13bdd1df3124')

    # Assertions
    assert status_code == 400
    assert response['message'] == 'Comment not found.'
    assert response['status'] is False
    assert response['type'] == 'custom_error'
    assert response['error_status']['error_code'] == '40014'

def test_delete_comment_unauthorized(mocker, comment):
    # Mock dependencies
    mocker.patch(get_comment_by_comment_id_mock, return_value=comment)
    mocker.patch(delete_existing_comment_mock, return_value=False)
    mocker.patch(error_logger_mock)

    # Call the function
    response, status_code = delete_comment('853d4bc5-88fe-4408-bf3f-194e78d76058', 'wrong_user_id')

    # Assertions
    assert status_code == 400
    assert response['message'] == 'You are not authorized to delete this comment.'
    assert response['status'] is False
    assert response['type'] == 'custom_error'
    assert response['error_status']['error_code'] == '40017'

def test_delete_comment_failure(mocker, comment):
    # Mock dependencies
    mocker.patch(get_comment_by_comment_id_mock, return_value=comment)
    mocker.patch(delete_existing_comment_mock, return_value=False)
    mocker.patch(error_logger_mock)

    # Call the function
    response, status_code = delete_comment('853d4bc5-88fe-4408-bf3f-194e78d76058', '2ce3f6ff-0420-455f-853d-13bdd1df3124')

    # Assertions
    assert status_code == 400
    assert response['message'] == 'Comment not Deleted'
    assert response['status'] is False
    assert response['type'] == 'custom_error'
    assert response['error_status']['error_code'] == '40013'

def test_delete_comment_exception(mocker, comment):
    # Mock dependencies
    mocker.patch(get_comment_by_comment_id_mock, return_value=comment)
    mocker.patch(delete_existing_comment_mock, side_effect=Exception('Database error'))
    mocker.patch(error_logger_mock)

    # Call the function
    response, status_code = delete_comment('853d4bc5-88fe-4408-bf3f-194e78d76058', '2ce3f6ff-0420-455f-853d-13bdd1df3124')

    # Assertions
    assert status_code == 400
    assert response['message'] == 'Failed to delete comment'
    assert response['status'] is False
    assert response['type'] == 'custom_error'
    assert response['error_status']['error_code'] == '40018'


def test_get_home_page_data_success(mock_posts):
    with patch(post_to_dict_mock) as mock_post_to_dict, patch(get_paginated_posts_db_mock) as mock_get_paginated_posts_db:
        # Mock the return values of the database function and utility function
        mock_get_paginated_posts_db.return_value = (mock_posts, 10)
        mock_post_to_dict.side_effect = lambda post: post

        # Call the function
        response, status_code = get_home_page_data(page=1, size=5, user_id='user123')

        # Assertions
        assert status_code == 200
        assert response['status'] is True
        assert response['data']['current_page'] == 1
        assert response['data']['page_size'] == 5
        assert response['data']['total_pages'] == 2
        assert response['data']['total_posts'] == 10
        assert response['data']['posts'] == mock_posts

def test_get_home_page_data_failure():
    with patch(get_paginated_posts_db_mock) as mock_get_paginated_posts_db:
        # Set the mock to raise an exception
        mock_get_paginated_posts_db.side_effect = Exception('DB error')

        # Call the function
        response, status_code = get_home_page_data(page=1, size=5, user_id='user123')

        # Assertions
        assert status_code == 400
        assert response['status'] is False
        assert response['message'] == 'Failed to retrieve home page data'
        assert response['error_status']['error_code'] == '40016'

def test_delete_post_success(mocker, post):
    # Mock the dependencies
    mocker.patch(get_post_by_id_mock, return_value=post)
    mocker.patch(delete_post_db_mock, return_value=True)
    mocker.patch(extract_public_id_from_url_mock, return_value="public_id")
    mocker.patch(cloudinary_uploader_destroy_mock)
    mocker.patch(cache_delete_mock)

    # Call the function
    response, status_code = delete_post(post_id=post.uid, user_id=post.user_uid)

    # Assertions
    assert status_code == 200
    assert response['status'] is True
    assert response['message'] == 'Post deleted successfully.'

def test_delete_post_not_found(mocker):
    # Mock the dependencies
    mocker.patch(get_post_by_id_mock, return_value=None)

    # Call the function
    response, status_code = delete_post(post_id="non_existing_id", user_id="user_id_123")

    # Assertions
    assert status_code == 400
    assert response['status'] is False
    assert response['message'] == 'Post not found'
    assert response['error_status']['error_code'] == '40008'

def test_delete_post_unauthorized(mocker, post):
    # Mock the dependencies
    mocker.patch(get_post_by_id_mock, return_value=post)

    # Call the function with a different user ID
    response, status_code = delete_post(post_id=post.uid, user_id="different_user_id")

    # Assertions
    assert status_code == 400
    assert response['status'] is False
    assert response['message'] == 'You are not authorized to delete this post.'
    assert response['error_status']['error_code'] == '40006'

def test_delete_post_failed_deletion(mocker, post):
    # Mock the dependencies
    mocker.patch(get_post_by_id_mock, return_value=post)
    mocker.patch(delete_post_db_mock, return_value=False)

    # Call the function
    response, status_code = delete_post(post_id=post.uid, user_id=post.user_uid)

    # Assertions
    assert status_code == 400
    assert response['status'] is False
    assert response['message'] == 'Failed to delete post.'
    assert response['error_status']['error_code'] == '40010'

def test_delete_post_exception(mocker, post):
    # Mock the dependencies
    mocker.patch(get_post_by_id_mock, return_value=post)
    mocker.patch(delete_post_db_mock, side_effect=Exception('DB error'))
    mocker.patch(error_logger_mock)

    # Call the function
    response, status_code = delete_post(post_id=post.uid, user_id=post.user_uid)

    # Assertions
    assert status_code == 400
    assert response['status'] is False
    assert response['message'] == 'Failed to delete post'
    assert response['error_status']['error_code'] == '40011'

def test_post_to_dict(post, mocker):
    # Mock the external functions
    mocker.patch(get_cached_image_mock, return_value="http://example.com/cached_image.jpg")
    mocker.patch(get_comment_count_for_post_mock, return_value=5)
    
    # Call the function
    result = post_to_dict(post)
    
    # Expected result
    expected_result = {
        'uid': str(post.uid),
        'title': post.title,
        'content': post.content,
        'user_uid': str(post.user_uid),
        'username': post.username,
        'created_at': post.created_at.isoformat(),
        'updated_at': post.updated_at.isoformat(),
        'image': "http://example.com/cached_image.jpg",
        'no_of_comments': 5
    }
    
    # Assertions
    assert result == expected_result

def test_update_post_success(mocker, post, data, new_image_file):
    mocker.patch(get_post_by_id_mock, return_value=post)
    mocker.patch(save_image_mock, return_value="http://example.com/new_image.jpg")
    mocker.patch(extract_public_id_from_url_mock, return_value="public_id")
    mocker.patch(cloudinary_uploader_destroy_mock)
    mocker.patch(get_cached_image_mock)
    mocker.patch(update_post_db_mock, return_value=True)

    response, status_code = update_post(post_id=post.uid, data=data, user_id=post.user_uid)

    assert status_code == 200
    assert response['status'] is True
    assert response['message'] == 'Post updated successfully.'

def test_update_post_not_found(mocker, data):
    mocker.patch(get_post_by_id_mock, return_value=None)

    response, status_code = update_post(post_id="non_existing_id", data=data, user_id="user_id_123")

    assert status_code == 400
    assert response['status'] is False
    assert response['message'] == 'Post not found.'
    assert response['error_status']['error_code'] == '40022'

def test_update_post_unauthorized(mocker, post, data):
    mocker.patch(get_post_by_id_mock, return_value=post)

    response, status_code = update_post(post_id=post.uid, data=data, user_id="different_user_id")

    assert status_code == 400
    assert response['status'] is False
    assert response['message'] == 'You are not authorized to update this post.'
    assert response['error_status']['error_code'] == '40006'

def test_update_post_image_upload_error(mocker, post, data):
    mocker.patch(get_post_by_id_mock, return_value=post)
    mocker.patch(save_image_mock, side_effect=Exception('Image upload error'))
    mocker.patch(update_post_db_mock, return_value=True)

    response, status_code = update_post(post_id=post.uid, data=data, user_id=post.user_uid)

    assert status_code == 400
    assert response['status'] is False
    assert response['message'] == 'Failed to update post'
    assert response['error_status']['error_code'] == '40009'

def test_update_post_update_db_error(mocker, post, data):
    mocker.patch(get_post_by_id_mock, return_value=post)
    mocker.patch(save_image_mock, return_value="http://example.com/new_image.jpg")
    mocker.patch(update_post_db_mock, return_value=False)

    response, status_code = update_post(post_id=post.uid, data=data, user_id=post.user_uid)

    assert status_code == 400
    assert response['status'] is False
    assert response['message'] == 'Failed to update post.'
    assert response['error_status']['error_code'] == '40009'

def test_update_post_exception(mocker, post, data):
    mocker.patch(get_post_by_id_mock, return_value=post)
    mocker.patch(save_image_mock, return_value="http://example.com/new_image.jpg")
    mocker.patch(update_post_db_mock, side_effect=Exception('DB error'))
    mocker.patch(error_logger_mock)

    response, status_code = update_post(post_id=post.uid, data=data, user_id=post.user_uid)

    assert status_code == 400
    assert response['status'] is False
    assert response['message'] == 'Failed to update post'
    assert response['error_status']['error_code'] == '40009'

def test_create_new_post_success(mocker, new_post_data):
    mocker.patch(get_user_by_user_id_mock, return_value=MagicMock(username='test_user'))
    mocker.patch(get_jwt_identity_mock, return_value='user_id_123')
    mocker.patch(create_post_db_mock, return_value=MagicMock(uid='post_id', title='New Post Title', content='This is the content of the new post.', image='http://example.com/image.jpg'))
    mocker.patch(save_image_mock, return_value='http://example.com/image.jpg')
    mocker.patch(get_cached_image_mock)
    
    response, status_code = create_new_post(new_post_data)

    assert status_code == 200
    assert response['status'] is True
    assert response['message'] == 'Post created successfully'
    assert response['data']['post_id'] == 'post_id'
    assert response['data']['title'] == 'New Post Title'

def test_create_new_post_missing_title_or_content(mocker, new_post_data):
    data_missing_title = new_post_data.copy()
    data_missing_title.pop('title')

    response, status_code = create_new_post(data_missing_title)

    assert status_code == 400
    assert response['status'] is False
    assert response['message'] == 'Title and content are required'
    assert response['error_status']['error_code'] == '40012'

def test_create_new_post_exception(mocker, new_post_data):
    mocker.patch(get_user_by_user_id_mock, return_value=MagicMock(username='test_user'))
    mocker.patch(get_jwt_identity_mock, return_value='user_id_123')
    mocker.patch(create_post_db_mock, side_effect=Exception('DB error'))
    mocker.patch(save_image_mock, return_value='http://example.com/image.jpg')
    mocker.patch(error_logger_mock)

    response, status_code = create_new_post(new_post_data)

    assert status_code == 400
    assert response['status'] is False
    assert response['message'] == 'Error creating post'
    assert response['error_status']['error_code'] == '40000'

def test_save_image_success(mocker):
    mocker.patch(cloudinary_uploader_upload_mock, return_value={'secure_url': 'http://example.com/image.jpg'})
    mocker.patch(extract_public_id_from_url_mock, return_value='public_id')
    mocker.patch(cloudinary_uploader_destroy_mock)

    image_url = save_image('image_file')

    assert image_url == 'http://example.com/image.jpg'

def test_save_image_exception(mocker):
    mocker.patch(cloudinary_uploader_upload_mock, side_effect=Exception('Upload error'))
    mocker.patch(error_logger_mock)

    image_url = save_image('image_file')

    assert image_url is None

def test_get_post_success(mocker, post):
    mocker.patch(get_post_by_id_mock, return_value=post)
    mocker.patch(post_to_dict_mock, return_value={
        'uid': post.uid,
        'title': post.title,
        'content': post.content,
        'user_uid': post.user_uid,
        'username': post.username,
        'image': post.image,
        'created_at': '2024-08-25T00:00:00Z'
    })
    
    response, status_code = get_post(post_id=post.uid)

    assert status_code == 200
    assert response['status'] is True
    assert response['message'] == 'Post retrieved successfully'
    assert response['data']['uid'] == post.uid

def test_get_post_not_found(mocker):
    mocker.patch(get_post_by_id_mock, return_value=None)

    response, status_code = get_post(post_id='non_existing_id')

    assert status_code == 400
    assert response['status'] is False
    assert response['message'] == 'Post not found'
    assert response['error_status']['error_code'] == '40008'

def test_get_post_exception(mocker):
    mocker.patch(get_post_by_id_mock, side_effect=Exception('DB error'))
    mocker.patch(error_logger_mock)

    response, status_code = get_post(post_id='any_id')

    assert status_code == 400
    assert response['status'] is False
    assert response['message'] == 'Error retrieving post'
    assert response['error_status']['error_code'] == '40021'