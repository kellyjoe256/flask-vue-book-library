"""
This file (test_auth.py) contains functional tests for authentication endpoints
"""
from assertpy import assert_that
from flask_jwt_extended import create_access_token
from app.models import User

auth_base_route = '/api/auth'


def test_login_endpoint_with_valid_credentials(client, init_database):
    """
    GIVEN a Flask application
    WHEN the `/api/auth/login` route is posted to (POST) with valid credentials
    THEN check that the response is valid
    """
    route = '{}/login'.format(auth_base_route)
    credentials = dict(username='admin', password='password')
    response = client.post(route, data=credentials)

    assert_that(response.status_code).is_equal_to(200)
    assert_that(response.headers['Content-Type']).contains('application/json')

    # make sure the authentication token is set through a cookie
    set_cookie = response.headers['Set-Cookie']
    cookie = set_cookie.split(';')[0]
    token = cookie.split('=')[1]

    token_regex = r'^[A-Za-z0-9-_=]+\.[A-Za-z0-9-_=]+\.?[A-Za-z0-9-_.+/=]*$'
    assert_that(token).matches(token_regex)


def test_login_endpoint_with_invalid_credentials(client):
    """
    GIVEN a Flask application
    WHEN the `/api/auth/login` route is posted to (POST) with invalid credentials
    THEN check that the response is invalid
    """
    route = '{}/login'.format(auth_base_route)
    credentials = dict(username='does_not_exist', password='hello')
    response = client.post(route, data=credentials)

    assert_that(response.status_code).is_equal_to(401)


def test_logout_endpoint_with_valid_credentials(client, init_database):
    """
    GIVEN a Flask application
    WHEN the `/api/auth/logout` route is posted to (POST) with valid credentials
    THEN check that the response is valid
    """
    route = '{}/logout'.format(auth_base_route)
    user = User.query.filter(User.username == 'admin').first()
    access_token = create_access_token(identity=user.id)

    headers = dict(Authorization='Bearer ' + access_token)
    response = client.post(route, headers=headers)

    assert_that(response.status_code).is_equal_to(200)


def test_logout_endpoint_with_invalid_credentials(client):
    """
    GIVEN a Flask application
    WHEN the `/api/auth/logout` route is posted to (POST) with no / invalid credentials
    THEN check that the response is invalid
    """
    # no credentials
    route = '{}/logout'.format(auth_base_route)
    response = client.post(route)

    assert_that(response.status_code).is_equal_to(401)

    # invalid credentials
    headers = dict(Authorization='Bearer fake.token')
    response = client.post(route, headers=headers)

    assert_that(response.status_code).is_equal_to(401)


def test_me_endpoint_with_valid_credentials(client, init_database):
    """
    GIVEN a Flask application
    WHEN the `/api/auth/me` route is called (GET) with valid credentials
    THEN check that the response is valid
    """
    route = '{}/me'.format(auth_base_route)
    user = User.query.filter(User.username == 'admin').first()
    access_token = create_access_token(identity=user.id)

    headers = dict(Authorization='Bearer ' + access_token)
    response = client.get(route, headers=headers)

    assert_that(response.status_code).is_equal_to(200)
    assert_that(response.data).contains_key('id', 'username')


def test_me_endpoint_with_invalid_credentials(client):
    """
    GIVEN a Flask application
    WHEN the `/api/auth/me` route is called (GET) with no / invalid credentials
    THEN check that the response is invalid
    """
    # no credentials
    route = '{}/me'.format(auth_base_route)
    response = client.get(route)

    assert_that(response.status_code).is_equal_to(401)

    # invalid credentials
    headers = dict(Authorization='Bearer fake.token')
    response = client.get(route, headers=headers)

    assert_that(response.status_code).is_equal_to(401)
