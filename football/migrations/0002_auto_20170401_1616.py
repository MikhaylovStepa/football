# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-01 16:16
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('football', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default=b'Unknown', max_length=30)),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'player',
                'verbose_name_plural': 'players',
            },
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default=b'Unknown', max_length=30)),
                ('coach', models.CharField(max_length=30)),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'team',
                'verbose_name_plural': 'teams',
            },
        ),
        migrations.AlterModelOptions(
            name='tournament',
            options={'ordering': ['name'], 'verbose_name': 'tournament', 'verbose_name_plural': 'tournament'},
        ),
        migrations.AddField(
            model_name='player',
            name='team',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='football.Team'),
        ),
    ]
