from django.db import models

class Event(models.Model):

    DAILY = 0
    WEEKLY = 10
    BI_WEEKLY = 20
    MONTHLY = 30
    REPEAT_INTERVALS = (
        (DAILY, "Daglig"),
        (WEEKLY, "Ukentlig"),
        (BI_WEEKLY, "Annenhver uke"),
        (MONTHLY, "Månedlig"),
    )

    color = models.CharField(max_length=6, verbose_name="farge", blank=True)
    title = models.CharField(max_length=50, verbose_name="navn")
    description = models.TextField(verbose_name="beskrivelse", blank=True)
    from_time = models.DateTimeField(verbose_name="fra")
    to_time = models.DateTimeField(verbose_name="til")
    repeats = models.IntegerField(verbose_name="repeteres", choices=REPEAT_INTERVALS, blank=True, null=True)