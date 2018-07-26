from django.contrib import admin

# Register your models here.
from configurations.models import CorrelationConf

admin.site.register(CorrelationConf)
