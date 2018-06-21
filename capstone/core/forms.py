from django import forms
from django.forms import ModelForm

from core.models import Notification


class UploadFileForm(forms.Form):
    file = forms.FileField()


class RejectForm(ModelForm):

    class Meta:
        model = Notification
        fields = ['message']
