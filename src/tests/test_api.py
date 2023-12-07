import os
from src.api.beer_api import *
import pytest
import requests


# @pytest.fixture
# def client():
#     with api.test_client() as client:
#         yield client

url_prefix = 'http://localhost:8080'


def test_api_main_route():
    response = requests.get(url_prefix + '/api')
    assert response.status_code == 200


def test_api_beer_info():
    beer_id = '1'
    response = requests.get(url_prefix + '/api/beers/' + beer_id)
    data = response.json()
    assert response.status_code == 200
    assert data['id'] == 1


def test_api_all_beers():
    response = requests.get(url_prefix + '/api/beers')
    data = response.json()
    assert response.status_code == 200
    assert data[0]['id'] == 1


# def test_api_contribute(client):
#     pass
