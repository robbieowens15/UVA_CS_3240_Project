from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone

from .models import Profile, Workout, Cardio_Workout, Strength_Workout, Other_Workout

import logging

# Create your views here.

def display_workouts(request):
    if (request.user.is_authenticated):
        if (Profile.objects.filter(user=request.user).count() == 0):
            p = Profile(user=request.user, username=request.user.username, email="", level=0, xp=0)
            p.save()
        else:
            p = Profile.objects.get(user=request.user)
        workouts = p.workouts.all()
        return render(request, 'exercise_gamification/workouts.html', {'workouts': workouts})
    return HttpResponseRedirect('/accounts/login')


def choose_workout_type(request):
    if (request.user.is_authenticated):
        return render(request, 'exercise_gamification/choose_workout.html')
    return HttpResponseRedirect('/accounts/login')

def load_cardio_subimssion(request):
    if (request.user.is_authenticated):
        return render(request, 'exercise_gamification/cardio_form.html')
    return HttpResponseRedirect('/accounts/login')

def load_strength_submission(request):
    if (request.user.is_authenticated):
        return render(request, 'exercise_gamification/strength_form.html')
    return HttpResponseRedirect('/accounts/login')

def load_other_submission(request):
    if (request.user.is_authenticated):
        return render(request, 'exercise_gamification/other_workout_form.html')
    return HttpResponseRedirect('/accounts/login')

def redirect_workout(request):
    if (request.user.is_authenticated):
        workout_type = request.POST.getlist('workout_type')
        if ('cardio' in workout_type):
            return HttpResponseRedirect(reverse('exercise_gamification:cardio_workout'))
        elif ('strength' in workout_type):
            return HttpResponseRedirect(reverse('exercise_gamification:strength_workout'))
        elif ('other' in workout_type):
            return HttpResponseRedirect(reverse('exercise_gamification:other_workout'))
        return HttpResponseRedirect(reverse('exercise_gamification:choose_workout'))
    return HttpResponseRedirect('/accounts/login')

def submit_cardio_workout(request):
    if (request.user.is_authenticated):
        p = Profile.objects.get(user=request.user)

        workout_name = request.POST['workout_name']
        calories = 300 # Dummy value for now
        workout_notes = request.POST['notes']

        cardio_duration = request.POST['duration']
        cardio_distance = request.POST['distance']

        w = Workout(base_profile=p, date=timezone.now(), name=workout_name, estimated_calories=calories, notes=workout_notes)
        w.save()
        c = Cardio_Workout(workout=w, duration=cardio_duration, distance=cardio_distance)
        c.save()

        p.workouts.add(w)

        return HttpResponseRedirect(reverse('exercise_gamification:workouts'))
    return HttpResponseRedirect('/accounts/login')

def submit_strength_workout(request):
    if (request.user.is_authenticated):
        p = Profile.objects.get(user=request.user)

        workout_name = request.POST['workout_name']
        calories = 300 # Dummy value for now
        workout_notes = request.POST['notes']

        strength_bodyweight = request.POST.getlist('bodyweight')
        strength_repitions = request.POST['repetitions']
        strength_weight = request.POST['weight']

        is_bodyweight = False

        if ('on' in strength_bodyweight):
            strength_weight = 0
            is_bodyweight = True

        w = Workout(base_profile=p, date=timezone.now(), name=workout_name, estimated_calories=calories, notes=workout_notes)
        w.save()

        s = Strength_Workout(workout=w, bodyweight=is_bodyweight, repetitions=strength_repitions, weight=strength_weight)
        s.save()

        p.workouts.add(w)

        return HttpResponseRedirect(reverse('exercise_gamification:workouts'))
    return HttpResponseRedirect('/accounts/login')

def submit_other_workout(request):
    if (request.user.is_authenticated):
        p = Profile.objects.get(user=request.user)

        workout_name = request.POST['workout_name']
        calories = 300 # Dummy value for now
        workout_notes = request.POST['notes']

        workout_description = request.POST['description']

        w = Workout(base_profile=p, date=timezone.now(), name=workout_name, estimated_calories=calories, notes=workout_notes)
        w.save()

        o = Other_Workout(workout=w, description=workout_description)
        o.save()

        p.workouts.add(w)

        return HttpResponseRedirect(reverse('exercise_gamification:workouts'))
    return HttpResponseRedirect('/accounts/login')
