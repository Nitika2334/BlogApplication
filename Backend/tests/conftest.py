import pytest
from App import create_app

@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app('testing')
    testing_client = flask_app.test_client()

    # No database creation or deletion here
    with flask_app.app_context():
        yield testing_client