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
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='navn')),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('color', models.CharField(max_length=6, blank=True, verbose_name='farge')),
                ('title', models.CharField(max_length=50, verbose_name='navn')),
                ('description', models.TextField(blank=True, verbose_name='beskrivelse')),
                ('from_time', models.DateTimeField(verbose_name='fra')),
                ('to_time', models.DateTimeField(verbose_name='til')),
                ('repeats', models.IntegerField(choices=[(0, 'Ukentlig')], null=True, blank=True, verbose_name='repeteres')),
                ('calendar', models.ForeignKey(to='events.Calendar', verbose_name='kalender')),
            ],
        ),
    ]
