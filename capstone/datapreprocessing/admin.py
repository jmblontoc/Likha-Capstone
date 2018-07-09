from django.contrib import admin
from django.db.models.base import ModelBase

from datapreprocessing.models import Metric
from . import models
#
# for name in dir(models):
#     model = getattr(models, name)
#
#     if isinstance(model, ModelBase):
#         admin.site.register(model)

admin.site.register(Metric)
