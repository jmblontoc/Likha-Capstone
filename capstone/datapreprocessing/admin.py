from django.contrib import admin
from django.db.models.base import ModelBase
from . import models

for name in dir(models):
    model = getattr(models, name)

    if isinstance(model, ModelBase):
        admin.site.register(model)
