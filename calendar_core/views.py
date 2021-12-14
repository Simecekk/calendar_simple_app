from datetime import datetime, timedelta

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework import status

from calendar_core.filters import CalendarEventFilterSet
from calendar_core.models import ConferenceRoom, CalendarEvent
from calendar_core.serializers import ConferenceRoomEditSerializer, ConferenceRoomRetrieveSerializer, \
    CalendarEventEditSerializer, CalendarEventRetrieveSerializer


class EditRetrieveGetSerializerMixin:
    retrieve_serializer_class = NotImplementedError
    edit_serializer_class = NotImplementedError

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update':
            return self.edit_serializer_class
        elif self.action == 'list' or self.action == 'detail':
            return self.retrieve_serializer_class


class BaseCalendarAppViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    LoginRequiredMixin,
    EditRetrieveGetSerializerMixin,
    viewsets.GenericViewSet,
):
    pass


class CalendarEventViewSet(BaseCalendarAppViewSet):
    """
    Enables viewing and creating

    Owner of the calendar event is user who made the request.

    filter query params:

    1) day=%Y%m%d
    2) location_id=<int>
    3) query=<str>

    """
    retrieve_serializer_class = CalendarEventRetrieveSerializer
    edit_serializer_class = CalendarEventEditSerializer
    filterset_class = CalendarEventFilterSet
    queryset = CalendarEvent.objects.all()

    def get_queryset(self):
        return CalendarEvent.objects.filter(
            Q(participants__id=self.request.user.id) |
            Q(location__manager_id=self.request.user.id) |
            Q(owner_id=self.request.user.id)
        )

    def create(self, request, *args, **kwargs):
        start = datetime.strptime(self.request.data['start'], '%Y-%m-%dT%H:%M')  # TODO maybe use isoformat
        end = datetime.strptime(self.request.data['end'], '%Y-%m-%dT%H:%M')
        meeting_duration = end - start

        if meeting_duration > timedelta(hours=8):
            return Response(
                {'error_message': 'Meeting cannot be longer than 8 hours'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return super(CalendarEventViewSet, self).create(request, *args, **kwargs)


class ConferenceRoomViewSet(BaseCalendarAppViewSet):
    """
    Enables Retrieve and Create features
    """
    queryset = ConferenceRoom.objects.all()
    retrieve_serializer_class = ConferenceRoomRetrieveSerializer
    edit_serializer_class = ConferenceRoomEditSerializer

