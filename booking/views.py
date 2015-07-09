from datetime import datetime, timedelta, date
from django.core.urlresolvers import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic import CreateView, ListView
from isoweek import Week
from booking.forms import MemberBookingForm
from booking.models import Booking
from rest_framework import generics as grviews


class BookingList(ListView):
    model = Booking

    @method_decorator(ensure_csrf_cookie)
    def dispatch(self, request, *args, **kwargs):
        return super(BookingList, self).dispatch(request, *args, **kwargs)


class MemberBookingAddView(CreateView):
    template_name = "booking/member_booking_add.html"
    form_class = MemberBookingForm
    success_url = reverse_lazy('booking:bookings')

    def get_initial(self):
        return {'from_t': '12:00', 'to_t': '14:00', 'date': date.today()}

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(MemberBookingAddView, self).form_valid(form)