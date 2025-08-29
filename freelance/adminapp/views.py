from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from clientapp.models import Job
from freelance_app.models import Client, FreelancerProfile

# Create your views here.

def adminindex(request):
    return render(request, 'admin/index.html')


def client_list(request):
    clients = Client.objects.all()  
    return render(request, 'admin/client_list.html', {'clients': clients})

@login_required
def client_detail(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    return render(request, 'admin/client_detail.html', {'client': client})

def approve_client(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    user = client.user  # Get the associated User model

    if not client.is_approved:
        client.is_approved = True
        user.is_active = True  
        client.save()
        user.save()  

        messages.success(request, f"{client.company_name} has been approved successfully!")

    return redirect('client_list')


def reject_client(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    user = client.user  # Get the associated User model

    # Delete the client and associated user
    user.delete()

    messages.success(request, f"{client.company_name} has been rejected and removed successfully!")

    return redirect('client_list')



from django.core.paginator import Paginator
@login_required
def freelancerlist(request):
    freelancers = FreelancerProfile.objects.all()
    
    # Pagination: 10 freelancers per page
    paginator = Paginator(freelancers, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'admin/freelancer_list.html', {'page_obj': page_obj})

@login_required
def freelancer_detail(request, freelancer_id):
    freelancer = get_object_or_404(FreelancerProfile, id=freelancer_id)
    return render(request, 'admin/freelancer_detail.html', {'freelancer': freelancer})


@login_required
def view_job_list(request):
    jobs = Job.objects.all().order_by('-created_at')
    return render(request, 'admin/job_list.html', {
        'jobs': jobs,
    })

def job_details(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    return render(request, 'admin/job_details.html', {'job': job})


