from django import forms

class TeamForm(forms.Form):
    team_name = forms.CharField(max_length=30)
    coach = forms.CharField(max_length=30)

class TournamentForm(forms.Form):
    tournament_id = forms.HiddenInput

class CreateTournamentForm(forms.Form):
    status = forms.Field()
    name = forms.CharField(
        max_length=30
    )
    loops = forms.IntegerField()
    tournament_type = forms.ChoiceField()

class TourTeamForm(forms.Form):
    tournament_id = forms.IntegerField()
    team_id = forms.IntegerField()

class CreateTeamForm(forms.Form):
    tournament_id = forms.HiddenInput()
    name = forms.CharField(
        max_length=30
    )
    coach = forms.CharField(
        max_length=30
    )
