from django.shortcuts import render
from . import api_interactions
# Create your views here.


def all_workouts(request):
    return render(request, 'workout_recommender/allworkouts.html', 
        {"workouts": api_interactions.get_all_workouts(500)})