from django.db import models

class TournamentManager(models.Manager):
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

    def get_last_id(self):
        last_id=0
        for item in Team.objects.all():
            if item.id > last_id:
                last_id=item.id
        return last_id

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

        def sort_items_by_tid(arr1, arr2):
            if arr1['tournament_id'] == arr2['tournament_id']:
                return arr1['points']-arr2['points']
            else:
                return 0
        team_stats_in_tournament.sort(key=lambda x: x['tournament_id'])
        team_stats_in_tournament.sort(cmp=sort_items_by_tid, reverse=True)
        i=1
        tournament_id=0
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

    def generate_schedule(self, tournament_id):
        teams = []
        tour_id = int(tournament_id)
        for item in TourTeam.objects.all():
            if item.tournament_id == tour_id:
                teams.append(item.team_id)
        loops_quantity = 1
        for item in Tournament.objects.filter(id=tournament_id):
            loops_quantity = item.loops_quantity
        number_of_teams = len(teams)
        if number_of_teams % 2 == 1:
            teams.append(0)
        # arr = []
        # def create_arr(number, i=0):
        #     if i < number-1:
        #
        #         index = i + 1
        #         while index<=number-1:
        #             #arr[i].append([teams[i],teams[index]])
        #             arr.append([i, index])
        #             index = index +1
        #         create_arr(number, i + 1)


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
        # def match_pairs_tour(arr, number):
        #     match_pairs_arr=[[] for x in range(number-1)]
        #     i = 0
        #     while i < len(arr):
        #         j=0
        #         while j < len(match_pairs_arr):
        #             if arr[i][0] not in match_pairs_arr[j] \
        #                 and arr[i][1] not in match_pairs_arr[j]:
        #                 match_pairs_arr[j].append(arr[i][0])
        #                 match_pairs_arr[j].append(arr[i][1])
        #                 break
        #             j = j+1
        #         i=i+1
        #     return match_pairs_arr
        # num=6
        # new_arr=match_pairs_tour(arr,num)
        # import pdb
        # pdb.set_trace()
        # return new_arr
        pairs = match_pairs_tour(teams)
        i = 0
        loop = 1
        tour = 0

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