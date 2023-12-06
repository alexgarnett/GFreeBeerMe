import os
from src.api.beer_api import *
import pytest


@pytest.fixture
def client():
    with api.test_client() as client:
        yield client


def test_api_main_route(client):
    response = client.get('/api')
    assert response.status_code == 308
    assert 'text/html' in response.content_type


def test_api_beer_info(client):
    beer_id = '1'
    response = client.get('/api/beers/' + beer_id)
    data = response.json
    assert response.status_code == 200
    assert data['id'] == 1


def test_api_all_beers(client):
    response = client.get('/api/beers')
    data = response.json
    assert response.status_code == 200
    assert data[0]['id'] == 1


# def test_api_contribute(client):
#     pass
