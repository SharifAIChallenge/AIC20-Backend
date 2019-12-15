from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from homepage.models import Homepage


class Tests(APITestCase):
    def create_homepage(self):
        homepage = Homepage.objects.create(title_en='AI', id=1, title_fa='نبرد هوش مصنوعی')
        homepage.save()

    def test_homepage(self):
        self.create_homepage()
        url = reverse('homepage:get_homepage')
        data = {}
        response = self.client.get(url, data, format='json')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
