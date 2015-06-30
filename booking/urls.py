from django.conf.urls import url
from booking.views import MemberBookingAddView, BookingList

urlpatterns = [
    url(r'^ny_booking/$', MemberBookingAddView.as_view(), name='new'),
    url(r'^$', BookingList.as_view(), name='bookings')
]