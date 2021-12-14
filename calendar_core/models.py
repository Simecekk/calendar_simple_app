from django.db import models


class BaseModel(models.Model):
    created = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        db_index=True,
    )
    modified = models.DateTimeField(
        auto_now=True,
        editable=False,
        db_index=True,
    )

    class Meta:
        abstract = True


class ConferenceRoom(BaseModel):
    manager = models.ForeignKey('account.User', on_delete=models.PROTECT, related_name='conference_rooms')
    name = models.CharField(max_length=256)
    address = models.CharField(max_length=512)

    def __str__(self):
        return f'{self.name} : {self.id}'


class CalendarEvent(BaseModel):
    owner = models.ForeignKey('account.User', on_delete=models.CASCADE, related_name='own_calendar_events')
    agenda = models.TextField()
    name = models.CharField(max_length=512)
    start = models.DateTimeField()
    end = models.DateTimeField()
    participants = models.ManyToManyField('account.User', related_name='calendar_events')
    location = models.ForeignKey('ConferenceRoom', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f'{self.name} : {self.id}'
