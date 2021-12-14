from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models

import pytz


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, first_name=None, last_name=None, **extra_fields):
        if not email:
            raise ValueError('Enter an email address')
        if not first_name:
            raise ValueError('Enter a first name')
        if not last_name:
            raise ValueError('Enter a last name')
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, first_name, last_name):
        user = self.create_user(email, password=password, first_name=first_name, last_name=last_name)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


def get_timezone_choices():
    tz_choices = []
    for tz in pytz.all_timezones:
        tz_choices.append((tz, tz))

    return tz_choices


TIMEZONE_CHOICES = get_timezone_choices()


class User(AbstractUser):
    email = models.EmailField(unique=True)
    company_id = models.CharField(max_length=256)
    timezone = models.CharField(choices=TIMEZONE_CHOICES, max_length=100, default='UTC')
    username = models.CharField(max_length=512, null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()
