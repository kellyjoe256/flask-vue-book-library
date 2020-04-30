"""
This file (test_book_model.py) contains the unit tests for the model
Book in the models.py file
"""
from assertpy import assert_that
from app.models import Book


def test_json_representation_of_book():
    """
    GIVEN a Book model
    WHEN a new Book is created
    THEN check the json representation of the new Book
    """
    book_data = dict(
        isbn='978-1-449-34284-5',
        title='The Art of War',
        num_of_pages=60,
        publisher='East India Publishing Company',
        publication_date='2018-12-17',
        about='Lorem ipsum dolor sit amet.',
    )
    book = Book(**book_data)
    book_json = book.json()

    assert_that(book_json).contains_value(60, 'The Art of War')
    assert_that(book_json).contains_key(
        'id', 'isbn', 'title', 'num_of_pages', 'publisher',
        'publication_date', 'about'
    )
