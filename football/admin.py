from django.contrib import admin
from football.models import Tournament, Team, Player, Match, Match_Player, Goal, TourTeam

admin.site.register(Tournament)
admin.site.register(Team)
admin.site.register(Player)
admin.site.register(Match)
admin.site.register(Match_Player)
admin.site.register(Goal)
admin.site.register(TourTeam)