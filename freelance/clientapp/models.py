from django.db import models

from freelance_app.models import Client

# Create your models here.

class Job(models.Model):
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('closed', 'Closed'),
        ('in_progress', 'In Progress'),
    ]
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
    ]
    
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='jobs')
    
    job_type = models.CharField(max_length=255, default='Freelance', editable=False)
    description = models.TextField()
    job_name = models.CharField(max_length=255)  
    basic_requirements = models.TextField()  
    job_start_time = models.DateField()  
    deadline = models.DateTimeField()  
    basic_worker_qualification = models.TextField()  
    salary = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    completed_at = models.DateTimeField(null=True, blank=True)
    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES, default='pending')

    def __str__(self):
        return self.title
    
class Application_Received(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    candidate = models.ForeignKey('freelance_app.FreelancerProfile', on_delete=models.CASCADE)
    application_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')], default='pending')
    
    def __str__(self):
        return f'Application Received: {self.candidate} for Job: {self.job}'
    

from django.contrib.auth.models import User
from django.utils.timezone import now



class ChatMessage(models.Model):
    job = models.ForeignKey('Job', on_delete=models.CASCADE, related_name='chats')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chat between {self.sender} and {self.receiver}"
    







    