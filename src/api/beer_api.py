from flask import Flask
from flask_swagger_ui import get_swaggerui_blueprint
from src.app.beer_app import *

api = Flask(__name__)

URL_PREFIX = '/api'

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


@api.route(URL_PREFIX + "/beers", methods=['GET'])
def all_beers():
    return get_all_beer_info()


@api.route(URL_PREFIX + "/beers/<beer_id>", methods=['GET'])
def beer_info(beer_id: int):
    return get_beer_info(beer_id)


@api.route(URL_PREFIX + "/beers/test_1", methods=['GET'])
def test_beer_info(beer_id=1):
    return get_beer_info(beer_id)


def start_api():
    api.run(host="0.0.0.0", port=8080, debug=True)


if __name__ == '__main__':
    start_api()
