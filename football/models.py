from django.db import models
import math


class TournamentManager(models.Manager):

    '''Manager for model Tournament'''


    def get_last_id(self):
        last_id=0
        for item in Tournament.objects.all():
            if item.id > last_id:
                last_id=item.id
        return last_id

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

    objects = TournamentManager()


class TeamManager(models.Manager):

    '''Manager for model Team'''


    def get_last_id(self):
        last_id=0
        for item in Team.objects.all():
            if item.id > last_id:
                last_id=item.id
        return last_id

    # calculate points in leage for every team
    def get_team_matches_and_points_in_the_leage(self):
        team_stats_in_tournament = []
        #create list of dicts with teams statistic in leage with defult values
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
        #edit statistic using table with matches results
        for match in Match.objects.all():
            for item in team_stats_in_tournament:
                if match.home_id == item['team_id'] and match.tournament_id == item[
                    'tournament_id'] and match.status=='ended':
                    item['matches'] = item['matches']+1
                    if match.score[:match.score.find(':')]!='-':
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
                    'tournament_id'] and match.status=='ended':
                    item['matches'] = item['matches'] + 1
                    if match.score[:match.score.find(':')]!='-':
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


        #sort list of dicts by tournament_id
        team_stats_in_tournament.sort(key=lambda x: x['tournament_id'])

        #second sort by points after sorting by tournament_id
        def sort_items_by_tid(arr1, arr2):
            if arr1['tournament_id'] == arr2['tournament_id']:
                return arr1['points']-arr2['points']
            else:
                return 0
        team_stats_in_tournament.sort(cmp=sort_items_by_tid, reverse=True)
        i=1
        tournament_id=0

        #add rank for teams in tournaments
        for item in team_stats_in_tournament:
            if tournament_id!=item['tournament_id']:
                i=1
                tournament_id=item['tournament_id']
            item['rank'] = i
            i=i+1
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

    '''Manager for model Match'''

    #create list of dicts with tournament and list of tours
    def get_tour_number_in_tournament(self):
        highest_tournament_tour = []
        for tournament in Tournament.objects.all():
            last_tour = 0
            for match in Match.objects.all():
                if tournament.id == match.tournament_id \
                        and match.tour > last_tour:
                    last_tour = match.tour
            highest_tournament_tour_row = {
                'tournament_id': tournament.id,
                'last_tour': range(1, last_tour+1)
            }
            highest_tournament_tour.append(highest_tournament_tour_row)
        return highest_tournament_tour

    #returns all last matches in all tournaments
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

    #generate matches schedule for leage tournaments
    #algorithm for genaration schedule is not simple.
    # for example you have six teams in tournament(1,2,3,4,5,6).
    # and for example in first tour you have next pairs:
    #1 vs 2, 3 vs 4, 5 vs 6
    #next tour should have another pairs. lets create second tour.
    #1  vs 3 - this pair didn't play yet
    #2 vs 4 - and this pair didn't play yet
    #5 vs 6 - but this pair have already played
    #we have to remake this tour
    #There is a special algorithm for genaration schedule which i transformed in python code
    def generate_schedule(self, tournament_id):
        teams = []
        tour_id = int(tournament_id)
        #get list of teams in tournament
        for item in TourTeam.objects.all():
            if item.tournament_id == tour_id:
                teams.append(item.team_id)
        loops_quantity = 1
        for item in Tournament.objects.filter(id=tournament_id):
            loops_quantity = item.loops_quantity
        number_of_teams = len(teams)
        if number_of_teams % 2 == 1:
            teams.append(0)

        #get list with teams_id in format [1,2,3,4,5,6] and
        #returns list of teams in another combination [1,3,5,2,6,4]
        #in future every two teams create a match in schedule
        def scroll_arr(arr):
            result = []
            i = 0
            temp = []
            while i < len(arr):
                temp.append([arr[i], arr[i + 1]])
                i = i + 2
            snake_arr = []
            i = 0
            while i < len(temp):
                snake_arr.append(temp[i][1])
                i = i + 1
            i = len(temp) - 1
            while i > 0:
                snake_arr.append(temp[i][0])
                i = i - 1
            new_snake_arr = []
            new_snake_arr.append(snake_arr[len(snake_arr) - 1])
            i = 0
            while i < len(snake_arr) - 1:
                new_snake_arr.append(snake_arr[i])
                i = i + 1
            result.append(arr[0])
            result.append(new_snake_arr[0])
            i = 0
            new_arr = []
            while i < len(new_snake_arr) / 2:
                new_arr.append(new_snake_arr[len(new_snake_arr) - 1 - i])
                new_arr.append(new_snake_arr[i + 1])
                i = i + 1
            i = 0
            while i < len(new_arr):
                result.append(new_arr[i])
                i = i + 1
            return result


        #create list of list of teams. every list is make a tour
        def match_pairs_tour(teams):
            match_pairs_arr = []
            arr = teams
            i=0
            while i<len(teams)-1:
                arr=scroll_arr(arr)
                j = 0
                match_pairs_arr.append([])
                while j<len(arr):
                    match_pairs_arr[i].append(arr[j])
                    j = j+1
                i = i+1
            return match_pairs_arr
        pairs = match_pairs_tour(teams)
        i = 0
        loop = 1
        tour = 0
        #create matches in tournament with some default values
        while loop<=loops_quantity:
            i=0
            if loop%2 == 1:
                while i<len(pairs):
                    tour = tour + 1
                    tour_id = tournament_id
                    score = '-:-'
                    status = 'new'
                    j=0
                    if number_of_teams%2 == 0:
                        while j<len(pairs[i]):
                            Match(tournament_id=tour_id, tour=tour, score=score,status=status, home_id=pairs[i][j], guest_id=pairs[i][j+1]).save()
                            j=j+2
                    else:
                        while j<len(pairs[i]):
                            if j%2==0 and pairs[i][j]!=0 and pairs[i][j+1]!=0:
                                Match(tournament_id=tour_id, tour=tour, score=score,
                                      status=status, home_id=pairs[i][j],
                                      guest_id=pairs[i][j + 1]).save()
                            if j%2==1 and pairs[i][j]!=0 and pairs[i][j-1]!=0:
                                Match(tournament_id=tour_id, tour=tour, score=score,
                                      status=status, home_id=pairs[i][j],
                                      guest_id=pairs[i][j + 1]).save()
                            j=j+2
                    i = i + 1
            else:
                while i < len(pairs):
                    tour = tour + 1
                    tour_id = tournament_id
                    score = '-:-'
                    status = 'new'
                    j = 0
                    if number_of_teams % 2 == 0:
                        while j < len(pairs[i]):
                            Match(tournament_id=tour_id, tour=tour,
                                  score=score, status=status,
                                  home_id=pairs[i][j + 1],
                                  guest_id=pairs[i][j]).save()
                            j = j + 2
                    else:
                        while j < len(pairs[i]):
                            if j % 2 == 0 and pairs[i][j] != 0 and pairs[i][
                                        j + 1] != 0:
                                Match(tournament_id=tour_id, tour=tour,
                                      score=score,
                                      status=status, home_id=pairs[i][j + 1],
                                      guest_id=pairs[i][j]).save()
                            if j % 2 == 1 and pairs[i][j] != 0 and pairs[i][
                                        j - 1] != 0:
                                Match(tournament_id=tour_id, tour=tour,
                                      score=score,
                                      status=status, home_id=pairs[i][j + 1],
                                      guest_id=pairs[i][j]).save()
                            j = j + 2
                    i = i + 1
            loop = loop+1
        return 'ok'

    #not ready
    def generate_schedule_for_cup(self, tournament_id):
        teams = []
        tour_id = int(tournament_id)
        for item in TourTeam.objects.all():
            if item.tournament_id == tour_id:
                teams.append(item.team_id)
        teams_count = len(teams)
        tours = math.ceil(math.log(teams_count, 2))





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