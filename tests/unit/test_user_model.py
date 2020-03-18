"""
This file (test_user_model.py) contains the unit tests for the model User
in the models.py file
"""
from assertpy import assert_that


def test_new_user(new_user):
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the username and hashed_password fields are defined correctly
    """
    assert_that(new_user.username).is_equal_to('admin')
    assert_that(new_user.salt).is_length(32)
    assert_that(new_user.hashed_password).is_not_equal_to('password')


def test_that_the_repr_is_defined_for_user_model(new_user):
    """
    GIVEN a User model
    THEN check the `repr` representation of the model is defined
    """
    assert_that(repr(new_user)).is_equal_to('<User admin>')
