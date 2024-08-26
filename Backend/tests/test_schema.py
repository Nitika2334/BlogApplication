import pytest
from unittest.mock import patch, MagicMock
from App.api.wrapper.schema import (
    get_user_by_username, get_user_by_email, get_user_by_user_id, add_user,
    create_post_db, update_post_db, get_post_by_id, save_image_db,
    delete_post_db, get_comment_count_for_post, get_comment_by_comment_id,
    get_comments_by_post_id, create_new_comment, update_existing_comment,
    delete_existing_comment
)
from App.Models.User.UserModel import User
from App.Models.Post.PostModel import Post
from App.Models.Comment.CommentModel import Comment

class MockCursor:
    def execute(self, *args, **kwargs):
        pass

    def fetchone(self):
        pass

    def close(self):
        pass

class MockConnection:
    def close(self):
        return "closed"

    def commit(self):
        pass

    def rollback(self):
        pass

def mock_create_connection():
    return MockCursor(), MockConnection()


# Test get_user_by_username function
def test_get_user_by_username_success(mocker, test_client):
    mock_user = MagicMock(spec=User)
    query_mock = MagicMock()
    query_mock.filter_by.return_value.first.return_value = mock_user
    
    mocker.patch('App.Models.User.UserModel.User.query', query_mock)

    username = "test_user"
    result = get_user_by_username(username)
    
    assert result == mock_user


def test_get_user_by_username_with_error(mocker):
    # Create a mock query object that raises an exception when filter_by is called
    query_mock = MagicMock()
    query_mock.filter_by.side_effect = Exception("Database error")
    mocker.patch('App.Models.User.UserModel.User.query', query_mock)

    username = "test_user"

    with pytest.raises(Exception) as excinfo:
        get_user_by_username(username)
    
    assert str(excinfo.value) == "Database error"


# Test get_user_by_email function

def test_get_user_by_email_success(mocker, test_client):
    mock_user = MagicMock(spec=User)
    query_mock = MagicMock()
    query_mock.filter_by.return_value.first.return_value = mock_user
    
    mocker.patch('App.Models.User.UserModel.User.query', query_mock)

    email = "test@example.com"
    result = get_user_by_email(email)
    
    assert result == mock_user


def test_get_user_by_email_with_error(mocker):
    # Create a mock query object that raises an exception when filter_by is called
    query_mock = MagicMock()
    query_mock.filter_by.side_effect = Exception("Database error")
    mocker.patch('App.Models.User.UserModel.User.query', query_mock)

    email = "test@example.com"

    with pytest.raises(Exception) as excinfo:
        get_user_by_email(email)
    
    assert str(excinfo.value) == "Database error"



# Test get_user_by_user_id function

def test_get_user_by_user_id_success(mocker, test_client):
    mock_user = MagicMock(spec=User)
    query_mock = MagicMock()
    query_mock.filter_by.return_value.first.return_value = mock_user
    
    mocker.patch('App.Models.User.UserModel.User.query', query_mock)

    user_id = 1
    result = get_user_by_user_id(user_id)
    
    assert result == mock_user    

def test_get_user_by_user_id_with_error(mocker):
    mocker.patch('App.config.Config.SQLALCHEMY_DATABASE_URI', return_value=mock_create_connection())
    
    uid = "test_uid"
    with pytest.raises(Exception) as excinfo:
        get_user_by_user_id(uid)
    assert str(excinfo.value) == "Database error"


# Test add_user function
    
def test_add_user_success(mocker, test_client):
    mock_user = MagicMock(spec=User)
    mocker.patch('App.api.wrapper.schema.User', return_value=mock_user)
    mocker.patch('App.api.wrapper.schema.db.session.add', lambda x: None)
    mocker.patch('App.api.wrapper.schema.db.session.commit', lambda: None)

    username = "new_user"
    email = "new@example.com"
    password = "password"
    
    result = add_user(username, email, password)
    
    assert result == mock_user

def test_add_user_with_error(mocker,test_client):
    mocker.patch('App.config.Config.SQLALCHEMY_DATABASE_URI', return_value=mock_create_connection())
    
    username = "test_user"
    email = "test@example.com"
    password = "password123"
    
    with pytest.raises(Exception) as excinfo:
        add_user(username, email, password)
    assert str(excinfo.value) == "Database error"


# Test create_post_db function
    
