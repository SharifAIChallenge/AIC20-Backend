from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class Tests(APITestCase):
    def test_homepage(self):
        url = reverse('homepage:get_homepage')
        data = {}
        response = self.client.get(url, data, format='json')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
