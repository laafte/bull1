# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import members.models
from django.conf import settings


class Migration(migrations.Migration):

    replaces = [('members', '0001_initial'), ('members', '0002_auto_20150706_0039'), ('members', '0003_auto_20150706_2124'), ('members', '0004_auto_20150706_2335'), ('members', '0005_auto_20150707_2354')]

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('password', models.CharField(verbose_name='password', max_length=128)),
                ('last_login', models.DateTimeField(verbose_name='last login', blank=True, null=True)),
                ('username', models.CharField(verbose_name='brukernavn', unique=True, max_length=255)),
                ('is_active', models.BooleanField(default=True, verbose_name='er aktiv')),
                ('is_admin', models.BooleanField(default=False, verbose_name='er admin')),
                ('first_name', models.CharField(verbose_name='fornavn', blank=True, max_length=100)),
                ('last_name', models.CharField(verbose_name='etternavn', blank=True, max_length=100)),
                ('bio', models.TextField(verbose_name='om meg', blank=True)),
                ('profile_photo', models.ImageField(blank=True, null=True, upload_to=members.models._original_photo_location)),
                ('postal_code', models.CharField(verbose_name='postnummer', blank=True, max_length=4)),
                ('city', models.CharField(verbose_name='sted', blank=True, max_length=50)),
                ('address', models.TextField(verbose_name='adresse', blank=True)),
                ('phone', models.CharField(verbose_name='telefonnummer', blank=True, max_length=40)),
                ('email', models.EmailField(verbose_name='e-post', blank=True, max_length=254)),
                ('birth_date', models.DateField(verbose_name='fødselsdato', blank=True, null=True)),
                ('has_completed_profile', models.BooleanField(verbose_name='har fullført registrering')),
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
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('name', models.CharField(verbose_name='navn', max_length=60)),
                ('description', models.TextField(verbose_name='beskrivelse', blank=True)),
                ('is_ensemble', models.BooleanField(default=False, verbose_name='gruppering', help_text='Gruppen er en gruppering på Låfte')),
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
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('from_date', models.DateField(verbose_name='fra dato', blank=True, null=True)),
                ('to_date', models.DateField(verbose_name='til dato', blank=True, null=True)),
                ('description', models.TextField(verbose_name='beskrivelse', blank=True)),
                ('group', models.ForeignKey(verbose_name='gruppe', related_name='memberships', to='members.Group')),
                ('member', models.ForeignKey(verbose_name='medlem', related_name='memberships', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'gruppemedlemskap',
                'verbose_name': 'gruppemedlemskap',
            },
        ),
        migrations.CreateModel(
            name='LoA',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('from_date', models.DateField(verbose_name='fra dato')),
                ('to_date', models.DateField(verbose_name='til dato')),
                ('reason', models.TextField(verbose_name='årsak', blank=True)),
                ('membership', models.ForeignKey(verbose_name='medlemskap', to='members.GroupMembership')),
            ],
            options={
                'verbose_name_plural': 'permisjoner',
                'verbose_name': 'permisjon',
            },
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('title', models.CharField(verbose_name='tittel', max_length=60)),
                ('from_date', models.DateField(verbose_name='fra dato', blank=True, null=True)),
                ('to_date', models.DateField(verbose_name='til dato', blank=True, null=True)),
                ('description', models.TextField(verbose_name='beskrivelse', blank=True)),
                ('membership', models.ForeignKey(verbose_name='medlemskap', related_name='positions', to='members.GroupMembership')),
            ],
            options={
                'verbose_name_plural': 'stillinger',
                'verbose_name': 'stilling',
            },
        ),
        migrations.AddField(
            model_name='group',
            name='members',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, through='members.GroupMembership'),
        ),
        migrations.AlterField(
            model_name='member',
            name='has_completed_profile',
            field=models.BooleanField(default=True, verbose_name='har fullført registrering'),
        ),
        migrations.AlterField(
            model_name='member',
            name='profile_photo',
            field=models.ImageField(verbose_name='profilbilde', blank=True, null=True, upload_to=members.models._original_photo_location),
        ),
    ]
