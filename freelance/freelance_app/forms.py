from django import forms
from .models import Client, FreelancerProfile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']



class FreelancerProfileForm(forms.ModelForm):
    # Define choices for availability days
    AVAILABILITY_OPTIONS = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    ]

    # MultipleChoiceField for availability days with a custom widget
    availability_days = forms.MultipleChoiceField(
        choices=AVAILABILITY_OPTIONS,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input availability-checkbox'}),
        required=False
)


    # Meta class to define model and exclude user/password fields
    class Meta:
        model = FreelancerProfile
        exclude = ['user', 'password']
        widgets = {
            'profile_photo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your phone number'
            }),
            'freelancer_name':  forms.TextInput(attrs={
                'class': 'form-control'
            }),

            'availability_hours': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 9 AM - 5 PM'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Tell us about yourself'
            }),
            'portfolio_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'Link to your portfolio'
            }),
            'experience_years': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'placeholder': 'Years of experience'
            }),
            'education': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter your educational qualifications'
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Enter your address'
            }),
            'skills': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter your skills (e.g., Python, Django, JavaScript)'
            }),
            'languages': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Languages you speak'
            }),
            'certifications': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Certifications or courses you have completed'
            }),
            'references': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'References or recommendations'
            }),
            'hobbies': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Your hobbies or interests'
            }),
            'projects': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Describe your past projects'
            }),
        }

    # Custom save method (optional for further customizations)
    def save(self, commit=True):
        profile = super().save(commit=False)
        if commit:
            profile.save()
        return profile
 

class ClientRegistrationForm(UserCreationForm):
    company_name = forms.CharField(max_length=255, required=True)
    phone_number = forms.CharField(max_length=15, required=True)
    company_address = forms.CharField(widget=forms.Textarea, required=True)
    company_location = forms.CharField(widget=forms.TextInput  , required=True)
    company_zip = forms.CharField(widget=forms.TextInput, required=True)
    description = forms.CharField(widget=forms.Textarea, required=True)
    services = forms.CharField(widget=forms.Textarea, required=True)
    client_logo = forms.ImageField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_active = False  # Prevents login until admin approves

    # Store the plain-text password before saving (accessing cleaned_data)
        plain_password = self.cleaned_data.get('password1')

        if commit:
            user.save()
            client = Client.objects.create(
                user=user,
                company_name=self.cleaned_data['company_name'],
                phone_number=self.cleaned_data['phone_number'],
                company_address=self.cleaned_data['company_address'],
                company_location=self.cleaned_data['company_location'],
                company_zip=self.cleaned_data['company_zip'],
                description=self.cleaned_data['description'],
                services=self.cleaned_data['services'],
                client_logo=self.cleaned_data['client_logo'],
                is_approved=False,  # Admin must approve before login
                password=plain_password  # Store the plain password in Client table
            )
        return user



