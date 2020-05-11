"""
This file (test_users.py) contains functional tests for users endpoints
"""
from assertpy import assert_that
from flask_jwt_extended import create_access_token
from app.models import User
from app.helpers import convert_to_dict

base_route = '/api/users'


def user_data():
    return dict(username='new_user', password='password')


def test_that_users_deleted_correctly(client):
    """
    GIVEN a Flask application
    WHEN the `/api/users/:id` route is called (DELETE) with valid credentials
    THEN check that the response meets the set conditions
    """
    user = User.query.filter(User.is_admin == True).first()
    access_token = create_access_token(identity=user)

    client.set_cookie('localhost', 'access_token', access_token)
    # create new user
    response = client.post(base_route, json=user_data())

    # delete created user
    response_data = convert_to_dict(response.data)
    response = client.delete(
        '{}/{}'.format(base_route, response_data.get('id')))

    assert_that(response.status_code).is_equal_to(204)
    assert_that(response.headers['Content-Type']).contains('application/json')


def test_that_users_updated_correctly(client):
    """
    GIVEN a Flask application
    WHEN the `/api/users/:id` route is called (PUT) with valid credentials
    WITH valid data
    THEN check that the response meets the set conditions
    """
    user = User.query.filter(User.is_admin == True).first()
    access_token = create_access_token(identity=user)

    client.set_cookie('localhost', 'access_token', access_token)
    data = user_data()
    # create new user
    response = client.post(base_route, json=data)

    # update created user
    response_data = convert_to_dict(response.data)
    data['username'] = 'new_username'
    response = client.put(
        '{}/{}'.format(base_route, response_data.get('id')), json=data)

    assert_that(response.status_code).is_equal_to(200)
    assert_that(response.headers['Content-Type']).contains('application/json')

    response_data = convert_to_dict(response.data)

    assert_that(response_data).contains_key('id', 'username', 'is_admin')


def test_that_getting_existing_user_works(client):
    """
    GIVEN a Flask application
    WHEN the `/api/users/:id` route is called (GET) with valid credentials
    BUT with an id that exists in the database
    THEN check that the response meets the set conditions
    """
    user = User.query.filter(User.is_admin == True).first()
    access_token = create_access_token(identity=user)

    client.set_cookie('localhost', 'access_token', access_token)
    response = client.get('{}/2'.format(base_route))

    assert_that(response.status_code).is_equal_to(200)
    assert_that(response.headers['Content-Type']).contains('application/json')

    response_data = convert_to_dict(response.data)

    assert_that(response_data).contains_key('id', 'username', 'is_admin')


def test_that_getting_non_existent_user_fails(client):
    """
    GIVEN a Flask application
    WHEN the `/api/users/:id` route is called (GET) with valid credentials
    BUT with an id that does not exist in the database
    THEN check that the response meets the set conditions
    """
    user = User.query.filter(User.is_admin == True).first()
    access_token = create_access_token(identity=user)

    client.set_cookie('localhost', 'access_token', access_token)
    response = client.get('{}/12345'.format(base_route))

    assert_that(response.status_code).is_equal_to(404)


def test_that_users_are_created_correctly(client):
    """
    GIVEN a Flask application
    WHEN the `/api/users` route is posted (POST) to with valid credentials
    THEN check that the response meets the set conditions
    """
    user = User.query.filter(User.is_admin == True).first()
    access_token = create_access_token(identity=user)

    client.set_cookie('localhost', 'access_token', access_token)
    response = client.post(base_route, json=user_data())

    assert_that(response.status_code).is_equal_to(201)
    assert_that(response.headers['Content-Type']).contains('application/json')

    response_data = convert_to_dict(response.data)

    assert_that(response_data).contains_key('id', 'username', 'is_admin')


def test_that_user_creation_fails_if_username_exists(client):
    """
    GIVEN a Flask application
    WHEN the `/api/users` route is posted (POST) to with valid credentials
    BUT with existing username
    THEN check that the response meets the set conditions
    """
    user = User.query.filter(User.is_admin == True).first()
    access_token = create_access_token(identity=user)

    client.set_cookie('localhost', 'access_token', access_token)
    client.post(base_route, json=user_data())
    response = client.post(base_route, json=user_data())

    assert_that(response.status_code).is_equal_to(409)


def test_user_creation_required_fields(client):
    """
    GIVEN a Flask application
    WHEN the `/api/users` route is posted (POST) to with valid credentials
    BUT required fields are not provided
    THEN check that the response status code is correct
    """
    user = User.query.filter(User.is_admin == True).first()
    access_token = create_access_token(identity=user)

    client.set_cookie('localhost', 'access_token', access_token)

    data = user_data()
    required_fields = ['username', 'password']
    for field in required_fields:
        del data[field]
        response = client.post(base_route, json=data)

        assert_that(response.status_code).is_greater_than_or_equal_to(400) \
            .is_less_than(500)


def test_that_users_are_listed_correctly(client):
    """
    GIVEN a Flask application
    WHEN the `/api/users` route is accessed (GET) with valid credentials
    THEN check that the response meets the set conditions
    """
    user = User.query.filter(User.is_admin == True).first()
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


def test_that_all_fails_for_non_admin_user(client):
    """
    GIVEN a Flask application
    WHEN the any of the `users` endpoints are called for non admin user
    THEN check that response status code is correct
    """
    actions = dict(
        get=[base_route, '{}/1'.format(base_route)],
        post=base_route,
        put='{}/1'.format(base_route),
        delete='{}/1'.format(base_route),
    )
    status_codes = []

    user = User.query.filter(User.is_admin == False).first()
    access_token = create_access_token(identity=user)
    client.set_cookie('localhost', 'access_token', access_token)
    for method, route in actions.items():
        if type(route) is not list:
            response = getattr(client, method)(route, data={})
            status_codes.append(response.status_code)
        else:
            for sub_route in route:
                response = getattr(client, method)(sub_route, data={})
                status_codes.append(response.status_code)

    assert_that(all(map(lambda x: x == 401, status_codes))).is_true()
