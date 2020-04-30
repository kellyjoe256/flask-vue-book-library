"""
This file (test_author_model.py) contains the unit tests for the model
Author in the models.py file
"""
from assertpy import assert_that
from app.models import Author


def test_json_representation_of_author():
    """
    GIVEN a Author model
    WHEN a new Author is created
    THEN check the json representation of the new Author
    """
    author_data = dict(
        first_name = 'John',
        last_name = 'Doe',
        gender = 'M',
        about = 'Lorem ipsum dolor sit amet.',
    )
    author = Author(**author_data)
    author_json = author.json()

    assert_that(author_json).contains_value('John', 'Doe', 'M')
    assert_that(author_json).contains_key(
        'first_name', 'last_name', 'gender', 'about'
    )
