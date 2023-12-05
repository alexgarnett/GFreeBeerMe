from src.app.main import app
import pytest


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_main_route(client):
    response = client.get('/')
    assert response.status_code == 200
    assert 'text/html' in response.content_type


def test_about_page_route(client):
    response = client.get('/about')
    assert response.status_code == 200
    assert 'text/html' in response.content_type


def test_contribute_page(client):
    response = client.get('/contribute')
    assert response.status_code == 200
    assert 'text/html' in response.content_type


# Functions that rely on API calls won't be testable until the app is structured
# in a way that the app and API can be started simultaneously from the command
# line, like in a shell script or by using make
# def test_submit_contribution(client):
#     response = client.post('/contribute/submit', data={
#             # Provide form data here
#         })
#         assert response.status_code == 201
#
#
# def test_all_beers_page(client):
#     pass
#
#
# def test_beer_info_page(client):
#     pass
