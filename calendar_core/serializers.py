import pytz
from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField

from account.models import User
from account.serializers import UserSerializer
from calendar_core.models import ConferenceRoom, CalendarEvent


class ConferenceRoomRetrieveSerializer(serializers.ModelSerializer):
    manager = UserSerializer()

    class Meta:
        model = ConferenceRoom
        fields = ['id', 'name', 'address', 'manager']


class ConferenceRoomEditSerializer(serializers.ModelSerializer):
    manager = PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = ConferenceRoom
        fields = ['name', 'address', 'manager']


class CalendarEventRetrieveSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    participants = UserSerializer(many=True, read_only=True)
    location = ConferenceRoomRetrieveSerializer()

    class Meta:
        model = CalendarEvent
        fields = ['id', 'owner', 'name', 'start', 'end', 'participants', 'location', ]


class CalendarEventEditSerializer(serializers.ModelSerializer):
    participants = PrimaryKeyRelatedField(queryset=User.objects.all(), many=True)
    location = PrimaryKeyRelatedField(queryset=ConferenceRoom.objects.all())

    class Meta:
        model = CalendarEvent
        fields = ['participants', 'location', 'name', 'agenda', 'start', 'end', ]

    def _get_utc_date(self, dt: 'datetime.datetime'):
        tz = pytz.timezone(self.context['request'].user.timezone)
        aware_dt = dt.replace(tzinfo=tz)
        utc_datetime = aware_dt.astimezone(pytz.utc)
        return utc_datetime

    def validate_start(self, validated_value):
        return self._get_utc_date(validated_value)

    def validate_end(self, validated_value):
        return self._get_utc_date(validated_value)

    @property
    def validated_data(self):
        validated_date = super(CalendarEventEditSerializer, self).validated_data
        validated_date.update({'owner': self.context['request'].user})
        return validated_date
