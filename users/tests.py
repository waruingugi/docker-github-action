from django.test import TestCase

# Create your tests here.
class DummyTestCase(TestCase):
    def test_value_is_same(self):
        self.assertEqual(1, 2)
