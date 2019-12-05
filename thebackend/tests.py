from django.test import TestCase

# Remove this and add your test case here.
# For learn how to add test case, visit:
# https://docs.djangoproject.com/en/2.2/topics/testing/overview/


class AnimalTestCase(TestCase):
    def test(self):
        self.assertEqual(1, 1, 'hoora we did not failed')
