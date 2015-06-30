from django.contrib import admin
from booking.models import MemberBooking, GlobalBooking

admin.site.register(MemberBooking)
admin.site.register(GlobalBooking)