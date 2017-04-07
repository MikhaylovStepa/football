"""Application views."""

import django.views.generic
from football.models import *
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from forms import TeamForm, TournamentForm

class IndexView(django.views.generic.TemplateView):
    """Render 'index.html' template."""

    template_name = 'index.html'
    def get(self, request, *args, **kwargs):
        context = {'tournaments' : Tournament.objects.all(),
                   'last_matches': Match.objects.get_last_matches_in_tournament()}
        return render(request, self.template_name, context)


class LeageView(django.views.generic.TemplateView):
    """Render 'about.html' template."""

    template_name = 'leages.html'
    context = {'leages': Tournament.objects.filter(tournament_type='leage'),
               'teams_points':Team.objects.get_team_matches_and_points_in_the_leage(),
               'last_matches': Match.objects.get_last_matches_in_tournament()}
    def get(self,request):
        return render(request,self.template_name,self.context)


class TournamentView(django.views.generic.TemplateView):
    """Render 'about.html' template."""

    template_name_leage = 'leage.html'
    template_name_cup = 'cup.html'
    def get(self, request, tournament_id):
        context = {'tournament': Tournament.objects.filter(id=tournament_id),
                   'teams_points': Team.objects.get_team_matches_and_points_in_the_leage(),
                   'matches': Match.objects.all(),
                   'tour_number': Match.objects.get_tour_number_in_tournament()
                   }
        if context['tournament'][0].tournament_type == 'leage':
            return render(request,self.template_name_leage,context)
        else:
            return render(request, self.template_name_cup, context)


class CupsView(django.views.generic.TemplateView):
    """Render 'about.html' template."""

    template_name = 'cups.html'
    context = {'leages': Tournament.objects.filter(tournament_type='cup'),
               'last_matches': Match.objects.get_last_matches_in_tournament()}
    def get(self, request):
        return render(request, self.template_name, self.context)




class MatchView(django.views.generic.TemplateView):
    """Render 'about.html' template."""

    template_name = 'match.html'

    def get(self, request, match_id):
        context = {'match': Match.objects.filter(id=match_id)}
        return render(request, self.template_name, context)

class PlayerView(django.views.generic.TemplateView):
    """Render 'index.html' template."""

    template_name = 'player.html'
    def get(self, request, player_id):
        context = {'player' : Player.objects.filter(id=player_id)}
        return render(request, self.template_name, context)


class TeamView(django.views.generic.TemplateView):
    """Render 'index.html' template."""

    template_name = 'team.html'
    def get(self, request, team_id):
        context = {'team' : Team.objects.filter(id=team_id),
                   'players' : Player.objects.filter(team_id=team_id)}
        return render(request, self.template_name, context)

class TeamsView(django.views.generic.TemplateView):
    """Render 'about.html' template."""

    template_name = 'teams.html'
    form_class = TeamForm

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name,
                      {'teams': Team.objects.all()})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        Team(name=form['team_name'].value(), coach=form['coach'].value()).save()
        return render(request, self.template_name, {'teams':Team.objects.all()})


class NewsView(django.views.generic.TemplateView):
    """Render 'about.html' template."""

    template_name = 'news.html'
    def get(self, request, *args, **kwargs):
        context=''
        return render(request,self.template_name,context)


class TournamentListView(django.views.generic.TemplateView):
    """Render 'about.html' template."""

    template_name = 'tournament_list.html'
    form_class = TournamentForm
    def get(self, request, *args, **kwargs):
        context = {'tournaments' : Tournament.objects.all()}
        return render(request,self.template_name,context)

    def post(self,request, *args, **kwargs):

        form=self.request.POST
        #import pdb
        #pdb.set_trace()
        #return form
        #'schedule': Match.objects.generate_schedule(form['tournament_id']),
        context = {'schedule': Match.objects.generate_schedule(form['tournament_id']),
                   'matches':Match.objects.filter(tournament_id = form['tournament_id'])}
        return render(request, 'tournament_schedule.html', context)