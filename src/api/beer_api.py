"""
This is the script that creates an API for interacting with the database
This script handles routing to the API endpoints and uses the helper functions from
beer_app.py in order to interact with the database
The API uses OpenAPI documentation which is described in static/swagger.yml
The API also uses SwaggerUI for visualization and documentation
SwaggerUI can be accessed at {API_URL}{API_PORT}/api, which by default is http://127.0.0.1:8080/api
"""

from flask import Flask, request
from flask_swagger_ui import get_swaggerui_blueprint
from api_functions import *

api = Flask(__name__)

SWAGGER_URL = "/api"
API_URL = "/static/swagger.yml"
swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': 'Access API'
    }
)
api.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)


@api.route(SWAGGER_URL + "/beers", methods=['GET'])
def all_beers():
    return get_all_beer_info()


@api.route(SWAGGER_URL + "/beers/<beer_id>", methods=['GET'])
def beer_info(beer_id: int):
    return get_beer_info(beer_id)


# @api.route(SWAGGER_URL + "/beers/test_1", methods=['GET'])
# def test_beer_info(beer_id=1):
#     return get_beer_info(beer_id)


@api.route(SWAGGER_URL + "/contribute", methods=['GET', 'POST'])
def contribute():
    if request.method == 'POST':
        beer_dict = request.json
        response = add_beer_to_db(beer_dict)
        return response


def start_api():
    api.run(host="0.0.0.0", port=8080, debug=True)


if __name__ == '__main__':
    start_api()
