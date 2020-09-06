from django import forms
from dashboard.models import *


class DocumentForm(forms.ModelForm):
    class Meta:
        model = reports
        fields = ('document', )