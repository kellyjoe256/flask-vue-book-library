"""
This file (test_categories_model.py) contains the unit tests for the model
Category in the models.py file
"""
from assertpy import assert_that
from app.models import Category


def test_json_representation_of_category():
    """
    GIVEN a Category model
    WHEN a new Category is created
    THEN check the json representation of the new Category
    """
    category = Category(name='fiction')
    category_json = category.json()

    assert_that(category_json).contains_value('fiction')
    assert_that(category_json).contains_key('id', 'name')
