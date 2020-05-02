import pytest
from app import create_app, db
from app.models import User

config_name = 'testing'
user_data = [
    dict(username='admin', password='password', is_admin=True),
    dict(username='non_admin', password='password', is_admin=False),
]


@pytest.fixture
def app():
    app = create_app(config_name)
    with app.app_context():
        db.create_all()

        # Create users
        for data in user_data:
            user = User(**data)
            user.save()

        yield app

        db.session.remove()
        db.drop_all()


@pytest.fixture(scope='module')
def new_user():
    data = user_data[0]
    return User(**data), data
