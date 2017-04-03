"""Application views."""

import django.views.generic
from football.models import *
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from django.db.models import Max

class IndexView(django.views.generic.TemplateView):
    """Render 'index.html' template."""

    template_name = 'index.html'
    def get(self, request, *args, **kwargs):
        context = {'tournaments' : Tournament.objects.all(),
                   'matches': Match.objects.filter(status='ended').order_by('-tour')}
        return render(request, self.template_name, context)


class LeageView(django.views.generic.TemplateView):
    """Render 'about.html' template."""

    template_name = 'leages.html'
    def get(self, request, *args, **kwargs):
        context=''
        return render(request,self.template_name,context)


class TournamentView(django.views.generic.TemplateView):
    """Render 'about.html' template."""

    template_name_leage = 'leage.html'
    template_name_cup = 'cup.html'
    def get(self, request, tournament_id):
        context = {'tournament': Tournament.objects.filter(id=tournament_id)}
        if context['tournament'][0].tournament_type == 'leage':
            return render(request,self.template_name_leage,context)
        else:
            return render(request, self.template_name_cup, context)


class CupsView(django.views.generic.TemplateView):
    """Render 'about.html' template."""

    template_name = 'cups.html'
    def get(self, request, *args, **kwargs):
        context=''
        return render(request,self.template_name,context)


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
        context = {'team' : Team.objects.filter(id=team_id)}
        return render(request, self.template_name, context)

class NewsView(django.views.generic.TemplateView):
    """Render 'about.html' template."""

    template_name = 'news.html'
    def get(self, request, *args, **kwargs):
        context=''
        return render(request,self.template_name,context)