from bootstrap3_datetime.widgets import DateTimePicker
from django.core.exceptions import ValidationError
from django.forms import ModelForm, DateTimeField, TimeField, DateField, DateInput
from django.utils import timezone
from datetime import datetime, timedelta, time
from booking.models import Booking, MemberBooking, BookingOccurrence


class MemberBookingForm(ModelForm):
    date = DateField(input_formats=["%d.%m.%Y"], label="Dato", help_text="Format: dd.mm.åååå",
                     widget=DateInput(format="%d.%m.%Y"))
    from_t = TimeField(input_formats=["%H:%M", "%H%M", "%H.%M", "%H"], label="Fra kl.")
    to_t = TimeField(input_formats=["%H:%M", "%H%M", "%H.%M", "%H"], label="Til kl.")
    # from_time = DateTimeField(input_formats=["%d.%m.%Y  %H:%M"], widget=DateTimePicker(
    #     options={'format': 'DD.MM.YYYY HH:mm'}, format="%d.%m.%Y %H:%M"
    # ), label="Fra")
    # to_time_time = DateTimeField(input_formats=["%d.%m.%Y  %H:%M"], widget=DateTimePicker(
    #     options={'format': 'DD.MM.YYYY HH:mm'}, format="%d.%m.%Y %H:%M"
    # ), label="Til")

    def clean(self):
        super(MemberBookingForm, self).clean()
        try:
            d = self.cleaned_data['date']
            t0 = self.cleaned_data['from_t']
            t1 = self.cleaned_data['to_t']
        except KeyError:
            raise ValidationError("Ugyldig dato eller klokkslett")
        d0 = datetime.combine(d, t0)
        d1 = datetime.combine(d, t1)
        d0 = timezone.make_aware(d0)
        d1 = timezone.make_aware(d1)
        self.cleaned_data['d0'] = d0
        self.cleaned_data['d1'] = d1
        if d1 <= d0:
            raise ValidationError("Kan ikke slutte før det har begynt")
        tzd = timezone.make_aware(datetime.combine(d, time()))
        potential_cols = BookingOccurrence.get_occurrences(tzd, tzd + timedelta(days=1))
        for pc in potential_cols:
            if (d0 < pc.to_time) and (d1 > pc.from_time):
                raise ValidationError('Låfte er allerede booket på dette tidspunktet')

    def save(self, commit=True):
        self.instance.from_time = self.cleaned_data['d0']
        self.instance.to_time = self.cleaned_data['d1']
        return super(MemberBookingForm, self).save(commit)

    class Meta:
        model = MemberBooking
        fields = ['date', 'from_t', 'to_t', 'purpose']