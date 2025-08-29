from django import forms

from clientapp.models import Application_Received



class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application_Received
        fields = []
        