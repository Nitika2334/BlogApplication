import pytest
from App import create_app, db

@pytest.fixture(scope='function')
def test_client():
    flask_app = create_app('testing')
    testing_client = flask_app.test_client()
    with flask_app.app_context():
        yield testing_client


@pytest.fixture
def mock_get_user_by_username(mocker):
    # Mock the get_user_by_username function
    mock_function = mocker.patch('App.api.wrapper.schema.get_user_by_username')
    return mock_function

@pytest.fixture
def mock_get_post_by_id(mocker):
    # Mock the get_post_by_id function
    mock_function = mocker.patch('App.api.wrapper.schema.get_post_by_id')
    return mock_function

@pytest.fixture
def mock_get_comments_by_post_id(mocker):
    # Mock the get_comments_by_post_id function
    mock_function = mocker.patch('App.api.wrapper.schema.get_comments_by_post_id')
    return mock_function


@pytest.fixture
def mock_create_new_comment(mocker):
    return mocker.patch('App.api.wrapper.schema.create_new_comment')
