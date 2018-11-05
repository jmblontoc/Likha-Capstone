from django.forms import ModelForm
from causalmodel.models import SuggestedIntervention


class SuggestedInterventionForm(ModelForm):

    class Meta:
        model = SuggestedIntervention
        fields = ['name', 'reason']

