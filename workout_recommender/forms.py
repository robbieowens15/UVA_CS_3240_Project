from django import forms
from . import api_interactions

class SelectorForm(forms.Form):
    muscle_groups = [('Any/All', 'Any/All')]
    muscle_groups_dict = api_interactions.get_all_muscle_groups()
    for group in muscle_groups_dict:
        muscle_groups.append((group["name"], group["name"]))
    #fields
    num_workouts = forms.IntegerField()
    selection = forms.CharField(label='Muscle Group', max_length=100,
        widget=forms.Select(choices=muscle_groups))