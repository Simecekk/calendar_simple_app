from django.db.models import Q
from django_filters.rest_framework import FilterSet
from django_filters import filters

from calendar_core.models import CalendarEvent, ConferenceRoom


class CalendarEventFilterSet(FilterSet):
    day = filters.DateFilter(field_name='start__date', label='day')
    query = filters.CharFilter(method='resolve_query', label='query')
    location_id = filters.ModelChoiceField(queryset=ConferenceRoom.objects.all())

    class Meta:
        model = CalendarEvent
        fields = ['location_id', 'query', 'day']

    @staticmethod
    def resolve_query(queryset, name, value):
        return CalendarEvent.objects.filter(
            Q(name__icontains=value) | Q(agenda__icontains=value)
        )
