import json
import pytest
from unittest.mock import MagicMock
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
    delete_post
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
error_logger_mock = "App.api.logger.error_logger"

#Post
create_post_mock = "App.api.wrapper.utils.create_post_db"
save_image_mock = "App.api.wrapper.utils.save_image"
get_post_by_id_mock = "App.api.wrapper.utils.get_post_by_id"
update_post_mock = "App.api.wrapper.utils.update_post"
delete_post_mock = "App.api.wrapper.utils.delete_post"
get_jwt_identity_mock="App.api.wrapper.utils.get_jwt_identity"
get_comment_count_for_post_mock="App.api.wrapper.utils.get_comment_count_for_post"
post_to_dict_mock="App.api.wrapper.utils.post_to_dict"

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
        image_url="http://example.com/image.jpg",
        user_uid="user_id_123"
    )

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


#Post

# Create Post Tests

def test_create_new_post_success(mocker, post):
    mocker.patch(create_post_mock, return_value=post)
    mocker.patch(save_image_mock, return_value='http://example.com/image.jpg')
    mocker.patch(get_user_by_user_id_mock, return_value=MagicMock(username='test_user'))
    mocker.patch(get_jwt_identity_mock, return_value='user_id_123')

    data = {'title': 'Test Post', 'content': 'This is a test post.', 'image': None}
    response, status_code = create_new_post(data)

    assert status_code == 200
    assert response['message'] == 'Post created successfully'
    assert response['status'] is True
    assert response['data']['post_id'] == str(post.uid)
    assert response['data']['title'] == 'Test Post'
    assert response['data']['username'] == 'test_user'
    assert response['data']['content'] == 'This is a test post.'



def test_create_post_exception(mocker):
    mocker.patch(create_post_mock, side_effect=Exception("Database error"))

    data = {"title": "Test Post", "content": "This is a test post.", "image": None}
    response, status_code = create_new_post(data)

    assert status_code == 400
    assert response["message"] == "Error creating post"
    assert response["status"] is False
    assert response["error_status"]["error_code"] == "40000"

# Get Post Tests

def test_get_post_success(mocker, post):
    # Mock dependencies
    mocker.patch(get_post_by_id_mock, return_value=post)
    mocker.patch(get_comment_count_for_post_mock, return_value=5)  # Adjust the path as needed

    # Mock post_to_dict to return the post in the expected format
    mocker.patch(post_to_dict_mock, side_effect=lambda p: {
        'uid': str(p.uid),
        'title': p.title,
        'content': p.content,
        'user_uid': str(p.user_uid),
        'username': 'test_user',  # Assuming username is a fixed value for the test
        'created_at': '2024-08-20T00:00:00Z',
        'updated_at': '2024-08-21T00:00:00Z',
        'image': p.image_url,
        'no_of_comments': 5  # This should match the value returned by the mock
    })

    # Call the function being tested
    response, status_code = get_post(post.uid)

    # Assertions to validate the response structure and content
    assert status_code == 200
    assert response["message"] == "Post retrieved successfully"
    assert response["status"] is True
    assert response["type"] == 'success_message'
    assert response["error_status"]["error_code"] == '00000'
    assert response["data"]["title"] == post.title
    assert response["data"]["content"] == post.content

def test_get_post_not_found(mocker):
    mocker.patch(get_post_by_id_mock, return_value=None)
    response, status_code = get_post("invalid_id")

    assert status_code == 400
    assert response["message"] == "Post not found"
    assert response["status"] is False
    assert response["error_status"]["error_code"] == "40008"

# # Update Post Tests
from werkzeug.datastructures import FileStorage
from io import BytesIO
def test_update_post_success(mocker, post, test_client):
    # Mock the necessary functions
    mocker.patch(get_post_by_id_mock, return_value=post)
    mocker.patch(update_post_mock, return_value=True)
    mocker.patch(get_jwt_identity_mock, return_value='user_id_123')
    mocker.patch(save_image_mock,return_value='http://example.com/new_image.jpg')
    
    image_file = FileStorage(stream=BytesIO(b'Test image content'), filename='test_image.jpg', content_type='image/jpeg')
    form_data = {
        'title': 'Updated Post Title',
        'content': 'Updated Post Content',
        'image': image_file
    }

    # Simulate a multipart/form-data request with Authorization header
    response = test_client.put(
        f'/api/v1/post/{post.uid}',
        data=form_data,
        content_type='multipart/form-data',
        headers={'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c'}
    )

    # Assert the response
    assert response.status_code == 200
    response_json = json.loads(response.data)
    assert response_json['message'] == 'Post updated successfully.'
    assert response_json['status'] is True
    assert response_json['type'] == 'success_message'
    assert response_json['data']['post_id'] == str(post.uid)
    assert response_json['data']['title'] == 'Updated Post Title'
    assert response_json['data']['content'] == 'Updated Post Content'



def test_update_post_not_found(mocker):
    mocker.patch(get_post_by_id_mock, return_value=None)

    data = {'title': 'Updated Post', 'content': 'Updated content.', 'image': None}
    response, status_code = update_post('invalid_id', data)

    assert status_code == 400
    assert response['message'] == 'Post not found.'
    assert response['status'] is False
    assert response['error_status']['error_code'] == '40022'

def test_update_post_exception(mocker, post):
    mocker.patch(get_post_by_id_mock, return_value=post)
    mocker.patch(update_post_mock, side_effect=Exception("Database error"))

    data = {"title": "Updated Post", "content": "Updated content.", "image": None}
    response, status_code = update_post("d817221b-6f69-40f6-aaca-018b80dfebe0", data)

    assert status_code == 400
    assert response["message"] == "Failed to update post."
    assert response["status"] is False
    assert response["error_status"]["error_code"] == "40009"

# Delete Post Tests
    
def test_delete_post_success(mocker, post):
    mocker.patch(get_post_by_id_mock, return_value=post)
    mocker.patch(delete_post_mock, return_value=True)
    mocker.patch(get_jwt_identity_mock, return_value='user_id_123')
    # mocker.patch('os.remove')

    # Ensure post.uid returns a proper string, not a MagicMock object
    post.uid = '9a20366e-7b3c-4910-ac0c-6af3b6e82b6e'

    response, status_code = delete_post(post.uid, 'user_id_123')

    assert status_code == 200




def test_delete_post_not_found(mocker):
    mocker.patch(get_post_by_id_mock, return_value=None)

    response, status_code = delete_post("d817221b-6f69-40f6-aaca-018b80dfebe8", "8b0ea4f3-f057-4ed7-b72c-af904661ab06")

    assert status_code == 400
    assert response["message"] == "Post not found"
    assert response["status"] is False
    assert response["error_status"]["error_code"] == "40008"

