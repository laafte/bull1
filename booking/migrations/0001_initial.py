# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('event_ptr', models.OneToOneField(auto_created=True, primary_key=True, serialize=False, parent_link=True, to='events.Event')),
                ('purpose', models.TextField(verbose_name='formål', blank=True)),
            ],
            options={
                'verbose_name': 'booking',
                'verbose_name_plural': 'bookinger',
            },
            bases=('events.event',),
        ),
        migrations.CreateModel(
            name='GlobalBooking',
            fields=[
                ('booking_ptr', models.OneToOneField(auto_created=True, primary_key=True, serialize=False, parent_link=True, to='booking.Booking')),
                ('owner_field_content', models.CharField(max_length=100, blank=True)),
            ],
            options={
                'verbose_name': 'global booking',
                'verbose_name_plural': 'globale bookinger',
            },
            bases=('booking.booking',),
        ),
        migrations.CreateModel(
            name='MemberBooking',
            fields=[
                ('booking_ptr', models.OneToOneField(auto_created=True, primary_key=True, serialize=False, parent_link=True, to='booking.Booking')),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'medlemsbooking',
                'verbose_name_plural': 'medlemsbookinger',
            },
            bases=('booking.booking',),
        ),
    ]
