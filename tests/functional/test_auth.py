"""
This file (test_auth.py) contains functional tests for authentication endpoints
"""
from datetime import datetime
from assertpy import assert_that
from werkzeug.http import parse_cookie
from flask_jwt_extended import create_access_token
from app.models import User
from app.helpers import convert_to_dict

base_route = '/api/auth'


def test_that_login_returns_correct_status_code(client):
    """
    GIVEN a Flask application
    WHEN the `/api/auth/login` route is posted to (POST) with valid credentials
    THEN check that the response status code is correct
    """
    route = '{}/login'.format(base_route)
    credentials = dict(username='admin', password='password')
    response = client.post(route, data=credentials)

    assert_that(response.status_code).is_equal_to(200)


def test_that_login_returns_correct_content_type(client):
    """
    GIVEN a Flask application
    WHEN the `/api/auth/login` route is posted to (POST) with valid credentials
    THEN check that the response content type is correct
    """
    route = '{}/login'.format(base_route)
    credentials = dict(username='admin', password='password')
    response = client.post(route, data=credentials)

    assert_that(response.headers['Content-Type']).contains('application/json')


def test_that_login_returns_a_valid_token(client):
    """
    GIVEN a Flask application
    WHEN the `/api/auth/login` route is posted to (POST) with valid credentials
    THEN check that a valid token is sent through a cookie
    """
    route = '{}/login'.format(base_route)
    credentials = dict(username='admin', password='password')
    response = client.post(route, data=credentials)

    # make sure the authentication token is set through a cookie
    cookies = response.headers.getlist('Set-Cookie')
    items = [list(parse_cookie(cookie).items())[0] for cookie in cookies]
    cookies_dict = {key: value for key, value in items}
    token = cookies_dict.get('access_token', '')

    token_regex = r'^[A-Za-z0-9-_=]+\.[A-Za-z0-9-_=]+\.?[A-Za-z0-9-_.+/=]*$'

    assert_that(token).matches(token_regex)


def test_that_login_fails_with_invalid_credentials(client):
    """
    GIVEN a Flask application
    WHEN the `/api/auth/login` route is posted to (POST) with invalid credentials
    THEN check that the response status code is correct
    """
    route = '{}/login'.format(base_route)
    credentials = dict(username='does_not_exist', password='hello')
    response = client.post(route, data=credentials)

    assert_that(response.status_code).is_greater_than_or_equal_to(400) \
        .is_less_than_or_equal_to(500)


def test_that_logout_returns_correct_status_code(client):
    """
    GIVEN a Flask application
    WHEN the `/api/auth/logout` route is posted to (POST) with valid credentials
    THEN check that the status code is correct
    """
    route = '{}/logout'.format(base_route)
    user = User.query.first()
    access_token = create_access_token(identity=user)

    client.set_cookie('localhost', 'access_token', access_token)
    response = client.post(route)

    assert_that(response.status_code).is_equal_to(200)


def test_that_logout_removes_token(client):
    """
    GIVEN a Flask application
    WHEN the `/api/auth/logout` route is posted to (POST) with valid credentials
    THEN check that the current auth token is being removed 
    """
    route = '{}/logout'.format(base_route)
    user = User.query.first()
    access_token = create_access_token(identity=user)

    client.set_cookie('localhost', 'access_token', access_token)
    response = client.post(route)

    cookie = response.headers.getlist('Set-Cookie').pop(0)
    _, cookie_expiration = list(parse_cookie(cookie).items())[1]
    today = datetime.today()
    cookie_expiration_date = datetime.strptime(
        cookie_expiration, '%a, %d-%b-%Y %H:%M:%S GMT')

    assert_that(cookie_expiration_date).is_before(today)


def test_logout_with_no_credentials(client):
    """
    GIVEN a Flask application
    WHEN the `/api/auth/logout` route is posted to (POST) with no credentials
    THEN check that the response status code is valid
    """
    route = '{}/logout'.format(base_route)
    response = client.post(route)

    assert_that(response.status_code).is_equal_to(401)


def test_logout_with_invalid_credentials(client):
    """
    GIVEN a Flask application
    WHEN the `/api/auth/logout` route is posted to (POST) with invalid credentials
    THEN check that the response status code is within the valid range
    """
    route = '{}/logout'.format(base_route)
    client.set_cookie('localhost', 'access_token', 'fake-token')
    response = client.post(route)

    assert_that(response.status_code).is_greater_than_or_equal_to(400) \
        .is_less_than_or_equal_to(500)


def test_that_me_returns_correct_status_code(client):
    """
    GIVEN a Flask application
    WHEN the `/api/auth/me` route is called (GET) with valid credentials
    THEN check that the response status code is correct
    """
    route = '{}/me'.format(base_route)
    user = User.query.first()
    access_token = create_access_token(identity=user)

    client.set_cookie('localhost', 'access_token', access_token)
    response = client.get(route)

    assert_that(response.status_code).is_equal_to(200)


def test_that_me_returns_current_user_data(client):
    """
    GIVEN a Flask application
    WHEN the `/api/auth/me` route is called (GET) with valid credentials
    THEN check that the response data contains current user details
    """
    route = '{}/me'.format(base_route)
    user = User.query.first()
    access_token = create_access_token(identity=user)

    client.set_cookie('localhost', 'access_token', access_token)
    response = client.get(route)

    response_data = convert_to_dict(response.data)

    assert_that(response_data).contains_key('id', 'username')


def test_me_with_no_credential(client):
    """
    GIVEN a Flask application
    WHEN the `/api/auth/me` route is called (GET) with no credentials
    THEN check that the response status code is valid
    """
    route = '{}/me'.format(base_route)
    response = client.get(route)

    assert_that(response.status_code).is_equal_to(401)


def test_me_with_invalid_credentials(client):
    """
    GIVEN a Flask application
    WHEN the `/api/auth/me` route is called (GET) with invalid credentials
    THEN check that the response status code is within the valid range
    """
    route = '{}/me'.format(base_route)
    client.set_cookie('localhost', 'access_token', 'fake-token')
    response = client.get(route)

    assert_that(response.status_code).is_greater_than_or_equal_to(400) \
        .is_less_than_or_equal_to(500)
