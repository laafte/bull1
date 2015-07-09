from django.conf.urls import url
from booking.api_views import BookingList, BookingRemove

urlpatterns = [
    url(r'^bookings/$', BookingList.as_view()),
    url(r'^bookings/(?P<pk>\d+)/', BookingRemove.as_view())
]