from django.db import models

class Tournament(models.Model):

    name = models.CharField(
        max_length=30,
        default='Unknown'
    )

    tournament_type = models.CharField(
        max_length=10,
        default='leage'
    )

    loops_quantity = models.IntegerField(
        default=1
    )

    status = models.CharField(
        max_length=10,
        default='new'
    )

    class Meta:
        """Meta parameters."""

        ordering = ['name']
        verbose_name = 'tournament'
        verbose_name_plural = 'tournament'

    def __unicode__(self):
        """New return representation."""
        return '{name}  - {tournament_type}'.format(
            name=self.name,
            tournament_type=self.tournament_type)


class TeamManager(models.Manager):

    def get_team_matches_and_points_in_the_leage(self):
        team_stats_in_tournament = []
        for item in TourTeam.objects.all().select_related('team'):
            team_matches_in_tournament_row = {'team_id': item.team_id,
                                              'team_name': item.team.name,
                                              'tournament_id': item.tournament_id,
                                              'matches': 0,
                                              'win':0,
                                              'draw':0,
                                              'lost':0,
                                              'goals':'0:0',
                                              'points': 0}
            team_stats_in_tournament.append(team_matches_in_tournament_row)
        for match in Match.objects.all():
            for item in team_stats_in_tournament:
                if match.home_id == item['team_id'] and match.tournament_id == item[
                    'tournament_id']:
                    item['matches'] = item['matches']+1
                    devide_score = match.score.find(':')
                    home_goals = int(match.score[:devide_score])
                    guest_goals = int(match.score[devide_score+1:])
                    devide_score_goals = item['goals'].find(':')
                    item['goals'] = str(int(item['goals'][:devide_score_goals])
                                        + home_goals) + ':' + \
                                    str(int(item['goals'][devide_score_goals+1:])+guest_goals)
                    if home_goals>guest_goals:
                        item['points'] = item['points']+3
                        item['win'] = item['win']+1
                    elif home_goals == guest_goals:
                        item['points'] = item['points']+1
                        item['draw'] = item['draw'] + 1
                    else:
                        item['lost'] = item['lost'] + 1
                if match.guest_id == item['team_id'] and match.tournament_id == item[
                    'tournament_id']:
                    item['matches'] = item['matches'] + 1
                    devide_score = match.score.find(':')
                    home_goals = int(match.score[:devide_score])
                    guest_goals = int(match.score[devide_score+1:])
                    devide_score_goals = item['goals'].find(':')
                    item['goals'] = str(int(item['goals'][:devide_score_goals])
                                        + guest_goals) + ':' + \
                                    str(int(item['goals'][
                                            devide_score_goals + 1:]) + home_goals)
                    if home_goals < guest_goals:
                        item['points'] = item['points'] + 3
                        item['win'] = item['win'] + 1
                    elif home_goals == guest_goals:
                        item['points'] = item['points'] + 1
                        item['draw'] = item['draw'] + 1
                    else:
                        item['lost'] = item['lost'] + 1

        def sort_items_by_tid(arr1, arr2):
            if arr1['tournament_id'] == arr2['tournament_id']:
                return arr1['points']-arr2['points']
            else:
                return 0
        team_stats_in_tournament.sort(key=lambda x: x['tournament_id'])
        team_stats_in_tournament.sort(cmp=sort_items_by_tid, reverse=True)
        return team_stats_in_tournament


class Team(models.Model):


    name = models.CharField(
        max_length=30,
        default='Unknown'
    )

    coach = models.CharField(
        max_length=30
    )

    objects = TeamManager()

    class Meta:
        """Meta parameters."""

        ordering = ['name']
        verbose_name = 'team'
        verbose_name_plural = 'teams'

    def __unicode__(self):
        """New return representation."""
        return '{name}'.format(
            name=self.name)


class Player(models.Model):
    name = models.CharField(
        max_length=30,
        default='Unknown'
    )

    team = models.ForeignKey(
        'Team',
        on_delete=models.SET_NULL,
        null=True
    )

    class Meta:
        """Meta parameters."""

        ordering = ['name']
        verbose_name = 'player'
        verbose_name_plural = 'players'

    def __unicode__(self):
        """New return representation."""
        return '{name}'.format(
            name=self.name)


class TourTeam(models.Model):
    team = models.ForeignKey(
        'Team',
        on_delete=models.SET_NULL,
        null=True
    )

    tournament = models.ForeignKey(
        'Tournament',
        on_delete=models.SET_NULL,
        null=True
    )

class Match_Player(models.Model):
    match=models.ForeignKey(
        'Match',
        on_delete=models.SET_NULL,
        null=True
    )

    player = models.ForeignKey(
        'Player',
        on_delete=models.SET_NULL,
        null=True
    )

    team = models.ForeignKey(
        'Team',
        on_delete=models.SET_NULL,
        null=True
    )

    class Meta:
        """Meta parameters."""

        ordering = ['id']
        verbose_name = 'match player'
        verbose_name_plural = 'match players'

class Goal(models.Model):
    match = models.ForeignKey(
        'Match',
        on_delete=models.SET_NULL,
        null=True
    )

    minute = models.IntegerField()

    player = models.ForeignKey(
        'Player',
        on_delete=models.SET_NULL,
        null=True
    )

class MatchManager(models.Manager):
    def get_last_matches_in_tournament(self):
        last_matches_in_tournament=[]
        highest_tournament_tour = []
        for tournament in Tournament.objects.all():
            last_tour=0
            for match in Match.objects.all():
                if tournament.id == match.tournament_id \
                        and match.tour > last_tour\
                        and match.status == 'ended':
                    last_tour=match.tour
            highest_tournament_tour_row = {
                'tournament_id': tournament.id,
                'last_tour': last_tour
            }
            highest_tournament_tour.append(highest_tournament_tour_row)
        for tournament in highest_tournament_tour:
            for match in Match.objects.all():
                if tournament['tournament_id']==match.tournament_id \
                    and tournament['last_tour']==match.tour:
                    last_matches_in_tournament_row = {
                        'match_id':match.id,
                        'tournament_id':match.tournament_id,
                        'last_tour':match.tour,
                        'team_home':match.home,
                        'team_guest':match.guest,
                        'score':match.score
                    }
                    last_matches_in_tournament.append(
                        last_matches_in_tournament_row)

        return last_matches_in_tournament

class Match(models.Model):
    tournament = models.ForeignKey(
        'Tournament',
        on_delete=models.SET_NULL,
        null=True
    )

    tour = models.IntegerField()

    status = models.CharField(
        max_length=10,
        default='not_started'
    )

    home = models.ForeignKey(
        'Team',
        on_delete=models.SET_NULL,
        null=True,
        related_name='match_guests'
    )

    guest = models.ForeignKey(
        'Team',
        on_delete=models.SET_NULL,
        null=True,
        related_name='match_homes'
    )

    score = models.CharField(
        max_length=10,
        blank=True
    )

    objects = MatchManager()