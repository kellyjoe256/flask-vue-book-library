"""
This file (test_books.py) contains functional tests for books endpoints
"""
from assertpy import assert_that
from flask_jwt_extended import create_access_token
from app.models import User
from app.helpers import convert_to_dict

base_route = '/api/books'


def book_data():
    return dict(
        isbn='978-1-449-34284-5',
        title='The Art of War',
        num_of_pages=60,
        publisher='East India Publishing Company',
        publication_date='2018-12-17',
        about='Lorem ipsum dolor sit amet.',
    )


def test_that_books_are_deleted_correctly(client):
    """
    GIVEN a Flask application
    WHEN the `/api/books/:id` route is called (DELETE) with valid credentials
    THEN check that the response meets the set conditions
    """
    user = User.query.first()
    access_token = create_access_token(identity=user)

    client.set_cookie('localhost', 'access_token', access_token)
    # create new book
    response = client.post(base_route, json=book_data())

    # delete created book
    response_data = convert_to_dict(response.data)
    response = client.delete(
        '{}/{}'.format(base_route, response_data.get('id')))

    assert_that(response.status_code).is_equal_to(204)
    assert_that(response.headers['Content-Type']).contains('application/json')


def test_that_books_are_updated_correctly(client):
    """
    GIVEN a Flask application
    WHEN the `/api/books/:id` route is called (PUT) with valid credentials
    WITH valid data
    THEN check that the response meets the set conditions
    """
    user = User.query.first()
    access_token = create_access_token(identity=user)

    client.set_cookie('localhost', 'access_token', access_token)
    # create new book
    data = book_data()
    response = client.post(base_route, json=data)

    # update created book
    response_data = convert_to_dict(response.data)
    data['title'] = 'The Art of Warring'
    response = client.put(
        '{}/{}'.format(base_route, response_data.get('id')), json=data)

    assert_that(response.status_code).is_equal_to(200)
    assert_that(response.headers['Content-Type']).contains('application/json')

    response_data = convert_to_dict(response.data)
    keys = ('id', 'isbn', 'title', 'num_of_pages',
            'publisher', 'publication_date',)

    assert_that(response_data).contains_key(*keys)


def test_that_getting_existing_book_works(client):
    """
    GIVEN a Flask application
    WHEN the `/api/books/:id` route is called (GET) with valid credentials
    BUT with an id that exists in the database
    THEN check that the response meets the set conditions
    """
    user = User.query.first()
    access_token = create_access_token(identity=user)

    # create an books
    client.set_cookie('localhost', 'access_token', access_token)
    response = client.post(base_route, json=book_data())

    response_data = convert_to_dict(response.data)

    # query the created book
    response = client.get('{}/{}'.format(base_route, response_data.get('id')))

    assert_that(response.status_code).is_equal_to(200)
    assert_that(response.headers['Content-Type']).contains('application/json')

    response_data = convert_to_dict(response.data)
    keys = ('id', 'isbn', 'title', 'num_of_pages',
            'publisher', 'publication_date', 'authors', 'categories',)

    assert_that(response_data).contains_key(*keys)


def test_that_getting_non_existent_book_fails(client):
    """
    GIVEN a Flask application
    WHEN the `/api/books/:id` route is called (GET) with valid credentials
    BUT with an id that does not exist in the database
    THEN check that the response meets the set conditions
    """
    user = User.query.first()
    access_token = create_access_token(identity=user)

    client.set_cookie('localhost', 'access_token', access_token)
    response = client.get('{}/12345'.format(base_route))

    assert_that(response.status_code).is_equal_to(404)


def test_that_books_are_created_correctly(client):
    """
    GIVEN a Flask application
    WHEN the `/api/books` route is posted (POST) to with valid credentials
    THEN check that the response meets the set conditions
    """
    user = User.query.first()
    access_token = create_access_token(identity=user)

    client.set_cookie('localhost', 'access_token', access_token)
    response = client.post(base_route, json=book_data())

    assert_that(response.status_code).is_equal_to(201)
    assert_that(response.headers['Content-Type']).contains('application/json')

    response_data = convert_to_dict(response.data)
    keys = ('id', 'isbn', 'title', 'num_of_pages',
            'publisher', 'publication_date',)

    assert_that(response_data).contains_key(*keys)


def test_that_book_creation_if_isbn_already_exists(client):
    """
    GIVEN a Flask application
    WHEN the `/api/books` route is posted (POST) to with valid credentials
    BUT isbn is already exists 
    THEN check that the response status code is correct
    """
    user = User.query.first()
    access_token = create_access_token(identity=user)

    client.set_cookie('localhost', 'access_token', access_token)

    # create book
    client.post(base_route, json=book_data())
    # trying creating new book with same isbn
    response = client.post(base_route, json=book_data())

    assert_that(response.status_code).is_equal_to(409)


def test_book_creation_required_fields(client):
    """
    GIVEN a Flask application
    WHEN the `/api/books` route is posted (POST) to with valid credentials
    BUT required fields are not provided
    THEN check that the response status code is correct
    """
    user = User.query.first()
    access_token = create_access_token(identity=user)

    client.set_cookie('localhost', 'access_token', access_token)

    data = book_data()
    required_fields = ['isbn', 'title', 'num_of_pages',
                       'publisher', 'publication_date', ]
    for field in required_fields:
        del data[field]
        response = client.post(base_route, json=data)

        assert_that(response.status_code).is_greater_than_or_equal_to(400) \
            .is_less_than(500)


def test_that_books_are_listed_correctly(client):
    """
    GIVEN a Flask application
    WHEN the `/api/books` route is accessed (GET) with valid credentials
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
