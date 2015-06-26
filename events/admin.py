from django.contrib import admin
from events.models import Calendar, Event

admin.site.register(Calendar)
admin.site.register(Event)