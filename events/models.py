from django.db import models


class Calendar(models.Model):
    name = models.CharField(max_length=50, verbose_name="navn")


class Event(models.Model):

    WEEKLY = 0
    REPEAT_INTERVALS = (
        (WEEKLY, "Ukentlig"),
    )

    color = models.CharField(max_length=6, verbose_name="farge", blank=True)
    calendar = models.ForeignKey(Calendar, verbose_name="kalender")
    title = models.CharField(max_length=50, verbose_name="navn")
    description = models.TextField(verbose_name="beskrivelse", blank=True)
    from_time = models.DateTimeField(verbose_name="fra")
    to_time = models.DateTimeField(verbose_name="til")
    repeats = models.IntegerField(verbose_name="repeteres", choices=REPEAT_INTERVALS, blank=True, null=True)