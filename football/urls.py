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
]

default = [
    url(r'^admin/', admin.site.urls),
    static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)[0]
]

urlpatterns = application_views + default