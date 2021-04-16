from django.urls import path

from . import views

app_name = 'workout_recommender'
urlpatterns = [
    path('', views.selector_form, name='selector_form'),
    path('workouts/', views.all_workouts, name='workouts')
]
