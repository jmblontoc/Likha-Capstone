from django.contrib import admin
from django.db.models.base import ModelBase
from core.models import Profile
from . import models

admin.site.register(Profile)