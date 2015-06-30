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
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('name', models.CharField(verbose_name='navn', max_length=50)),
                ('slot', models.IntegerField(verbose_name='plassering', blank=True, null=True, choices=[(1, 'Sidebar'), (2, 'Topp')], unique=True)),
            ],
            options={
                'verbose_name': 'Meny',
                'verbose_name_plural': 'Menyer',
            },
        ),
        migrations.CreateModel(
            name='MenuItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('text', models.CharField(verbose_name='tekst', max_length=50)),
                ('icon', models.CharField(verbose_name='ikon', max_length=50, blank=True, help_text='https://www.google.com/design/icons/')),
                ('url', models.CharField(verbose_name='URL', max_length=255)),
                ('url_is_django', models.BooleanField(verbose_name='URL er django-url-navn', help_text='Ikke huk av denne om du ikke forstår hva det vil si.', default=False)),
                ('position', models.IntegerField(verbose_name='posisjon')),
                ('parent_menu', models.ForeignKey(to='dashboard.Menu', verbose_name='i meny', related_name='items')),
                ('sub_menu', models.OneToOneField(to='dashboard.Menu', blank=True, verbose_name='inneholder meny', related_name='parent_item', null=True)),
            ],
            options={
                'verbose_name': 'Menyelement',
                'ordering': ['parent_menu', 'position'],
                'verbose_name_plural': 'Menyelementer',
            },
        ),
        migrations.AlterUniqueTogether(
            name='menuitem',
            unique_together=set([('position', 'parent_menu')]),
        ),
    ]
