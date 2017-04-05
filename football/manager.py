"""Managers for models"""

from django.db import models
import django.views.generic


class TeamManager(models.Manager):

    def get_team_matches_in_the_leage(self):
        team_matches_in_tournament = []
        for item in TourTeam.objects.all():
            team_matches_in_tournament_row = {'team_id': item.team_id,
                                              'tournament_id': item.tournament_id,
                                              'matches_count': 0}
            team_matches_in_tournament.append(team_matches_in_tournament_row)
        for match in Match.objects.all():
            for item in team_matches_in_tournament:
                if (match.home_id == item['team_id'] or match.guest_id == item[
                    'team_id']) and match.tournament_id == item[
                    'tournament_id']:
                    item['matches_count'] = item['matches_count'] + 1
        return team_matches_in_tournament