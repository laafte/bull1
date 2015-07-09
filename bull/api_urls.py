from django.conf.urls import url, include
from booking import api_urls as booking_urls

urlpatterns = [
    url(r'^booking/', include(booking_urls, namespace='booking')),
]