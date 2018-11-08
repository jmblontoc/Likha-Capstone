from django.forms import ModelForm

from causalmodel.models import RootCause


class RootCauseForm(ModelForm):

    class Meta:
        model = RootCause
        fields = ['name']