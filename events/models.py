from datetime import timedelta
from django.core.exceptions import ValidationError
from django.db import models


class Event(models.Model):

    class Meta:
        ordering = ['from_time']

    DAILY = 0
    WEEKLY = 10
    BI_WEEKLY = 20
    REPEAT_INTERVALS = (
        (DAILY, "Daglig"),
        (WEEKLY, "Ukentlig"),
        (BI_WEEKLY, "Annenhver uke"),
    )

    REPEAT_DELTAS = {
        DAILY: timedelta(days=1),
        WEEKLY: timedelta(weeks=1),
        BI_WEEKLY: timedelta(weeks=2),
    }

    color = models.CharField(max_length=6, verbose_name="farge", blank=True)
    title = models.CharField(max_length=50, verbose_name="navn")
    description = models.TextField(verbose_name="beskrivelse", blank=True)
    from_time = models.DateTimeField(verbose_name="fra")
    to_time = models.DateTimeField(verbose_name="til")
    repeats = models.IntegerField(verbose_name="repeteres", choices=REPEAT_INTERVALS, blank=True, null=True)

    def clean(self):
        if self.to_time and self.from_time and self.to_time <= self.from_time:
            raise ValidationError("Tidsintervall kan ikke være negativt")