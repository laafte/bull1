# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import members.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, blank=True, verbose_name='last login')),
                ('username', models.CharField(unique=True, max_length=255, verbose_name='brukernavn')),
                ('is_active', models.BooleanField(default=True, verbose_name='er aktiv')),
                ('is_admin', models.BooleanField(default=False, verbose_name='er admin')),
                ('first_name', models.CharField(max_length=100, blank=True, verbose_name='fornavn')),
                ('last_name', models.CharField(max_length=100, blank=True, verbose_name='etternavn')),
                ('bio', models.TextField(blank=True, verbose_name='bio')),
                ('profile_photo', models.ImageField(null=True, blank=True, upload_to=members.models._original_photo_location)),
                ('postal_code', models.CharField(max_length=4, blank=True, verbose_name='postnummer')),
                ('city', models.CharField(max_length=50, blank=True, verbose_name='sted')),
                ('address', models.TextField(blank=True, verbose_name='adresse')),
                ('phone', models.CharField(max_length=40, blank=True, verbose_name='telefonnummer')),
                ('email', models.EmailField(max_length=254, blank=True, verbose_name='e-post')),
                ('birth_date', models.DateField(null=True, blank=True, verbose_name='fødselsdato')),
                ('is_pang', models.BooleanField(default=False, verbose_name='er pang')),
            ],
            options={
                'verbose_name_plural': 'medlemmer',
                'verbose_name': 'medlem',
            },
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60, verbose_name='navn')),
                ('description', models.TextField(blank=True, verbose_name='beskrivelse')),
                ('is_ensemble', models.BooleanField(help_text='Gruppen er en gruppering på Låfte', default=False, verbose_name='gruppering')),
                ('hidden', models.BooleanField(default=False, verbose_name='skjult')),
            ],
            options={
                'verbose_name_plural': 'grupper',
                'verbose_name': 'gruppe',
            },
        ),
        migrations.CreateModel(
            name='GroupMembership',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('from_date', models.DateField(null=True, blank=True, verbose_name='fra dato')),
                ('to_date', models.DateField(null=True, blank=True, verbose_name='til dato')),
                ('description', models.TextField(blank=True, verbose_name='beskrivelse')),
                ('group', models.ForeignKey(to='members.Group', related_name='memberships', verbose_name='gruppe')),
                ('member', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='memberships', verbose_name='medlem')),
            ],
            options={
                'verbose_name_plural': 'gruppemedlemskap',
                'verbose_name': 'gruppemedlemskap',
            },
        ),
        migrations.CreateModel(
            name='LoA',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('from_date', models.DateField(verbose_name='fra dato')),
                ('to_date', models.DateField(verbose_name='til dato')),
                ('reason', models.TextField(blank=True, verbose_name='årsak')),
                ('membership', models.ForeignKey(to='members.GroupMembership', verbose_name='medlemskap')),
            ],
            options={
                'verbose_name_plural': 'permisjoner',
                'verbose_name': 'permisjon',
            },
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=60, verbose_name='tittel')),
                ('from_date', models.DateField(null=True, blank=True, verbose_name='fra dato')),
                ('to_date', models.DateField(null=True, blank=True, verbose_name='til dato')),
                ('description', models.TextField(blank=True, verbose_name='beskrivelse')),
                ('membership', models.ForeignKey(to='members.GroupMembership', related_name='positions', verbose_name='medlemskap')),
            ],
            options={
                'verbose_name_plural': 'stillinger',
                'verbose_name': 'stilling',
            },
        ),
    ]
