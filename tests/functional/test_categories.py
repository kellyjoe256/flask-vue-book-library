"""
This file (test_categories.py) contains functional tests for categories endpoints
"""
from assertpy import assert_that
from flask_jwt_extended import create_access_token
from app.models import User
from app.helpers import convert_to_dict

base_route = '/api/categories'


def category_data():
    return dict(name='History')


def test_that_categories_are_deleted_correctly(client):
    """
    GIVEN a Flask application
    WHEN the `/api/categories/:id` route is called (DELETE) with valid credentials
    THEN check that the response meets the set conditions
    """
    user = User.query.first()
    access_token = create_access_token(identity=user)

    client.set_cookie('localhost', 'access_token', access_token)
    # create new category
    response = client.post(base_route, json=category_data())

    # delete created category
    response_data = convert_to_dict(response.data)
    response = client.delete(
        '{}/{}'.format(base_route, response_data.get('id')))

    assert_that(response.status_code).is_equal_to(204)
    assert_that(response.headers['Content-Type']).contains('application/json')


def test_that_categories_are_updated_correctly(client):
    """
    GIVEN a Flask application
    WHEN the `/api/categories/:id` route is called (PUT) with valid credentials
    WITH valid data
    THEN check that the response meets the set conditions
    """
    user = User.query.first()
    access_token = create_access_token(identity=user)

    client.set_cookie('localhost', 'access_token', access_token)
    # create new category
    data = category_data()
    response = client.post(base_route, json=data)

    # update created category
    response_data = convert_to_dict(response.data)
    data['name'] = 'Geography'
    response = client.put(
        '{}/{}'.format(base_route, response_data.get('id')), json=data)

    assert_that(response.status_code).is_equal_to(200)
    assert_that(response.headers['Content-Type']).contains('application/json')

    response_data = convert_to_dict(response.data)
    assert_that(response_data).contains_key('id', 'name')


def test_that_getting_existing_category_works(client):
    """
    GIVEN a Flask application
    WHEN the `/api/categories/:id` route is called (GET) with valid credentials
    BUT with an id that exists in the database
    THEN check that the response meets the set conditions
    """
    user = User.query.first()
    access_token = create_access_token(identity=user)

    # create new category
    client.set_cookie('localhost', 'access_token', access_token)
    response = client.post(base_route, json=category_data())

    response_data = convert_to_dict(response.data)
    # query the created category
    response = client.get('{}/{}'.format(base_route, response_data.get('id')))

    assert_that(response.status_code).is_equal_to(200)
    assert_that(response.headers['Content-Type']).contains('application/json')

    response_data = convert_to_dict(response.data)

    assert_that(response_data).contains_key('id', 'name')


def test_that_getting_non_existent_category_fails(client):
    """
    GIVEN a Flask application
    WHEN the `/api/categories/:id` route is called (GET) with valid credentials
    BUT with an id that does not exist in the database
    THEN check that the response meets the set conditions
    """
    user = User.query.first()
    access_token = create_access_token(identity=user)

    client.set_cookie('localhost', 'access_token', access_token)
    response = client.get('{}/12345'.format(base_route))

    assert_that(response.status_code).is_equal_to(404)


def test_that_categories_are_created_correctly(client):
    """
    GIVEN a Flask application
    WHEN the `/api/categories` route is posted (POST) to with valid credentials
    THEN check that the response meets the set conditions
    """
    user = User.query.first()
    access_token = create_access_token(identity=user)

    client.set_cookie('localhost', 'access_token', access_token)
    response = client.post(base_route, json=category_data())

    assert_that(response.status_code).is_equal_to(201)
    assert_that(response.headers['Content-Type']).contains('application/json')

    response_data = convert_to_dict(response.data)

    assert_that(response_data).contains_key('id', 'name')


def test_that_category_creation_fails_if_already_exists(client):
    """
    GIVEN a Flask application
    WHEN the `/api/categories` route is posted (POST) to with valid credentials
    BUT the category with given name exists
    THEN check that the response meets the set conditions
    """
    user = User.query.first()
    access_token = create_access_token(identity=user)

    client.set_cookie('localhost', 'access_token', access_token)
    # create new category
    client.post(base_route, json=category_data())
    # creating the same category again
    response = client.post(base_route, json=category_data())

    assert_that(response.status_code).is_equal_to(409)


def test_category_creation_required_fields(client):
    """
    GIVEN a Flask application
    WHEN the `/api/categories` route is posted (POST) to with valid credentials
    BUT required fields are not provided
    THEN check that the response status code is correct
    """
    user = User.query.first()
    access_token = create_access_token(identity=user)

    client.set_cookie('localhost', 'access_token', access_token)

    data = category_data()
    required_fields = ['name']
    for field in required_fields:
        del data[field]
        response = client.post(base_route, json=data)

        assert_that(response.status_code).is_greater_than_or_equal_to(400) \
            .is_less_than(500)


def test_that_categories_are_listed_correctly(client):
    """
    GIVEN a Flask application
    WHEN the `/api/categories` route is accessed (GET) with valid credentials
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
