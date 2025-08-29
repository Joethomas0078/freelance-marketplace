from django.db import models
from django.contrib.auth.models import User

class FreelancerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="freelancer_profile")
    freelancer_name = models.CharField(max_length=255, blank=True, null=True)
    profile_photo = models.ImageField(upload_to='profile/', blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    availability_days = models.JSONField(blank=True, null=True)  # Stores as ["Monday", "Wednesday"]
    availability_hours = models.CharField(max_length=255, blank=True, null=True)  # Format: "9 AM - 5 PM"
    description = models.TextField(blank=True, null=True)
    portfolio_url = models.URLField(blank=True, null=True)
    experience_years = models.PositiveIntegerField(blank=True, null=True)
    education = models.TextField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    skills = models.TextField(blank=True, null=True)
    languages = models.TextField(blank=True, null=True)
    certifications = models.TextField(blank=True, null=True)
    references = models.TextField(blank=True, null=True)
    hobbies = models.TextField(blank=True, null=True)
    projects = models.TextField(blank=True, null=True)
    password = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Freelancer Profile: {self.user.username}"



class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="client_profile")
    is_approved = models.BooleanField(default=False) 
    company_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    company_address = models.TextField(blank=True, null=True)
    company_location = models.CharField(max_length=150, blank=True, null=True)
    company_zip = models.CharField(max_length=10, blank=True,null=True)
    description = models.TextField(blank=True, null=True)
    services = models.TextField(blank=True, null=True)
    client_logo = models.ImageField(upload_to='clients/', blank=True, null=True)
    password = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Client: {self.user.username}"



