from datetime import datetime, timedelta
from django.views.generic import CreateView, ListView
from booking.forms import MemberBookingForm
from booking.models import Booking


class BookingList(ListView):
    model = Booking


class MemberBookingAddView(CreateView):
    template_name = "booking/member_booking_add.html"
    form_class = MemberBookingForm

    def get_initial(self):
        time_now = datetime.now()
        # Rounds the time to next hour
        time_now += timedelta(minutes=60)
        time_now -= timedelta(minutes=time_now.minute % 60,
                              seconds=time_now.second,
                              microseconds=time_now.microsecond)
        # Computes an hour later than that
        next_hour = time_now + timedelta(minutes=60)
        return {'from_time': time_now, 'to_time': next_hour}

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(MemberBookingAddView, self).form_valid(form)