from django.test import TestCase

class DummyTestCase(TestCase):
    def dummy_test(self):
        self.assertEqual(0, 0)

