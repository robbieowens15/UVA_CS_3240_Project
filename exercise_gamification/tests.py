from django.test import RequestFactory, TestCase
from django.contrib.auth.models import User, AnonymousUser
from django.urls import reverse
from django.contrib import messages
from django.contrib.messages.middleware import MessageMiddleware
from django.contrib.sessions.middleware import SessionMiddleware
from .models import *
from .views import *

class HomeTests(TestCase):

    def test_home_page(self):
        response = self.client.get('', secure=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Welcome")

    def test_login_page(self):
        response = self.client.get('/accounts/login/', secure=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sign In")
        self.assertContains(response, "Google")

class WorkoutTests(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

    def test_workout_redirect(self):
        request = self.factory.get('/exercise_gamification/workouts/', secure=True)
        request.user = AnonymousUser()
        response = display_workouts(request)
        self.assertEqual(response.status_code, 302)
        request.user = User.objects.create()
        response = display_workouts(request)
        self.assertEqual(response.status_code, 200)

    def test_load_cardio(self):
        request = self.factory.get('/exercise_gamification/workouts/cardio_workout/', secure=True)
        request.user = User.objects.create()
        response = load_cardio_subimssion(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Submit Cardio Workout")

    def test_load_strength(self):
        request = self.factory.get('/exercise_gamification/workouts/strength_workout/', secure=True)
        request.user = User.objects.create()
        response = load_strength_submission(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Submit Strength Workout")

    def test_load_other(self):
        request = self.factory.get('/exercise_gamification/workouts/other_workout/', secure=True)
        request.user = User.objects.create()
        response = load_other_submission(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Submit Other Workout")

    def test_submit_cardio(self):
        request = self.factory.post('/exercise_gamification/workouts/cardio_workout/', secure=True, data={'workout_name':'running', 'duration':30, 'distance':1000, 'notes':'hard'})
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        middleware = MessageMiddleware()
        middleware.process_request(request)
        request.session.save()
        request.user = User.objects.create()
        request.user.profile = Profile.objects.create(user=request.user, name='John', username='johnstudent', bio="I am a student", level=0, xp=0)
        self.assertEqual(request.user.profile.workouts.exists(), False)
        self.assertEqual(request.user.profile.xp, 0)
        response = submit_cardio_workout(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(request.user.profile.workouts.exists(), True)
        request = self.factory.get('/exercise_gamification/workouts/', secure=True)
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        middleware = MessageMiddleware()
        middleware.process_request(request)
        request.session.save()
        request.user = User.objects.get()
        response = display_workouts(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "running")
        self.assertTrue(request.user.profile.xp > 0)

    def test_submit_strength(self):
        request = self.factory.post('/exercise_gamification/workouts/strength_workout/', secure=True, data={'workout_name':'bicep curls', 'bodyweight':'False', 'repetitions':12, 'weight':25, 'notes':''})
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        middleware = MessageMiddleware()
        middleware.process_request(request)
        request.session.save()
        request.user = User.objects.create()
        request.user.profile = Profile.objects.create(user=request.user, name='John', username='johnstudent', bio="I am a student", level=0, xp=0)
        self.assertEqual(request.user.profile.workouts.exists(), False)
        self.assertEqual(request.user.profile.xp, 0)
        response = submit_strength_workout(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(request.user.profile.workouts.exists(), True)
        request = self.factory.get('/exercise_gamification/workouts/', secure=True)
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        middleware = MessageMiddleware()
        middleware.process_request(request)
        request.session.save()
        request.user = User.objects.get()
        response = display_workouts(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "bicep curls")
        self.assertTrue(request.user.profile.xp > 0)

    def test_submit_other(self):
        request = self.factory.post('/exercise_gamification/workouts/other_workout/', secure=True, data={'workout_name':'basketball', 'description':'half court game', 'notes':'fun'})
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        middleware = MessageMiddleware()
        middleware.process_request(request)
        request.session.save()
        request.user = User.objects.create()
        request.user.profile = Profile.objects.create(user=request.user, name='John', username='johnstudent', bio="I am a student", level=0, xp=0)
        self.assertEqual(request.user.profile.workouts.exists(), False)
        self.assertEqual(request.user.profile.xp, 0)
        response = submit_other_workout(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(request.user.profile.workouts.exists(), True)
        request = self.factory.get('/exercise_gamification/workouts/', secure=True)
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        middleware = MessageMiddleware()
        middleware.process_request(request)
        request.session.save()
        request.user = User.objects.get()
        response = display_workouts(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "basketball")
        self.assertTrue(request.user.profile.xp > 0)

class ProfileTests(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

    def test_profile_creation(self):
        User.objects.create()
        u = User.objects.get()
        Profile.objects.create(user=u, name='John', username='johnstudent', bio="I am a student", level=0, xp=0)
        john = Profile.objects.get(name='John')
        self.assertEqual(john.username, 'johnstudent')
        self.assertEqual(john.bio, 'I am a student')

    def test_profile_redirect(self):
        request = self.factory.get('/exercise_gamification/profile/', secure=True)
        request.user = AnonymousUser()
        response = show_profile(request)
        self.assertEqual(response.status_code, 302)
        request.user = User.objects.create()
        response = show_profile(request)
        self.assertEqual(response.status_code, 200)

    def test_save_profile(self):
        request = self.factory.post('/exercise_gamification/profile/save_profile/', secure=True, data={'name':'Joe', 'username':'joetheman', 'email':'joe@gmail.com', 'bio':'I am Joe'})
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        middleware = MessageMiddleware()
        middleware.process_request(request)
        request.session.save()
        request.user = User.objects.create()
        request.user.profile = Profile.objects.create(user=request.user, name='', username='', bio='', level=0, xp=0)
        self.assertEqual(request.user.profile.name, "")
        response = save_profile(request)
        self.assertEqual(response.status_code, 302)
        request = self.factory.get('/exercise_gamification/profile/', secure=True)
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        middleware = MessageMiddleware()
        middleware.process_request(request)
        request.session.save()
        request.user = User.objects.get()
        response = show_profile(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(request.user.profile.name, "Joe")
        self.assertContains(response, "I am Joe")
