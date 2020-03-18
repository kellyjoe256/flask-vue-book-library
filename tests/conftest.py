import pytest
from app import create_app
from app.models import User


@pytest.fixture
def app():
    config_name = 'testing'
    app = create_app(config_name)
    return app


@pytest.fixture(scope='module')
def new_user():
    user_data = dict(username='admin', password='password')
    return User(**user_data)
