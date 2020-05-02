"""
This file (test_authors.py) contains functional tests for authors endpoints
"""
from assertpy import assert_that
from flask_jwt_extended import create_access_token
from app.models import User
from app.helpers import convert_to_dict

base_route = '/api/authors'


def author_data():
    return dict(
        last_name='Mark',
        first_name='Twaikn',
        gender='M',
        about='**Exceptional** author',
    )


def test_that_authors_are_deleted_correctly(client):
    """
    GIVEN a Flask application
    WHEN the `/api/authors/:id` route is called (DELETE) with valid credentials
    THEN check that the response meets the set conditions
    """
    user = User.query.first()
    access_token = create_access_token(identity=user)

    client.set_cookie('localhost', 'access_token', access_token)
    # create new author
    response = client.post(base_route, json=author_data())

    # delete created author
    response_data = convert_to_dict(response.data)
    response = client.delete(
        '{}/{}'.format(base_route, response_data.get('id')))

    assert_that(response.status_code).is_equal_to(204)
    assert_that(response.headers['Content-Type']).contains('application/json')


def test_that_authors_are_updated_correctly(client):
    """
    GIVEN a Flask application
    WHEN the `/api/authors/:id` route is called (PUT) with valid credentials
    WITH valid data
    THEN check that the response meets the set conditions
    """
    user = User.query.first()
    access_token = create_access_token(identity=user)

    client.set_cookie('localhost', 'access_token', access_token)
    # create new author
    data = author_data()
    response = client.post(base_route, json=data)

    # update created author
    response_data = convert_to_dict(response.data)
    data['first_name'] = 'Twain'
    response = client.put(
        '{}/{}'.format(base_route, response_data.get('id')), json=data)
    assert_that(response.status_code).is_equal_to(200)
    assert_that(response.headers['Content-Type']).contains('application/json')

    response_data = convert_to_dict(response.data)
    keys = ('id', 'first_name', 'last_name', 'gender', 'about')

    assert_that(response_data).contains_key(*keys)


def test_that_getting_existing_author_works(client):
    """
    GIVEN a Flask application
    WHEN the `/api/authors/:id` route is called (GET) with valid credentials
    BUT with an id that exists in the database
    THEN check that the response meets the set conditions
    """
    user = User.query.first()
    access_token = create_access_token(identity=user)

    # create new author
    client.set_cookie('localhost', 'access_token', access_token)
    response = client.post(base_route, json=author_data())

    # query the created author
    response_data = convert_to_dict(response.data)
    response = client.get('{}/{}'.format(base_route, response_data.get('id')))

    assert_that(response.status_code).is_equal_to(200)
    assert_that(response.headers['Content-Type']).contains('application/json')

    response_data = convert_to_dict(response.data)
    keys = ('id', 'first_name', 'last_name', 'gender', 'about', 'books',)

    assert_that(response_data).contains_key(*keys)


def test_that_getting_non_existent_author_fails(client):
    """
    GIVEN a Flask application
    WHEN the `/api/authors/:id` route is called (GET) with valid credentials
    BUT with an id that does not exist in the database
    THEN check that the response meets the set conditions
    """
    user = User.query.first()
    access_token = create_access_token(identity=user)

    client.set_cookie('localhost', 'access_token', access_token)
    response = client.get('{}/12345'.format(base_route))

    assert_that(response.status_code).is_equal_to(404)


def test_that_authors_are_created_correctly(client):
    """
    GIVEN a Flask application
    WHEN the `/api/authors` route is posted (POST) to with valid credentials
    THEN check that the response meets the set conditions
    """
    user = User.query.first()
    access_token = create_access_token(identity=user)

    client.set_cookie('localhost', 'access_token', access_token)
    response = client.post(base_route, json=author_data())

    assert_that(response.status_code).is_equal_to(201)
    assert_that(response.headers['Content-Type']).contains('application/json')

    response_data = convert_to_dict(response.data)
    keys = ('id', 'first_name', 'last_name', 'gender', 'about')

    assert_that(response_data).contains_key(*keys)


def test_author_creation_required_fields(client):
    """
    GIVEN a Flask application
    WHEN the `/api/authors` route is posted (POST) to with valid credentials
    BUT required fields are not provided
    THEN check that the response status code is correct
    """
    user = User.query.first()
    access_token = create_access_token(identity=user)

    client.set_cookie('localhost', 'access_token', access_token)

    data = author_data()
    required_fields = ['first_name', 'last_name', 'gender', 'about']
    for field in required_fields:
        del data[field]
        response = client.post(base_route, json=data)

        assert_that(response.status_code).is_greater_than_or_equal_to(400) \
            .is_less_than(500)


def test_that_authors_are_listed_correctly(client):
    """
    GIVEN a Flask application
    WHEN the `/api/authors` route is accessed (GET) with valid credentials
    THEN check that the response meets the set conditions
    """
    user = User.query.first()
    access_token = create_access_token(identity=user)

    client.set_cookie('localhost', 'access_token', access_token)
    response = client.get(base_route)

    assert_that(response.status_code).is_equal_to(200)
    assert_that(response.headers['Content-Type']).contains('application/json')

    response_data = convert_to_dict(response.data)

    assert_that(response_data).contains_key('data', 'links', 'meta')

    links_keys = ('first', 'last', 'next', 'previous')
    assert_that(response_data.get('links')).contains_key(*links_keys)

    meta_keys = ('current_page', 'last_page', 'per_page', 'total')
    assert_that(response_data.get('meta')).contains_key(*meta_keys)
