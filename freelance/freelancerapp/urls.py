from django.urls import path
from . import views

urlpatterns = [

    path('',views.freelancerindex , name='freelancer_dashboard'),
    path('freelancer/update-profile/', views.update_profile, name='update_profile'),
    path('freelancer/view_job_lists/', views.view_job_lists, name='view_job_lists'),
    path('freelancer/job_details_now/<int:job_id>/', views.free_job_details, name='free_job_details'),
    path('freelancer/apply/<int:job_id>/', views.apply_for_job, name='apply_for_job'),
    path('freelancer/myjobs/', views.myjobs, name='myjobs'),
    path('freelancer/start-job/<int:job_id>/', views.start_job, name='start_job'),
    path('freelancer/end-job/<int:job_id>/', views.end_job, name='end_job'),

    path("freelancer/chat/<int:job_id>/", views.freelancer_chat_view, name="freelancer_chat"),
    
    
]