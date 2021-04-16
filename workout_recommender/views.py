from django.shortcuts import render

# Create your views here.


def all_workouts(request):
    return render(request, 'workout_recommender/index.html')