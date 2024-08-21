import pytest
from App import create_app, db


@pytest.fixture
def test_client():
    flask_app = create_app('testing')
    testing_client = flask_app.test_client()
    with flask_app.app_context():
        yield testing_client