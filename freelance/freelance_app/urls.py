from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [

    path('',views.index , name='index'),
    path('register/freelancer/', views.freelancer_register, name='freelancer_register'),
    path('register/client/', views.register_client, name='client_register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_user, name='logout'),
    
]

if settings.DEBUG:
    urlpatterns+=static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
