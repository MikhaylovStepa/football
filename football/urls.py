"""cvs_land URL Configuration.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

import football.views

admin.autodiscover()

application_views = [
    url(regex=r'^$',
        view=football.views.IndexView.as_view(),
        name='index'),
    url(regex=r'^leage/$',
        view=football.views.LeageView.as_view(),
        name='leages'),
    url(regex=r'^tournament/$',
        view=football.views.TournamentView.as_view(),
        name='tournament'),
    url(regex=r'^tournament/(?P<tournament_id>[0-9]+)/$',
        view=football.views.TournamentView.as_view(),
        name='tournament'),
    url(regex=r'^cups/$',
        view=football.views.CupsView.as_view(),
        name='cups'),
    url(regex=r'^match/(?P<match_id>[0-9]+)/$',
        view=football.views.MatchView.as_view(),
        name='match'),
    url(regex=r'^player/(?P<player_id>[0-9]+)/$',
        view=football.views.PlayerView.as_view(),
        name='player'),
    url(regex=r'^team/(?P<team_id>[0-9]+)/$',
        view=football.views.TeamView.as_view(),
        name='team'),
    url(regex=r'^news/$',
        view=football.views.NewsView.as_view(),
        name='news'),
    url(regex=r'^teams/$',
        view=football.views.TeamsView.as_view(),
        name='teams'),
    url(regex=r'^tournament_list/$',
        view=football.views.TournamentListView.as_view(),
        name='tournament_list'),
    url(regex=r'^tournament_schedule/$',
        view=football.views.TournamentListView.as_view(),
        name='tournament_schedule'),
    url(regex=r'^admin/$',
        view=football.views.AdminView.as_view(),
        name='admin'),
    url(regex=r'^create_tournament/$',
        view=football.views.CreateTournamentView.as_view(),
        name='create_tournament'),
    url(regex=r'^edit_tournament/(?P<tournament_id>[0-9]+)/$',
        view=football.views.EditTournamentView.as_view(),
        name='edit_tournament'),
    url(regex=r'^delete_tournament/(?P<tournament_id>[0-9]+)/$',
        view=football.views.DeleteTournamentView.as_view(),
        name='delete_tournament'),
    url(regex=r'^add_team/(?P<tournament_id>[0-9]+)/$',
        view=football.views.AddTeamView.as_view(),
        name='add_team'),
    url(regex=r'^generate_schedule/(?P<tournament_id>[0-9]+)/$',
        view=football.views.GenerateScheduleView.as_view(),
        name='generate_schedule'),
    url(regex=r'^delete_team_from_tournament/(?P<tourteam_id>[0-9]+)/$',
        view=football.views.DeleteTeamView.as_view(),
        name='delete_team_from_tournament'),
    url(regex=r'^create_new_team_and_add/(?P<tournament_id>[0-9]+)/$',
        view=football.views.CreateTeamView.as_view(),
        name='create_new_team_and_add'),
    url(regex=r'^results/(?P<tournament_id>[0-9]+)/$',
        view=football.views.ResultsView.as_view(),
        name='results'),
    url(regex=r'^match_results/(?P<match_id>[0-9]+)/$',
        view=football.views.MatchResultsView.as_view(),
        name='match_results'),
]

default = [
    url(r'^admin/', admin.site.urls),
    static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)[0]
]

urlpatterns = application_views + default