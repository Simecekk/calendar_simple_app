from rest_framework import routers

from calendar_core.views import ConferenceRoomViewSet, CalendarEventViewSet

calendar_router = routers.DefaultRouter()

calendar_router.register('conference_rooms', ConferenceRoomViewSet)
calendar_router.register('calendar_events', CalendarEventViewSet)
