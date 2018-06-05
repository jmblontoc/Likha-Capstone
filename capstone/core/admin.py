from django.contrib import admin
from django.db.models.base import ModelBase
from core.models import Profile, Notification
from . import models

admin.site.register(Profile)
admin.site.register(Notification)