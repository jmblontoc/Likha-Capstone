from django.forms import ModelForm

from datainput.models import FamilyProfileLine, Patient


class FamilyProfileForm(ModelForm):

    class Meta:
        model = FamilyProfileLine
        fields = '__all__'
        exclude = ['family_profile']


class PatientForm(ModelForm):

    class Meta:
        model = Patient
        fields = '__all__'
        exclude = ['barangay']