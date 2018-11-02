from django.contrib import admin

# Register your models here.
from causalmodel.models import RootCause, DataMap, Block, Child, CausalModel, CausalModelComment, Memo, Box, Son, \
    SuggestedIntervention

admin.site.register(RootCause)
admin.site.register(DataMap)
admin.site.register(Block)
admin.site.register(Child)
admin.site.register(CausalModel)
admin.site.register(CausalModelComment)
admin.site.register(Memo)
admin.site.register(Box)
admin.site.register(Son)
admin.site.register(SuggestedIntervention)