def test_create_post_db_success(mocker, test_client):
    mock_post = MagicMock(spec=Post)
    mocker.patch('App.api.wrapper.schema.Post', return_value=mock_post)
    mocker.patch('App.api.wrapper.schema.db.session.add', lambda x: None)
    mocker.patch('App.api.wrapper.schema.db.session.commit', lambda: None)

    title = "New Post"
    content = "This is a new post."
    user_uid = 1
    username = "user"
    
    result = create_post_db(title, content, user_uid, username)
    
    assert result == mock_post

def test_create_post_db_with_error(mocker,test_client):
    mocker.patch('App.config.Config.SQLALCHEMY_DATABASE_URI', return_value=mock_create_connection())
    
    title = "Test Title"
    content = "Test Content"
    user_uid = "user_uid"
    username = "test_user"
    
    with pytest.raises(Exception) as excinfo:
        create_post_db(title, content, user_uid, username)
    assert str(excinfo.value) == "Database error"


# Test update_post_db function
    
def test_update_post_db_with_error(mocker):
    mocker.patch('App.api.wrapper.schema.Post.query.filter_by', side_effect=Exception("Database error"))
    mocker.patch('App.api.wrapper.schema.db.session.commit', side_effect=Exception("Database error"))

    post_id = 1
    title = "Updated Title"
    content = "Updated Content"

    with pytest.raises(Exception) as excinfo:
        update_post_db(post_id, title, content)
    
    assert str(excinfo.value) == "Database error"


def test_update_post_db_with_error(mocker,test_client):
    mocker.patch('App.config.Config.SQLALCHEMY_DATABASE_URI', return_value=mock_create_connection())
    
    post_id = "post_id"
    title = "Updated Title"
    content = "Updated Content"
    
    with pytest.raises(Exception) as excinfo:
        update_post_db(post_id, title, content)
    assert str(excinfo.value) == "Database error"


# Test get_post_by_id function
    
def test_get_post_by_id_success(mocker):
    mock_post = MagicMock(spec=Post)
    mocker.patch('App.api.wrapper.schema.Post.query.filter_by', side_effect=Exception("Database error"))

    post_id = 1
    with pytest.raises(Exception) as excinfo:
        get_post_by_id(post_id)
    
    assert str(excinfo.value) == "Database error"   

def test_get_post_by_id_with_error(mocker,test_client):
    mocker.patch('App.config.Config.SQLALCHEMY_DATABASE_URI', return_value=mock_create_connection())
    
    post_id = "post_id"
    
    with pytest.raises(Exception) as excinfo:
        get_post_by_id(post_id)
    assert str(excinfo.value) == "Database error"

# Test delete_post_db function
    
def test_delete_post_db_success(mocker, test_client):
    mock_post = MagicMock(spec=Post)
    mocker.patch('App.api.wrapper.schema.Post.query.filter_by', side_effect=Exception("Database error"))
    mocker.patch('App.api.wrapper.schema.db.session.delete', lambda x: None)
    mocker.patch('App.api.wrapper.schema.db.session.commit', side_effect=Exception("Database error"))

    post_id = 1
    user_uid = 1

    with pytest.raises(Exception) as excinfo:
        delete_post_db(post_id, user_uid)
    
        assert str(excinfo.value) == "Database error"

    

def test_delete_post_db_with_error(mocker,test_client):
    mocker.patch('App.config.Config.SQLALCHEMY_DATABASE_URI', return_value=mock_create_connection())
    
    post_id = "post_id"
    user_uid = "user_uid"
    
    with pytest.raises(Exception) as excinfo:
        delete_post_db(post_id, user_uid)

    assert str(excinfo.value) == "Database error"


# Test get_comment_count_for_post function

def test_get_comment_count_for_post_success(mocker, test_client):
    mock_count = 5
    mocker.patch('App.api.wrapper.schema.Post.query.filter_by', side_effect=Exception("Database error"))

    post_id = 1

    with pytest.raises(Exception) as excinfo:
        get_comment_count_for_post(post_id)
    
    assert str(excinfo.value) == "Database error"


def test_get_comment_count_for_post_with_error(mocker,test_client):
    mocker.patch('App.config.Config.SQLALCHEMY_DATABASE_URI', return_value=mock_create_connection())
    
    post_id = "post_id"
    
    with pytest.raises(Exception) as excinfo:
        get_comment_count_for_post(post_id)
    assert str(excinfo.value) == "Database error"


# Test get_comment_by_comment_id function
    
