from django.conf import settings
from django.db import models
from events.models import Event


class Booking(Event):
    """
    Represents a booking of Låfte, generally for practice
    """
    class Meta:
        verbose_name = "booking"
        verbose_name_plural = "bookinger"

    purpose = models.TextField(blank=True, verbose_name="formål")

    def save(self, *args, **kwargs):
        self.title = "Låftebooking"
        super(Booking, self).save(*args, **kwargs)


class MemberBooking(Booking):
    """
    A booking done by a member
    """
    class Meta:
        verbose_name = "medlemsbooking"
        verbose_name_plural = "medlemsbookinger"

    owner = models.ForeignKey(settings.AUTH_USER_MODEL)


class GlobalBooking(Booking):
    """
    A booking without a specified owner
    """
    class Meta:
        verbose_name = "global booking"
        verbose_name_plural = "globale bookinger"

    owner_field_content = models.CharField(max_length=100, blank=True)