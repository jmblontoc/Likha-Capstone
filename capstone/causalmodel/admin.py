from django.contrib import admin

# Register your models here.
from causalmodel.models import RootCause, DataMap

admin.site.register(RootCause)
admin.site.register(DataMap)
