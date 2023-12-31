from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from .models import *
from .views import *

class RecommenderTests(TestCase):

    def test_recommender_form(self):
        response = self.client.get('/workout_recommender/', secure=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Workout Recommender")

    def test_selector_form(self):
        self.factory = RequestFactory()
        request = self.factory.post('/workout_recommender/', secure=True)
        request.user = User.objects.create()
        response = selector_form(request)
        self.assertEqual(response.status_code, 200)
