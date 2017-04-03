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

class Team(models.Model):
    name = models.CharField(
        max_length=30,
        default='Unknown'
    )

    coach = models.CharField(
        max_length=30
    )

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