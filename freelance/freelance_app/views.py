from pyexpat.errors import messages
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from freelance_app.forms import ClientRegistrationForm, FreelancerProfileForm, UserRegistrationForm
from freelance_app.models import Client, FreelancerProfile


# Create your views here.


def index(request):
    return render(request, 'index.html')

def freelancer_register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # Save the user
            user = form.save(commit=False)
            user.is_active = True  # Activate user account immediately
            plain_password = form.cleaned_data['password1']  # Get plain password from form
            user.set_password(plain_password)  # Hash password for the User table
            user.save()

            # Create a FreelancerProfile with the user and password
            FreelancerProfile.objects.create(
                user=user,
                password=plain_password  # Save the hashed password from User
            )

            # Automatically log the user in after registration
            login(request, user)
            return redirect('update_profile')  # Redirect to the profile update page
    else:
        form = UserRegistrationForm()

    return render(request, 'freelancer_register.html', {'form': form})  


import logging

logger = logging.getLogger(__name__)

def register_client(request):
    if request.method == 'POST':
        form = ClientRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful! Please wait for admin approval.")
            return redirect('login')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ClientRegistrationForm()
    return render(request, 'client_register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Check if user is Superadmin
            if user.is_superuser:
                login(request, user)
                return redirect('adminindex')  # Redirect superadmin to admin dashboard
            
            # Check if user is a Freelancer
            elif FreelancerProfile.objects.filter(user=user).exists():
                login(request, user)
                return redirect('freelancer_dashboard')  # Redirect freelancer to their dashboard
            
            # Check if user is a Client
            elif Client.objects.filter(user=user).exists():
                client = Client.objects.get(user=user)
                if client.is_approved:  # Ensure the client is approved
                    if user.is_active:  # Check if the user is active
                        login(request, user)
                        return redirect('client_dashboard')  # Redirect client to their dashboard
                    else:
                        messages.error(request, "Your account is inactive. Please contact admin.")
                        return redirect('login')
                else:
                    messages.error(request, "Your account is awaiting admin approval.")
                    return redirect('login')

            # If user exists but is not associated with any role
            else:
                messages.error(request, "Your account does not have access.")
                return redirect('login')
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login')

    return render(request, 'login.html')


def logout_user(request):
    logout(request)
    return redirect('index')


