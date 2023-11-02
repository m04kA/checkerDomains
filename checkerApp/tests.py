from django.urls import reverse
from rest_framework.test import APITestCase

from checkerApp.src import linksParser

from checkerApp.models import UserDomainsHistory


class HistoryDomainsTests(APITestCase):
    def setUp(self):
        history_test_1 = UserDomainsHistory.objects.create(user_id='1', domain='ya.ru', created_at=123)
        history_test_2 = UserDomainsHistory.objects.create(user_id='1', domain='ya.ru', created_at=124)
        history_test_3 = UserDomainsHistory.objects.create(user_id='1', domain='test.ru', created_at=124)

    def test_green_flow(self):
        response = self.client.get(reverse('get_domains'), {'start': 122, 'finish': 125}, HTTP_X_USER_ID='1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['domains']), 2)

    def test_not_access(self):
        response = self.client.get(reverse('get_domains'), {'start': 122, 'finish': 125})
        self.assertEqual(response.status_code, 403)

    def test_green_filter(self):
        response = self.client.get(reverse('get_domains'), {'start': 122, 'finish': 124}, HTTP_X_USER_ID='1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['domains']), 1)

    def test_null_result(self):
        response = self.client.get(reverse('get_domains'), {'start': 125, 'finish': 128}, HTTP_X_USER_ID='1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['domains']), 0)

    def test_unit_get_domains(self):
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

