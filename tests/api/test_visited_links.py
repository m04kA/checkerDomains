from unittest.mock import patch

import pytest

from rest_framework.test import APIClient

from checkerApp.utils import linksParser
from checkerApp.tasks import add_data_in_database

client = APIClient()


@pytest.mark.django_db
@patch.object(add_data_in_database, 'delay')
def test_green_flow(mock_delay):
    links_data = {
        "links": [
            "https://ti.ru/",
            "https://tu.ru/search/?text=мемы+с+котиками",
            "https://papa.ru",
            "https://mama.com/questions/65724760/how-it-is"
        ]
    }

    response = client.post('/visited_links', links_data, format='json', HTTP_X_USER_ID='1')

    assert {'status': 'Ok'} == response.data
    assert response.status_code == 200


def test_has_not_access():
    links_data = {
        "links": [
            "https://ti.ru/",
            "https://tu.ru/search/?text=мемы+с+котиками",
            "https://papa.ru",
            "https://mama.com/questions/65724760/how-it-is"
        ]
    }

    response = client.post('/visited_links', links_data, format='json')

    assert response.status_code == 403


def test_wrong_body():
    links_data = {
        "linkases": [
            "https://ti.ru/",
            "https://tu.ru/search/?text=мемы+с+котиками",
            "https://papa.ru",
            "https://mama.com/questions/65724760/how-it-is"
        ]
    }

    response = client.post('/visited_links', links_data, format='json', HTTP_X_USER_ID='1')

    assert response.status_code == 400


def test_unit_get_domains_from_links():
    expected_domains = {"ya.ru", "sber.ru", "stackoverflow.com"}
    links = [
        "https://ya.ru/",
        "https://ya.ru/search/?text=мемы+с+котиками",
        "https://sber.ru",
        "https://stackoverflow.com/questions/65724760/how-it-is"
        "ha-ha-ha"
    ]
    domains = linksParser.get_unique_domains_from_links(links)
    assert set(domains) == expected_domains
