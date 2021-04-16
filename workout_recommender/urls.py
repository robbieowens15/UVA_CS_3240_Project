from django.urls import path

from . import views

app_name = 'workout_recommender'
urlpatterns = [
    path('workouts/', views.all_workouts, name='workouts'),
]
