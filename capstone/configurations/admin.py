from django.contrib import admin

# Register your models here.
from configurations.models import CorrelationConf, NotifyBNS

admin.site.register(NotifyBNS)
admin.site.register(CorrelationConf)
