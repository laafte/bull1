from datetime import datetime
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

    def __str__(self):
        return self.purpose


class MemberBooking(Booking):
    """
    A booking done by a member
    """
    class Meta:
        verbose_name = "medlemsbooking"
        verbose_name_plural = "medlemsbookinger"

    owner = models.ForeignKey(settings.AUTH_USER_MODEL)

    def __str__(self):
        return "{}: {}".format(self.owner.get_full_name(), self.purpose)


class GlobalBooking(Booking):
    """
    A booking without a specified owner
    """
    class Meta:
        verbose_name = "global booking"
        verbose_name_plural = "globale bookinger"

    owner_field_content = models.CharField(max_length=100, blank=True)


class BookingOccurrence(object):

    def __init__(self, from_time, to_time, booking, repeat_index=0):
        self.from_time = from_time
        self.to_time = to_time
        self.booking = booking
        self.repeat_index = repeat_index

    @staticmethod
    def get_occurrences(from_date, to_date):
        bs = [BookingOccurrence(b.from_time, b.to_time, b)
              for b in Booking.objects.filter(from_time__gte=from_date, to_time__lt=to_date, repeats__isnull=True)]
        for b in Booking.objects.filter(repeats__isnull=False):
            r_index = 0
            d = Event.REPEAT_DELTAS[b.repeats]
            while b.from_time + (d*r_index) < from_date:
                r_index += 1
            while b.from_time + (d*r_index) < to_date:
                bs.append(BookingOccurrence(b.from_time + (d*r_index),
                                            b.to_time + (d*r_index),
                                            b, r_index))
                r_index += 1
        bs.sort(key=lambda x: x.from_time)
        return bs