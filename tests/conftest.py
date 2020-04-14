import pytest
from app import create_app, db
from app.models import User

config_name = 'testing'


@pytest.fixture
def app():
    app = create_app(config_name)
    return app


@pytest.fixture(scope='module')
def new_user():
    user_data = dict(username='admin', password='password')
    return User(**user_data), user_data


@pytest.fixture(scope='module')
def init_database():
    app = create_app(config_name)

    # Create the database and the database table
    with app.app_context():
        db.create_all()

        # Create user
        user = User(username='admin', password='password')
        user.save()

    yield db

    with app.app_context():
        db.drop_all()
