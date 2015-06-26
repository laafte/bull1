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
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='navn')),
                ('slot', models.IntegerField(choices=[(1, 'Sidebar'), (2, 'Topp')], unique=True, null=True, blank=True, verbose_name='plassering')),
            ],
            options={
                'verbose_name_plural': 'Menyer',
                'verbose_name': 'Meny',
            },
        ),
        migrations.CreateModel(
            name='MenuItem',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=50, verbose_name='tekst')),
                ('icon', models.CharField(help_text='https://www.google.com/design/icons/', max_length=50, blank=True, verbose_name='ikon')),
                ('url', models.CharField(max_length=255, verbose_name='URL')),
                ('url_is_django', models.BooleanField(help_text='Ikke huk av denne om du ikke forstår hva det vil si.', default=False, verbose_name='URL er django-url-navn')),
                ('position', models.IntegerField(verbose_name='posisjon')),
                ('parent_menu', models.ForeignKey(to='dashboard.Menu', related_name='items', verbose_name='i meny')),
                ('sub_menu', models.OneToOneField(to='dashboard.Menu', null=True, verbose_name='inneholder meny', related_name='parent_item', blank=True)),
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
