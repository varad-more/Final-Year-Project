from django import forms

class report_uploads(forms.Form):
    # category = forms.CharField()
    # title = forms.CharField()
    # date = forms.DateField()
    # notes = forms.CharField()
    report = forms.FileField()
    # publish = forms.CharField()