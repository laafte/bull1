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
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('password', models.CharField(verbose_name='password', max_length=128)),
                ('last_login', models.DateTimeField(verbose_name='last login', blank=True, null=True)),
                ('username', models.CharField(verbose_name='brukernavn', max_length=255, unique=True)),
                ('is_active', models.BooleanField(verbose_name='er aktiv', default=True)),
                ('is_admin', models.BooleanField(verbose_name='er admin', default=False)),
                ('first_name', models.CharField(verbose_name='fornavn', max_length=100, blank=True)),
                ('last_name', models.CharField(verbose_name='etternavn', max_length=100, blank=True)),
                ('bio', models.TextField(verbose_name='bio', blank=True)),
                ('profile_photo', models.ImageField(blank=True, null=True, upload_to=members.models._original_photo_location)),
                ('postal_code', models.CharField(verbose_name='postnummer', max_length=4, blank=True)),
                ('city', models.CharField(verbose_name='sted', max_length=50, blank=True)),
                ('address', models.TextField(verbose_name='adresse', blank=True)),
                ('phone', models.CharField(verbose_name='telefonnummer', max_length=40, blank=True)),
                ('email', models.EmailField(verbose_name='e-post', max_length=254, blank=True)),
                ('birth_date', models.DateField(verbose_name='fødselsdato', blank=True, null=True)),
                ('is_pang', models.BooleanField(verbose_name='er pang', default=False)),
            ],
            options={
                'verbose_name': 'medlem',
                'verbose_name_plural': 'medlemmer',
            },
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('name', models.CharField(verbose_name='navn', max_length=60)),
                ('description', models.TextField(verbose_name='beskrivelse', blank=True)),
                ('is_ensemble', models.BooleanField(verbose_name='gruppering', help_text='Gruppen er en gruppering på Låfte', default=False)),
                ('hidden', models.BooleanField(verbose_name='skjult', default=False)),
            ],
            options={
                'verbose_name': 'gruppe',
                'verbose_name_plural': 'grupper',
            },
        ),
        migrations.CreateModel(
            name='GroupMembership',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('from_date', models.DateField(verbose_name='fra dato', blank=True, null=True)),
                ('to_date', models.DateField(verbose_name='til dato', blank=True, null=True)),
                ('description', models.TextField(verbose_name='beskrivelse', blank=True)),
                ('group', models.ForeignKey(to='members.Group', verbose_name='gruppe', related_name='memberships')),
                ('member', models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='medlem', related_name='memberships')),
            ],
            options={
                'verbose_name': 'gruppemedlemskap',
                'verbose_name_plural': 'gruppemedlemskap',
            },
        ),
        migrations.CreateModel(
            name='LoA',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('from_date', models.DateField(verbose_name='fra dato')),
                ('to_date', models.DateField(verbose_name='til dato')),
                ('reason', models.TextField(verbose_name='årsak', blank=True)),
                ('membership', models.ForeignKey(verbose_name='medlemskap', to='members.GroupMembership')),
            ],
            options={
                'verbose_name': 'permisjon',
                'verbose_name_plural': 'permisjoner',
            },
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('title', models.CharField(verbose_name='tittel', max_length=60)),
                ('from_date', models.DateField(verbose_name='fra dato', blank=True, null=True)),
                ('to_date', models.DateField(verbose_name='til dato', blank=True, null=True)),
                ('description', models.TextField(verbose_name='beskrivelse', blank=True)),
                ('membership', models.ForeignKey(to='members.GroupMembership', verbose_name='medlemskap', related_name='positions')),
            ],
            options={
                'verbose_name': 'stilling',
                'verbose_name_plural': 'stillinger',
            },
        ),
    ]
