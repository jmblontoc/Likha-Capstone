from django.forms import ModelForm

from datainput.models import FamilyProfileLine


class FamilyProfileForm(ModelForm):

    class Meta:
        model = FamilyProfileLine
        fields = '__all__'
        exclude = ['family_profile']