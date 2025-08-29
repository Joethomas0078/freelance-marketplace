from django.urls import path
from . import views

urlpatterns = [

    path('',views.adminindex , name='adminindex'),
    path('client_list',views.client_list , name='client_list'),
    path('clients/<int:client_id>/', views.client_detail, name='client_detail'),
    path('clients/<int:client_id>/approve/', views.approve_client, name='approve_client'),
    path('reject-client/<int:client_id>/', views.reject_client, name='reject_client'),
    path('clients/freelancerlist', views.freelancerlist, name='freelancerlist'),
    path('clients/freelancerlist/<int:freelancer_id>/', views.freelancer_detail, name='freelancer_detail'),

    path('view_job_list', views.view_job_list, name='view_job_list'),
    path('job_details/<int:job_id>', views.job_details, name='job_details'),
    
    
]