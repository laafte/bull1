# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('name', models.CharField(verbose_name='navn', max_length=50)),
                ('slot', models.IntegerField(choices=[(1, 'Sidebar'), (2, 'Topp')], null=True, blank=True, verbose_name='plassering', unique=True)),
            ],
            options={
                'verbose_name_plural': 'Menyer',
                'verbose_name': 'Meny',
            },
        ),
        migrations.CreateModel(
            name='MenuItem',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('text', models.CharField(verbose_name='tekst', max_length=50)),
                ('icon', models.CharField(max_length=50, verbose_name='ikon', blank=True, help_text='<a href="https://www.google.com/design/icons/">Oversikt over ikoner</a>')),
                ('url', models.CharField(verbose_name='URL', max_length=255)),
                ('url_is_django', models.BooleanField(default=False, verbose_name='URL er django-url-navn', help_text='Ikke huk av denne om du ikke forstår hva det vil si.')),
                ('position', models.IntegerField(verbose_name='posisjon')),
                ('parent_menu', models.ForeignKey(verbose_name='i meny', related_name='items', to='dashboard.Menu')),
                ('sub_menu', models.OneToOneField(verbose_name='inneholder meny', blank=True, to='dashboard.Menu', null=True, related_name='parent_item')),
            ],
            options={
                'verbose_name_plural': 'Menyelementer',
                'verbose_name': 'Menyelement',
                'ordering': ['parent_menu', 'position'],
            },
        ),
        migrations.AlterUniqueTogether(
            name='menuitem',
            unique_together=set([('position', 'parent_menu')]),
        ),
    ]
