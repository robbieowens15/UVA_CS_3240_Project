from django.shortcuts import render

from exercise_gamification.models import Profile

def index(request):
    top_users = Profile.objects.order_by('-xp')
    if (request.user.is_authenticated):
        if (Profile.objects.filter(user=request.user).count() == 0):
            full_name = request.user.first_name + ' ' + request.user.last_name
            p = Profile.objects.create(user=request.user, name=full_name, username=request.user.username, email=request.user.email, bio='', level=0, xp=0)
        else:
            p = Profile.objects.get(user=request.user)
        for index, item in enumerate(top_users):
            if (item == p):
                break
        return render(request, 'exercise_gamification/index.html', {'profile': p, 'top_users': top_users[:20], 'rank': index + 1})
    return render(request, 'exercise_gamification/index.html', {'top_users': top_users[:20]})
