from bootstrap3_datetime.widgets import DateTimePicker
from django.forms import ModelForm, DateTimeField
from booking.models import Booking, MemberBooking


class MemberBookingForm(ModelForm):
    from_time = DateTimeField(input_formats=["%d.%m.%Y  %H:%M"], widget=DateTimePicker(
        options={'format': 'DD.MM.YYYY HH:mm'}, format="%d.%m.%Y  %H:%M"
    ), label="Fra")
    to_time = DateTimeField(input_formats=["%d.%m.%Y  %H:%M"], widget=DateTimePicker(
        options={'format': 'DD.MM.YYYY HH:mm'}, format="%d.%m.%Y  %H:%M"
    ), label="Til")

    class Meta:
        model = MemberBooking
        fields = ['from_time', 'to_time', 'purpose', 'repeats']