from collections import OrderedDict
from django.utils import six
from rest_framework import serializers
from booking.models import Booking, MemberBooking, GlobalBooking
from members.models import Member


class OwnerSerializer(serializers.ModelSerializer):

    name = serializers.CharField(source='get_full_name')

    class Meta:
        model = Member
        fields = ['id', 'name']


# noinspection PyAbstractClass
class BookingOccurrenceSerializer(serializers.Serializer):
    id = serializers.IntegerField(source='booking.id')
    recurrence_num = serializers.IntegerField(source='repeat_index')
    type = serializers.SerializerMethodField()
    from_time = serializers.DateTimeField()
    to_time = serializers.DateTimeField()
    owner = serializers.SerializerMethodField()
    purpose = serializers.CharField(source='booking.purpose')

    def get_type(self, occ):
        try:
            b = occ.booking.memberbooking
            return "member"
        except MemberBooking.DoesNotExist:
            pass
        try:
            b = occ.booking.globalbooking
            return 'global'
        except GlobalBooking.DoesNotExist:
            pass
        return ""

    def get_owner(self, occ):
        if self.get_type(occ) == 'member':
            return OwnerSerializer().to_representation(occ.booking.memberbooking.owner)
        elif self.get_type(occ) == 'global':
            return occ.booking.globalbooking.owner_field_content \
                if occ.booking.globalbooking.owner_field_content != "" else None
        return None

    def to_representation(self, instance):
        """
        Object instance -> Dict of primitive datatypes.
        """
        ret = OrderedDict()
        fields = [field for field in self.fields.values() if not field.write_only]

        for field in fields:
            try:
                attribute = field.get_attribute(instance)
            except serializers.SkipField:
                continue

            if attribute is not None:
                representation = field.to_representation(attribute)
                if representation is None:
                    # Do not seralize empty objects
                    continue
                if isinstance(representation, list) and not representation:
                    # Do not serialize empty lists
                    continue
                ret[field.field_name] = representation

        return ret


class BookingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Booking
        fields = ['id', 'type', 'owner', 'purpose', 'from_time', 'to_time']

