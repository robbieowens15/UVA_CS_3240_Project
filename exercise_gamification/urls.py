from django.urls import path

from . import views

app_name = 'exercise_gamification'
urlpatterns = [
    path('workouts/', views.display_workouts, name='workouts'),
    path('workouts/choose_workout/', views.choose_workout_type, name='choose_workout'),
    path('workouts/redirect_workout/', views.redirect_workout, name='redirect_workout'),
    path('workouts/cardio_workout/', views.load_cardio_subimssion, name='cardio_workout'),
    path('workouts/submit_cardio/', views.submit_cardio_workout, name='submit_cardio'),
    path('workouts/strength_workout/', views.load_strength_submission, name='strength_workout'),
    path('workouts/submit_strength/', views.submit_strength_workout, name='submit_strength'),
    path('workouts/other_workout/', views.load_other_submission, name='other_workout'),
    path('workouts/submit_other/', views.submit_other_workout, name='submit_other'),
]
