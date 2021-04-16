from django.shortcuts import render
from . import api_interactions
from .forms import SelectorForm
# Create your views here.

def selector_form(request):
    context={}
    context['form'] = SelectorForm(request.POST)
    return render(request, 'workout_recommender/selector_form.html', context)
    """
        if context['form'].is_valid():
        num_workouts = form.cleaned_data.get('num_workouts')
        selection = form.cleaned_data.get('selection')

        return render(request, 'workout_recommender/workouts.html',
            {"workouts": 
                api_interactions.get_select_workouts(num_workouts, selection)})
    """

def all_workouts(request):
    return render(request, 'workout_recommender/workouts.html', 
        {"workouts": api_interactions.get_all_workouts(500)})