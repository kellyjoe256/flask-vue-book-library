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
    user, _ = new_user

    assert_that(repr(user)).matches(r"\<User '[\w_-]+?'\>")
    assert_that(user.salt).is_length(32)
    assert_that(len(user.hashed_password)).is_greater_than(50)


def test_that_correct_password_returns_true(new_user):
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check that a correct password returns TRUE
    """
    user, user_data = new_user

    assert_that(user.verify_password(user_data.get('password'))).is_true()


def test_that_an_incorrect_password_returns_false(new_user):
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check that an incorrect password returns FALSE
    """
    user, user_data = new_user
    password = 'x{}x'.format(user_data.get('password'))

    assert_that(user.verify_password(password)).is_false()


def test_json_representation_of_user(new_user):
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the json representation of the new User
    """
    user, user_data = new_user
    user_json = user.json()

    acceptable_keys = 'id', 'username', 'created_at', 'is_admin'
    unacceptable_keys = 'salt', 'password', 'hashed_password'

    assert_that(user_json).contains_value(user_data.get('username'))
    assert_that(user_json).contains_key(*acceptable_keys)
    assert_that(user_json).does_not_contain_key(*unacceptable_keys)
