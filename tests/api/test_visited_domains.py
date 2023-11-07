import pytest

from checkerApp.models import UserDomainsHistory
from rest_framework.test import APIClient

client = APIClient()


@pytest.mark.django_db
@pytest.mark.parametrize(
    ('start', 'finish', 'expected_domains',),
    [
        pytest.param(
            122,
            125,
            {
                'ya.ru',
                'test.ru'
            },
            id='get-all-domains'
        ),
        pytest.param(
            122,
            124,
            {
                'ya.ru'
            },
            id='get-one-domain'
        ),
        pytest.param(
            125,
            128,
            set(),
            id='get-no-one-domain'
        ),
    ]
)
def test_green_flow(
        start: int,
        finish: int,
        expected_domains: set
):
    history_test_1 = UserDomainsHistory.objects.create(user_id='1', domain='ya.ru', created_at=123)
    history_test_2 = UserDomainsHistory.objects.create(user_id='1', domain='ya.ru', created_at=124)
    history_test_3 = UserDomainsHistory.objects.create(user_id='1', domain='test.ru', created_at=124)

    response = client.get('/visited_domains', {'start': start, 'finish': finish}, HTTP_X_USER_ID='1')

    assert response.status_code == 200
    assert set(response.data['domains']) == expected_domains


def test_has_not_access():
    response = client.get('/visited_domains', {'start': 1, 'finish': 2})

    assert response.status_code == 403

@pytest.mark.parametrize(
    ('start', 'finish'),
    [
        pytest.param(
            'h',
            10,
            id='wrong-start'
        ),
        pytest.param(
            1,
            'h',
            id='wrong-finish'
        ),
        pytest.param(
            'b',
            'h',
            id='wrong-all-query-params'
        ),
        pytest.param(
            None,
            'h',
            id='without-start'
        ),
        pytest.param(
            'h',
            None,
            id='without-finish'
        ),
        pytest.param(
            None,
            None,
            id='without-all-query-params'
        ),

    ]

)
def test_wrong_query_params(
        start,
        finish
):
    params = {}
    if start:
        params['start'] = start
    if finish:
        params['finish'] = finish
    response = client.get('/visited_domains', params, HTTP_X_USER_ID='1')

    assert response.status_code == 400