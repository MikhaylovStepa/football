# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-01 19:49
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('football', '0002_auto_20170401_1616'),
    ]

    operations = [
        migrations.CreateModel(
            name='Goal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('minute', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('round', models.IntegerField()),
                ('status', models.CharField(default=b'not_started', max_length=10)),
                ('score', models.CharField(blank=True, max_length=10)),
                ('guest', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='match_homes', to='football.Team')),
                ('home', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='match_guests', to='football.Team')),
                ('tournament', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='football.Tournament')),
            ],
        ),
        migrations.CreateModel(
            name='Match_Player',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('match', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='football.Match')),
                ('player', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='football.Player')),
                ('team', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='football.Team')),
            ],
            options={
                'ordering': ['id'],
                'verbose_name': 'match player',
                'verbose_name_plural': 'match players',
            },
        ),
        migrations.CreateModel(
            name='TourTeam',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='football.Team')),
                ('tournament', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='football.Tournament')),
            ],
        ),
        migrations.AddField(
            model_name='goal',
            name='match',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='football.Match'),
        ),
        migrations.AddField(
            model_name='goal',
            name='player',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='football.Player'),
        ),
    ]