def test_get_comment_by_comment_id_success(mocker):
    mock_comment = MagicMock()

    mock_query = MagicMock()
    mock_query.filter_by.return_value.first.return_value = mock_comment

    mocker.patch('App.Models.Comment.CommentModel.Comment.query', mock_query)

    comment_id = 1
    result = get_comment_by_comment_id(comment_id)
    
    assert result == mock_comment
def test_get_comment_by_comment_id_with_error(mocker,test_client):
    mocker.patch('App.config.Config.SQLALCHEMY_DATABASE_URI', return_value=mock_create_connection())
    
    comment_id = "comment_id"
    
    with pytest.raises(Exception) as excinfo:
        get_comment_by_comment_id(comment_id)
    assert str(excinfo.value) == "Database error"


# Test get_comments_by_post_id function
    
def test_get_comments_by_post_id_success(mocker):
    # Create mock comment instances
    mock_comments = [MagicMock(spec=Comment)]

    # Create a mock query object
    mock_query = MagicMock()
    mock_query.filter_by.return_value.all.return_value = mock_comments

    # Patch the Comment.query to return the mock query object
    mocker.patch('App.Models.Comment.CommentModel.Comment.query', mock_query)

    post_uid = 1
    result = get_comments_by_post_id(post_uid)
    
    assert result == mock_comments

def test_get_comments_by_post_id_with_error(mocker,test_client):
    mocker.patch('App.config.Config.SQLALCHEMY_DATABASE_URI', return_value=mock_create_connection())
    
    post_uid = "post_uid"
    
    with pytest.raises(Exception) as excinfo:
        get_comments_by_post_id(post_uid)
    assert str(excinfo.value) == "Database error"


# Test create_new_comment function
    
def test_create_new_comment_success(mocker, test_client):
    mock_comment = MagicMock(spec=Comment)
    mocker.patch('App.api.wrapper.schema.Comment', return_value=mock_comment)
    mocker.patch('App.api.wrapper.schema.db.session.add', lambda x: None)
    mocker.patch('App.api.wrapper.schema.db.session.commit', lambda: None)

    post_uid = 1
    user_uid = 1
    data = {'content': 'This is a comment.'}
    username = 'user'
    
    result = create_new_comment(post_uid, user_uid, data, username)
    
    assert result == mock_comment

def test_create_new_comment_with_error(mocker,test_client):
    mocker.patch('App.config.Config.SQLALCHEMY_DATABASE_URI', return_value=mock_create_connection())
    
    post_uid = "post_uid"
    user_uid = "user_uid"
    data = {"content": "Test comment"}
    username = "test_user"
    
    with pytest.raises(Exception) as excinfo:
        create_new_comment(post_uid, user_uid, data, username)
    assert str(excinfo.value) == "Database error"


# Test update_existing_comment function
    
def test_update_existing_comment_success(mocker, test_client):
    mock_comment = MagicMock(spec=Comment)
    mocker.patch('App.api.wrapper.schema.db.session.commit', lambda: None)

    data = {'content': 'Updated content.'}
    result = update_existing_comment(mock_comment, data)
    
    assert result is True

def test_update_existing_comment_with_error(mocker, test_client):
    # Mock the database session to raise an exception when commit is called
    mock_session = mocker.patch('App.api.wrapper.schema.db.session.commit')
    mock_session.side_effect = Exception("Database error")
    
    comment = MagicMock()
    data = {"content": "Updated content"}
    
    with pytest.raises(Exception) as excinfo:
        update_existing_comment(comment, data)
    
    # Verify that the raised exception matches the expected exception
    assert str(excinfo.value) == "Database error"



# Test delete_existing_comment function

def test_delete_existing_comment_success(mocker, test_client):
    mock_comment = MagicMock(spec=Comment)
    mocker.patch('App.api.wrapper.schema.db.session.delete', lambda x: None)
    mocker.patch('App.api.wrapper.schema.db.session.commit', lambda: None)

    result = delete_existing_comment(mock_comment)
    
    assert result is True

def test_delete_existing_comment_with_error(mocker, test_client):
    # Mock the session to raise an exception when delete or commit is called
    mocker.patch('App.api.wrapper.schema.db.session.delete', lambda x: None)
    mocker.patch('App.api.wrapper.schema.db.session.commit', side_effect=Exception("Database error"))

    comment = MagicMock()

    with pytest.raises(Exception) as excinfo:
        delete_existing_comment(comment)
    
    assert str(excinfo.value) == "Database error"





