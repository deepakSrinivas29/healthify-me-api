import connexion
import six
import json

from flask import make_response, jsonify
from swagger_server.models.user import User  # noqa: E501
from swagger_server import util
from swagger_server.encoder import JSONEncoder

users = {}
logged_users = set()

def create_user(body):  # noqa: E501
    """Create user

    This can only be done by the logged in user. # noqa: E501

    :param body: Created user object
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = User.from_dict(connexion.request.get_json())  # noqa: E501

    if body.username in users:
        return make_response("Username already taken!", 400)

    users[body.username] = body

    return make_response("Successfully created user!", 200)


def delete_user(username):  # noqa: E501
    """Delete user

    This can only be done by the logged in user. # noqa: E501

    :param username: The name that needs to be deleted
    :type username: str

    :rtype: None
    """

    if username not in users:
        return make_response("Username not found!", 404)

    del users[username]

    return make_response("Successfully deleted user!", 200)


def get_user_by_name(username):  # noqa: E501
    """Get user by user name

     # noqa: E501

    :param username: The name that needs to be fetched. Use user1 for testing.
    :type username: str

    :rtype: User
    """

    if username in users:
        return make_response(JSONEncoder().default(users[username]))

    return make_response("User not found!", 404)


def login_user(username, password):  # noqa: E501
    """Logs user into the system

     # noqa: E501

    :param username: The user name for login
    :type username: str
    :param password: The password for login in clear text
    :type password: str

    :rtype: str
    """
    # Check if user exists
    if username in users:

        # Check if password matches
        if password == users[username].password:
            return make_response("Login successful!", 200)

        return make_response("Invalid password!", 401)

    return make_response("Invalid Username!", 401)


def logout_user():  # noqa: E501
    """Logs out current logged in user session

     # noqa: E501


    :rtype: None
    """
    return make_response("Successfully logged out!", 200)


def update_user(username, body):  # noqa: E501
    """Updated user

    This can only be done by the logged in user. # noqa: E501

    :param username: name that need to be updated
    :type username: str
    :param body: Updated user object
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = User.from_dict(connexion.request.get_json())  # noqa: E501

    if username in users:
        users[username] = body
        return make_response("Update successful!", 200)

    return make_response("User not found!", 404)
