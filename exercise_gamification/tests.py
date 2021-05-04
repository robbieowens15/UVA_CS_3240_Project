from django.test import TestCase
from django.contrib.auth.models import User
from .models import Profile, Workout, Cardio_Workout, Strength_Workout, Other_Workout

class ExerciseTestCase(TestCase):

    def setUp(self):
        User.objects.create()
        u = User.objects.get()
        Profile.objects.create(user=u, name='John', username='johnstudent', bio="I am a student", level=0, xp=0)

    
    def test_profile_creation(self):
        john = Profile.objects.get(name='John')
        self.assertEqual(john.username, 'johnstudent')
        self.assertEqual(john.bio, 'I am a student')


    
