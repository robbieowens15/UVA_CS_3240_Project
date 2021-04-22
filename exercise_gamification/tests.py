from django.test import TestCase


class DummyTestCase(TestCase):
    
    def test_dummy(self):
        s = 'hello world'
        self.assertEqual(s, 'hello world')

