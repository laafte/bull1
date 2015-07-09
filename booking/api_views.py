from datetime import timedelta, datetime, time
from django.utils import timezone
from isoweek import Week
from rest_framework import generics
from booking.models import Booking, BookingOccurrence, MemberBooking
from booking.serializers import BookingSerializer, BookingOccurrenceSerializer


class BookingList(generics.ListAPIView):

    serializer_class = BookingOccurrenceSerializer

    def get_queryset(self):
        week = Week.thisweek()
        w = self.request.GET.get('week', None)
        if w is not None:
            week = Week.fromstring(w)
        from_day = datetime.combine(week.monday(), time())
        from_day = timezone.make_aware(from_day)
        to_day = from_day + timedelta(days=7)
        return BookingOccurrence.get_occurrences(from_day, to_day)
        # return Booking.objects.filter(from_time__gte=from_day, to_time__lt=to_day, repeats__isnull=True)


class BookingRemove(generics.DestroyAPIView):

    def get_queryset(self):
        return MemberBooking.objects.filter(owner=self.request.user)