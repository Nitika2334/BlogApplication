import pytest
from unittest.mock import MagicMock
from App import db

from App.Models.User.UserModel import User
from App.Models.Post.PostModel import Post
from App.Models.Comment.CommentModel import Comment
from App.api.wrapper.schema import (
    get_user_by_username,
    get_user_by_email,
    get_user_by_user_id,
    add_user,
    get_post_by_id,
    get_comment_by_comment_id,
    get_comments_by_post_id,
    create_new_comment,
    update_existing_comment,
    delete_existing_comment
)

class MockQuery:
    def __init__(self, data):
        self.data = data

    def filter_by(self, **kwargs):
        filtered_data = [item for item in self.data if all(getattr(item, k) == v for k, v in kwargs.items())]
        return MockQuery(filtered_data)

    def first(self):
        return self.data[0] if self.data else None

    def all(self):
        return self.data

    def count(self):
        return len(self.data)

    def order_by(self, *args):
        # Simulate ordering
        return self

    def offset(self, offset):
        # Simulate offset
        return self

    def limit(self, limit):
        # Simulate limit
        return self

class MockSession:
    def __init__(self, data):
        self.data = data

    def query(self, model):
        return MockQuery([item for item in self.data if isinstance(item, model)])

    def add(self, item):
        self.data.append(item)

    def commit(self):
        pass  # No operation needed for mock

    def rollback(self):
        pass  # No operation needed for mock

    def delete(self, item):
        if item in self.data:
            self.data.remove(item)


# Sample Data
user_data = [User(username="test_user", email="test@example.com", uid=1, password="password")]
post_data = [Post(uid=1, title="Test Post", content="Content", user_uid=1, username="test_user")]
comment_data = [Comment(uid=1, content="Test Comment", user_uid=1, post_uid=1, username="test_user")]

@pytest.fixture
def mock_db(mocker):
    mock_session = MockSession(user_data + post_data + comment_data)
    mocker.patch('App.api.wrapper.schema.db.session', mock_session)
    return mock_session

def test_get_user_by_username(mock_db):
    user = get_user_by_username("test_user")
    assert user.username == "test_user"

def test_get_user_by_email(mock_db):
    user = get_user_by_email("test@example.com")
    assert user.email == "test@example.com"

def test_get_user_by_user_id(mock_db):
    user = get_user_by_user_id(1)
    assert user.uid == 1

def test_add_user(mock_db):
    new_user = add_user("new_user", "new@example.com", "newpassword")
    assert new_user.username == "new_user"
    assert len(mock_db.data) == 4  # 3 existing + 1 new user


def test_get_post_by_id(mock_db):
    post = get_post_by_id(1)
    assert post.uid == 1


def test_get_comment_count_for_post(mock_db):
    count = get_comment_count_for_post(1)
    assert count == 1

def test_get_comment_by_comment_id(mock_db):
    comment = get_comment_by_comment_id(1)
    assert comment.uid == 1

def test_get_comments_by_post_id(mock_db):
    comments = get_comments_by_post_id(1)
    assert len(comments) == 1

def test_create_new_comment(mock_db):
    new_comment = create_new_comment(1, 1, {"content": "Another Comment"}, "test_user")
    assert new_comment.content == "Another Comment"
    assert len(mock_db.data) == 4  # 2 existing (1 post, 1 comment) + 1 new comment

def test_update_existing_comment(mock_db):
    comment = mock_db.query(Comment).filter_by(uid=1).first()
    result = update_existing_comment(comment, {"content": "Updated Comment"})
    assert comment.content == "Updated Comment"
    assert result is True

def test_delete_existing_comment(mock_db):
    comment = mock_db.query(Comment).filter_by(uid=1).first()
    result = delete_existing_comment(comment)
    assert result is True
    assert len(mock_db.data) == 2  # Comment should be deleted, so 2 items left (1 user, 1 post)

