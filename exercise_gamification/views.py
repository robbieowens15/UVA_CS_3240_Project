from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils import timezone
from django.contrib import messages

from .models import Profile, Workout, Cardio_Workout, Strength_Workout, Other_Workout

import logging

# Create your views here.

def show_profile(request):
    if (request.user.is_authenticated):
        if (Profile.objects.filter(user=request.user).count() == 0):
            full_name = request.user.first_name + ' ' + request.user.last_name
            Profile.objects.create(user=request.user, name=full_name, username=request.user.username, email=request.user.email, bio='', level=0, xp=0)
        progress_width = "width: "+ str(int((request.user.profile.xp - request.user.profile.level*10000)/100)) +"%"
        return render(request, 'exercise_gamification/profile.html', {'profile': request.user.profile, 'friends': request.user.profile.friends.all(), 'workouts': request.user.profile.workouts.all(), 'width': progress_width})
    return HttpResponseRedirect('/accounts/login')

def show_other_user_profile(request, username):
    if (request.user.is_authenticated):
        if (username == request.user.profile.username):
            return HttpResponseRedirect(reverse('exercise_gamification:profile'))
    profile = get_object_or_404(Profile, username=username)
    if (request.user.profile.friends.filter(username=username).count() > 0):
        friends = 'yes'
    else:
        friends = 'no'
    return render(request, 'exercise_gamification/profile.html', {'profile': profile, 'is_friend': friends})

def show_friends(request):
    if (request.user.is_authenticated):
        friends = request.user.profile.friends.all()
        return render(request, 'exercise_gamification/friends.html', {'friends': friends})
    return HttpResponseRedirect('/accounts/login')

def profile_editor(request):
    if (request.user.is_authenticated):
        return render(request, 'exercise_gamification/edit_profile.html', {'user_exists': False})
    return HttpResponseRedirect('/accounts/login')

def save_profile(request):
    if (request.user.is_authenticated):
        user_full_name = request.POST['name']
        profile_user = request.POST['username']
        user_email = request.POST['email']
        user_bio = request.POST['bio']

        request.user.username = profile_user
        request.user.save()
        if (Profile.objects.filter(user=request.user).count() == 0):
            Profile.objects.create(user=request.user, name=user_full_name, username=profile_user, email=user_email, bio=user_bio, level=0, xp=0)
        else:
            p = Profile.objects.get(user=request.user)
            Profile.objects.filter(user=request.user).update(name=user_full_name, username=profile_user, email=user_email, bio=user_bio)
        return HttpResponseRedirect(reverse('exercise_gamification:profile'))
    return HttpResponseRedirect('/accounts/login')

def add_friend(request, username):
    if (request.user.is_authenticated):
        profile = get_object_or_404(Profile, username=username)
        request.user.profile.friends.add(profile)
        return HttpResponseRedirect(reverse('exercise_gamification:user_profile', args=(username,)))
    return HttpResponseRedirect('/accounts/login')

def remove_friend(request, username):
    if (request.user.is_authenticated):
        profile = get_object_or_404(Profile, username=username)
        request.user.profile.friends.remove(profile)
        return show_profile(request)
    return HttpResponseRedirect('/accounts/login')

def display_workouts(request):
    if (request.user.is_authenticated):
        if (Profile.objects.filter(user=request.user).count() == 0):
            full_name = request.user.first_name + ' ' + request.user.last_name
            p = Profile.objects.create(user=request.user, name=full_name, username=request.user.username, email=request.user.email, bio='', level=0, xp=0)
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
        calories = 0 # Dummy value for now
        workout_notes = request.POST['notes']

        cardio_duration = request.POST['duration']
        cardio_distance = request.POST['distance']

        w = Workout(base_profile=p, date=timezone.now(), name=workout_name, estimated_calories=calories, notes=workout_notes)
        w.save()
        c = Cardio_Workout(workout=w, duration=cardio_duration, distance=cardio_distance)
        c.save()
        
        p.workouts.add(w)
        old_xp = p.xp
        p.xp = int(p.xp + 1000 + float(cardio_duration)*10 + float(cardio_distance)*100)
        old_level = p.level
        p.level = p.xp // 10000
        p.save()
        messages.success(request, "Nice work, " + p.name+". " + str(p.xp-old_xp) + " xp earned!")

        if p.level > old_level:
            messages.success(request, "Amazing " + p.name +", you're now a level " + str(p.level) +"! Keep up the great work!")

        return HttpResponseRedirect(reverse('exercise_gamification:workouts'))
    return HttpResponseRedirect('/accounts/login')

def submit_strength_workout(request):
    if (request.user.is_authenticated):
        p = Profile.objects.get(user=request.user)

        workout_name = request.POST['workout_name']
        calories = 0 # Dummy value for now
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

        old_xp = p.xp
        p.xp = int(p.xp + 1000 + float(strength_repitions)*100)
        old_level = p.level
        p.level = p.xp // 10000
        p.save()
        messages.success(request, "Nice work, " + p.name+". " + str(p.xp-old_xp) + " xp earned!")
        if p.level > old_level:
            messages.success(request, "Amazing " + p.name +", you're now a level " + str(p.level) +"! Keep up the great work!")

        return HttpResponseRedirect(reverse('exercise_gamification:workouts'))
    return HttpResponseRedirect('/accounts/login')

def submit_other_workout(request):
    if (request.user.is_authenticated):
        p = Profile.objects.get(user=request.user)

        workout_name = request.POST['workout_name']
        calories = 0 # Dummy value for now
        workout_notes = request.POST['notes']

        workout_description = request.POST['description']

        w = Workout(base_profile=p, date=timezone.now(), name=workout_name, estimated_calories=calories, notes=workout_notes)
        w.save()

        o = Other_Workout(workout=w, description=workout_description)
        o.save()

        p.workouts.add(w)

        p.xp = p.xp + 1000
        old_level = p.level
        p.level = p.xp // 10000
        p.save()
        messages.success(request, "Nice work, " + p.name+". " + str(1000) + " xp earned!")

        if p.level > old_level:
            messages.success(request, "Amazing " + p.name +", you're now a level " + str(p.level) +"! Keep up the great work!")

        return HttpResponseRedirect(reverse('exercise_gamification:workouts'))
    return HttpResponseRedirect('/accounts/login')
