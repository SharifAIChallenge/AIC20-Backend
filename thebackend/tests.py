from django.test import TestCase


class AnimalTestCase(TestCase):
    def test(self):
        self.assertEqual(1, 2, 'hoora we faild')
