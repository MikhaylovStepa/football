from django import forms

class TeamForm(forms.Form):
    team_name = forms.CharField(max_length=30)
    coach = forms.CharField(max_length=30)