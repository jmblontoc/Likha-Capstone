from django.forms import ModelForm

from datainput.models import FamilyProfileLine, Patient, MonthlyReweighing, HealthCareWasteManagement, InformalSettlers, \
    UnemploymentRate


class FamilyProfileForm(ModelForm):

    class Meta:
        model = FamilyProfileLine
        fields = '__all__'
        exclude = ['family_profile']


class PatientForm(ModelForm):

    class Meta:
        model = Patient
        fields = '__all__'
        exclude = ['barangay', 'date_created']


class MonthlyReweighingForm(ModelForm):

    class Meta:
        model = MonthlyReweighing
        fields = '__all__'
        exclude = ['patient', 'date', 'status', 'uploaded_by']


class HealthCareWasteManagementForm(ModelForm):

    class Meta:
        model = HealthCareWasteManagement
        fields = '__all__'
        exclude = ['date']


class InformalSettlersForm(ModelForm):

    class Meta:
        model = InformalSettlers
        fields =  '__all__'
        exclude = ['date']


class UnemploymentRateForm(ModelForm):

    class Meta:
        model = UnemploymentRate
        fields = '__all__'
        exclude = ['date']