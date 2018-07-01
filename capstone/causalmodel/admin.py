from django.contrib import admin

# Register your models here.
from causalmodel.models import RootCause, DataMap, Block, Child, CausalModel

admin.site.register(RootCause)
admin.site.register(DataMap)
admin.site.register(Block)
admin.site.register(Child)
admin.site.register(CausalModel)
