from django.shortcuts import render
from . import api_interactions
from .forms import SelectorForm
# Create your views here.

def selector_form(request):
    context={}
    context['form'] = SelectorForm(request.POST)
    if context['form'].is_valid():
        num_workouts = context['form'].cleaned_data['num_workouts']
        selection = context['form'].cleaned_data['selection']

        relevent_workouts = api_interactions.get_select_workouts(num_workouts, selection)
        return render(request, 'workout_recommender/workouts.html', 
        {"workouts": relevent_workouts})

    return render(request, 'workout_recommender/selector_form.html', context)
    """
        

        return render(request, 'workout_recommender/workouts.html',
            {"workouts": 
                api_interactions.get_select_workouts(num_workouts, selection)})
    """

def all_workouts(request):
    return render(request, 'workout_recommender/workouts.html', 
        {"workouts": api_interactions.get_all_workouts(500)})