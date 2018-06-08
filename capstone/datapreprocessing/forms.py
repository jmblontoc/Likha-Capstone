from django.forms import ModelForm, forms, Select, ChoiceField

from datapreprocessing.models import Metric


class MetricForm(ModelForm):

    class Meta:
        model = Metric
        fields = ['threshold']