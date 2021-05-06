from exercise_gamification.models import FriendRequest

def add_variables(request):
    if (request.user.is_authenticated):
        incoming_fr = FriendRequest.objects.filter(to_user=request.user)
        outgoing_fr = FriendRequest.objects.filter(from_user=request.user)
        num_fr = FriendRequest.objects.filter(to_user=request.user).count()
        return {
            'incoming_fr': incoming_fr,
            'outgoing_fr': outgoing_fr,
            'num_fr': num_fr
        }
    return {}