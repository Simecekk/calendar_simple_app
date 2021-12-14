from datetime import datetime, timedelta

from django.contrib.auth import get_user_model
from model_mommy import mommy
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from calendar_core.models import ConferenceRoom, CalendarEvent


class TestCalendarEventViewSet(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.superuser = get_user_model().objects.create_superuser(
            'john.rambo@gmail.com', 'secret', 'john', 'rambo'
        )
        self.user = get_user_model().objects.create_user(
            'chuck.norris@gmail.com', 'secret', 'chuck', 'norris'
        )
        self.client.login(username='chuck.norris@gmail.com', password='secret')

        self.conference_room = mommy.make(ConferenceRoom)

    def _get_calendar_event_data(self, **kwargs):
        data = {
            'participants': kwargs.get('participants', []),
            'location': kwargs.get('location', self.conference_room.id),
            'name': kwargs.get('name', 'Testing Name'),
            'agenda': kwargs.get('agenda', 'Testing agenda'),
            'start': kwargs.get('start', datetime.now().strftime('%Y-%m-%dT%H:%M')),
            'end': kwargs.get('end', (datetime.now() + timedelta(minutes=120)).strftime('%Y-%m-%dT%H:%M')),
        }
        return data

    def test_calendar_event_correct_owner(self):
        """ Owner should be the user who made the request """
        data = self._get_calendar_event_data()

        response = self.client.post('/calendar_events/', data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response_data = response.json()

        event = CalendarEvent.objects.get(name=response_data['name'])
        self.assertEqual(event.owner, self.user)

    def test_calendar_event_cannot_be_longer_than_8_hours(self):
        end = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%dT%H:%M')
        data = self._get_calendar_event_data(end=end)

        response = self.client.post('/calendar_events/', data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response_data = response.json()
        self.assertEqual(response_data['error_message'], 'Meeting cannot be longer than 8 hours')
