# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('color', models.CharField(verbose_name='farge', blank=True, max_length=6)),
                ('title', models.CharField(verbose_name='navn', max_length=50)),
                ('description', models.TextField(verbose_name='beskrivelse', blank=True)),
                ('from_time', models.DateTimeField(verbose_name='fra')),
                ('to_time', models.DateTimeField(verbose_name='til')),
                ('repeats', models.IntegerField(choices=[(0, 'Daglig'), (10, 'Ukentlig'), (20, 'Annenhver uke'), (30, 'Månedlig')], null=True, blank=True, verbose_name='repeteres')),
            ],
        ),
    ]
