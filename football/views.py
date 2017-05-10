"""Application views."""

import django.views.generic
from football.models import *
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from forms import TeamForm, TournamentForm, CreateTournamentForm
import django.urls as urls

class IndexView(django.views.generic.TemplateView):
    """Render 'index.html' template."""

    #show information about last played tour in all tournaments
    template_name = 'index.html'
    def get(self, request, *args, **kwargs):
        context = {'tournaments' : Tournament.objects.all(),
                   'last_matches': Match.objects.get_last_matches_in_tournament()}
        return render(request, self.template_name, context)


class LeageView(django.views.generic.TemplateView):
    """Render 'leages.html' template."""

    #show info about leages: not full touranment table and last played tour
    template_name = 'leages.html'
    context = {'leages': Tournament.objects.filter(tournament_type='leage'),
               'teams_points':Team.objects.get_team_matches_and_points_in_the_leage(),
               'last_matches': Match.objects.get_last_matches_in_tournament()}
    def get(self,request):
        return render(request,self.template_name,self.context)


class TournamentView(django.views.generic.TemplateView):
    """Render 'leage.html' and 'cup.html' template."""

    #show info about leage or cup: full table and list of matches and tours
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
    """Render 'cups.html' template."""

    # show info about cups: not full touranment table and last played tour
    template_name = 'cups.html'
    context = {'leages': Tournament.objects.filter(tournament_type='cup'),
               'last_matches': Match.objects.get_last_matches_in_tournament()}
    def get(self, request):
        return render(request, self.template_name, self.context)


class MatchView(django.views.generic.TemplateView):
    """Render 'match.html' template."""

    # show info about match
    template_name = 'match.html'
    def get(self, request, match_id):
        context = {'match': Match.objects.filter(id=match_id)}
        return render(request, self.template_name, context)

class PlayerView(django.views.generic.TemplateView):
    """Render 'player.html' template."""

    # show info about player
    template_name = 'player.html'
    def get(self, request, player_id):
        context = {'player' : Player.objects.filter(id=player_id)}
        return render(request, self.template_name, context)


class TeamView(django.views.generic.TemplateView):
    """Render 'team.html' template."""

    # show info about team
    template_name = 'team.html'
    def get(self, request, team_id):
        context = {'team' : Team.objects.filter(id=team_id),
                   'players' : Player.objects.filter(team_id=team_id)}
        return render(request, self.template_name, context)

class TeamsView(django.views.generic.TemplateView):
    """Render 'teams.html' template."""

    template_name = 'teams.html'
    form_class = TeamForm

    #edit info about team
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name,
                      {'teams': Team.objects.all()})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        Team(name=form['team_name'].value(), coach=form['coach'].value()).save()
        return render(request, self.template_name, {'teams':Team.objects.all()})


class NewsView(django.views.generic.TemplateView):
    """Render 'news.html' template."""

    #static page
    template_name = 'news.html'
    def get(self, request, *args, **kwargs):
        context=''
        return render(request,self.template_name,context)


class TournamentListView(django.views.generic.TemplateView):
    """Render 'tournament_list.html' template."""

    #CRUD operations with tournaments
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

class AdminView(django.views.generic.TemplateView):

    # CRUD operations with tournaments
    template_name = 'admin.html'
    context = {'tournaments':Tournament.objects.all()}

    def get(self, request, *args, **kwargs):
        template_name = 'admin.html'
        context = {'tournaments': Tournament.objects.all(),
                   'teams': Team.objects.all()}
        return render(request, template_name, context)

