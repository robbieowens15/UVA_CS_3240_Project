from django.shortcuts import render

from exercise_gamification.models import Profile

"""
Title: Get the index of an element in a queryset
Source: https://stackoverflow.com/questions/1042596/get-the-index-of-an-element-in-a-queryset
"""
def index(request):
    top_users = Profile.objects.order_by('-xp')
    if (request.user.is_authenticated):
        # Create new profile if the profile doesn't exist
        if (Profile.objects.filter(user=request.user).count() == 0):
            full_name = request.user.first_name + ' ' + request.user.last_name
            p = Profile.objects.create(user=request.user, name=full_name, username=request.user.username, email=request.user.email, bio='', level=0, xp=0)
        else:
            p = Profile.objects.get(user=request.user)
        # Finds the user's rank out of all users
        for index, item in enumerate(top_users): # Loop through elements in top_users query set
            if (item == p): # If the logged-in user profile is found, break and the index + 1 is the user's rank
                break
        return render(request, 'exercise_gamification/index.html', {'profile': p, 'top_users': top_users[:20], 'rank': index + 1})
    return render(request, 'exercise_gamification/index.html', {'top_users': top_users[:20]})
