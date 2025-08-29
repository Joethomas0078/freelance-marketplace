from django.urls import path
from . import views

urlpatterns = [

    path('',views.clientindex , name='client_dashboard'),
    path('post_job',views.post_job , name='post_job'),
    path('job_list',views.job_list , name='job_list'),
    path('job/<int:job_id>/responses/', views.view_responses, name='view_responses'),
    path('job/<int:job_id>/view_job_details/', views.job_details, name='view_job_details'),
    path('freelancer/<int:freelancer_id>/<int:job_id>/', views.freelancer_detail, name='freelancer_detail'),
    path('job/<int:job_id>/select/<int:application_id>/', views.select_freelancer, name='select_freelancer'),
    path('jobs/edit/<int:job_id>/', views.edit_job, name='edit_job'),
    path('completed_jobs/', views.completed_jobs, name='completed_jobs'),
    path('make_payment/<int:job_id>/', views.make_payment, name='make_payment'),
    path('process_payment/<int:job_id>/', views.process_payment, name='process_payment'),
    path('chat/<int:job_id>/<int:freelancer_id>/', views.chat_view, name='chat_view'),

    path('client/update-profile/', views.update_client_profile, name='update_client_profile'),

]