class CreateTournamentView(django.views.generic.TemplateView):

    def get(self, request, *args, **kwargs):
        template_name = 'create_tournament.html'
        context=''
        return render(request, template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.request.POST
        Tournament(name=form['name'], loops_quantity=form['loops'], tournament_type=form['tournament_type'], status=form['status']).save()
        return HttpResponseRedirect(urls.reverse_lazy('edit_tournament', args=[Tournament.objects.get_last_id()]))


class EditTournamentView(django.views.generic.TemplateView):

    template_name = 'edit_tournament.html'

    def get(self, request, tournament_id):
        context = {'tournament': Tournament.objects.filter(id=tournament_id),
                   'teams': Team.objects.all()}
        return render(request, self.template_name, context)

    def post(self, request, tournament_id, *args, **kwargs):
        form = self.request.POST
        #if form.is_valid():
        Tournament.objects.filter(id=tournament_id).update(loops_quantity=form['loops'], name=form['name'], tournament_type=form['tournament_type'], status=form['status'])
        return HttpResponseRedirect(urls.reverse_lazy('edit_tournament', args=[
            tournament_id]))
        #else:
            #return HttpResponseRedirect(urls.reverse_lazy('index'))

class DeleteTournamentView(django.views.generic.TemplateView):
    template_name = 'delete_tournament.html'
    def get(self, request, tournament_id):
        name=''
        for item in Tournament.objects.filter(id=tournament_id):
            name = item.name
        context = {'name': name}
        Tournament.objects.filter(id=tournament_id).delete()
        return render(request, self.template_name, context)


class AddTeamView(django.views.generic.TemplateView):

    #Add team into tournament from list of teams
    template_name = 'add_team.html'
    def get(self, request, tournament_id):
        name=''
        for item in Tournament.objects.filter(id=tournament_id):
            name = item.name
        context = {'name': name,
                   'teams': Team.objects.all(),
                   'tour_teams':TourTeam.objects.filter(tournament_id=tournament_id).select_related('team'),
                   'tournament_id':tournament_id}
        return render(request, self.template_name, context)
    def post(self, request, tournament_id):
        form=self.request.POST
        TourTeam(tournament_id=tournament_id, team_id=form['team_id']).save()
        return HttpResponseRedirect(urls.reverse_lazy('add_team', args=[
            tournament_id]))

class GenerateScheduleView(django.views.generic.TemplateView):
    template_name = 'generate_schedule.html'

    def get(self, request, tournament_id):

        for item in Tournament.objects.filter(id=tournament_id):
            name = item.name
        Match.objects.filter(tournament_id=tournament_id).delete()
        context = {'schedule': Match.objects.generate_schedule(tournament_id),
                   'matches': Match.objects.filter(tournament_id=tournament_id),
                   'name' : name}
        return render(request, self.template_name, context)

class DeleteTeamView(django.views.generic.TemplateView):
    template_name = 'delete_team_from_tournament.html'
    def get(self, request, tourteam_id):
        tour=''
        team=''
        for item in TourTeam.objects.filter(id=tourteam_id).select_related('team').select_related('tournament'):
            tour = item.tournament.name
            team = item.team.name
        context = {'tour': tour,
                   'team':team}
        TourTeam.objects.filter(id=tourteam_id).delete()
        return render(request, self.template_name, context)

class CreateTeamView(django.views.generic.TemplateView):
    template_name = 'create_new_team_and_add.html'

    def post(self, request, tournament_id):
        form = self.request.POST
        Team(name=form['name'], coach=form['coach']).save()
        TourTeam(tournament_id=tournament_id, team_id=Team.objects.get_last_id()).save()
        return HttpResponseRedirect(urls.reverse_lazy('add_team', args=[
            tournament_id]))

class ResultsView(django.views.generic.TemplateView):
    template_name = 'results.html'

    def get(self, request, tournament_id):
        context = {'matches': Match.objects.filter(tournament_id=tournament_id)}
        return render(request, self.template_name, context)

class MatchResultsView(django.views.generic.TemplateView):
    template_name = 'match_result.html'

    def get(self, request, match_id):
        context = {'matches': Match.objects.filter(id=match_id)}
        return render(request, self.template_name, context)

    def post(self, request, match_id):
        form=self.request.POST
        Match.objects.filter(id=match_id).update(status='ended', home_id=form['home_id'], guest_id=form['guest_id'], score=form['score'], tournament_id=form['tournament_id'])
        Tournament.objects.filter(id=form['tournament_id']).update(status='started')
        return HttpResponseRedirect(urls.reverse_lazy('match_results', args=[match_id]))