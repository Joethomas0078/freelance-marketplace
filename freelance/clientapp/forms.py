from django import forms

from freelance_app.models import Client
from .models import Job

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['job_name', 'description', 'basic_requirements', 'job_start_time', 'deadline', 'basic_worker_qualification', 'salary', 'status']
        widgets = {
            'job_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter job name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'cols': 50}),
            'basic_requirements': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'cols': 50}),
            'job_start_time': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'deadline': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'basic_worker_qualification': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'cols': 50}),
            'salary': forms.NumberInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': ''}),  # Make this consistent with the styling of balance field
        }


class ClientUpdateForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = [
            'company_name', 'phone_number', 'company_address', 'company_location',
            'company_zip', 'description', 'services', 'client_logo'
        ]
        widgets = {
            'company_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter company name'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter phone number'}),
            'company_address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter company address'}),
            'company_location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter company location'}),
            'company_zip': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter company zip'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'cols': 50}),
            'services': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'cols': 50}),
            'client_logo': forms.FileInput(attrs={'class': 'form-control'}),
        }