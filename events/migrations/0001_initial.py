# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Calendar',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('name', models.CharField(verbose_name='navn', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('color', models.CharField(verbose_name='farge', max_length=6, blank=True)),
                ('title', models.CharField(verbose_name='navn', max_length=50)),
                ('description', models.TextField(verbose_name='beskrivelse', blank=True)),
                ('from_time', models.DateTimeField(verbose_name='fra')),
                ('to_time', models.DateTimeField(verbose_name='til')),
                ('repeats', models.IntegerField(verbose_name='repeteres', blank=True, null=True, choices=[(0, 'Daglig'), (10, 'Ukentlig'), (20, 'Annenhver uke'), (30, 'Månedlig')])),
                ('calendar', models.ForeignKey(verbose_name='kalender', to='events.Calendar')),
            ],
        ),
    ]
