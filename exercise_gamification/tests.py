from django.test import TestCase


class DummyTestCase(TestCase):
    
    def dummy_test(self):
        self.assertTrue(1 == 1)
