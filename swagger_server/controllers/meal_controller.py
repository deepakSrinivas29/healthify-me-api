import connexion
import six
from flask import Response, make_response, jsonify
import json

from swagger_server.models.meal import Meal  # noqa: E501
from swagger_server import util
import swagger_server.controllers.utils as Nutrionix
from swagger_server.encoder import JSONEncoder

users_meal = {}
meals = {}  # meal_id: body

def add_meal(body):  # noqa: E501
    """Add meal

    This can only be done by the logged in user. # noqa: E501

    :param body: Meal object to Add
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = Meal.from_dict(connexion.request.get_json())  # noqa: E501

    try:
        if not body.calorie:
            body.calorie = int(Nutrionix.fetch_calories(body.food_name))

    except Exception as e:
        print("Failed to reach Nutrionix: "+str(e))
        body.calorie = 0

    meals[body.meal_id] = body
    return body


def delete_meal(meal_id):  # noqa: E501
    """Delete meal entry

    This can only be done by the logged in user. # noqa: E501

    :param meal_id: The meal that needs to be deleted.
    :type meal_id: str

    :rtype: None
    """
    meal_id = int(meal_id)

    if meal_id not in meals:
        msg='Meal not found!'
        return make_response(msg,404)

    del meals[meal_id]

    return make_response("Successfully deleted meal!",200)


def get_meal_by_meal_id(meal_id):  # noqa: E501
    """Get meal by meal id

    Get Meal by specifying the meal ID # noqa: E501

    :param meal_id: The meal that needs to be fetched.
    :type meal_id: str

    :rtype: Meal
    """
    meal_id = int(meal_id)

    if meal_id not in meals:
        msg='Meal not found!'
        return make_response(msg,404)

    return make_response(JSONEncoder().default(meals[meal_id]))
    # return json.JSONEncoder().encode(meals[meal_id])
    # return json.dumps(meals[meal_id])

def update_meal(meal_id, body):  # noqa: E501
    """Update Meal entry

    This can only be done by the logged in user. # noqa: E501

    :param meal_id: meal that needs to be updated
    :type meal_id: str
    :param body: Updated meal object
    :type body: dict | bytes

    :rtype: None
    """
    meal_id = int(meal_id)

    if meal_id not in meals:
        msg='Meal not found!'
        return make_response(msg,404)

    if connexion.request.is_json:
        body = Meal.from_dict(connexion.request.get_json())  # noqa: E501

    # Check for the match b/w meal_id and body.meal_id
    if meal_id != body.meal_id:
        msg = "No match between Meal ids!"
        return make_response(msg, 400)

    # if body doesn't have calories as input
    try:
        if not body.calorie:
            body.calorie = int(Nutrionix.fetch_calories(body.food_name))

    except Exception as e:
        print("Failed to reach Nutrionix: "+str(e))
        body.calorie = 0

    meals[meal_id] = body
    desc = f'Successfully updated meal with Meal id: {meal_id}'

    response = {'message': desc, "updated_meal": body}

    return jsonify(response)
