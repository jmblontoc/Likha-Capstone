from django.forms import ModelForm, forms, Select, ChoiceField, TextInput

from datapreprocessing.models import Metric


class MetricForm(ModelForm):

    class Meta:
        model = Metric
        fields = ['threshold', 'unit']


class EditMetricForm(ModelForm):

    class Meta:
        model = Metric
        fields = ['threshold']