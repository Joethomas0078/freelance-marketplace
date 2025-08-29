from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from clientapp.forms import ClientUpdateForm, JobForm
from clientapp.models import Application_Received, ChatMessage, Job
from freelance_app.models import Client, FreelancerProfile
from django.contrib import messages
from django.contrib.auth.models import User

# Create your views here.
@login_required
def clientindex(request):
    return render(request, 'client/index.html')

@login_required
def job_list(request):
    if hasattr(request.user, 'client_profile'):  
        jobs = Job.objects.filter(client=request.user.client_profile).distinct()

        # Attach accepted application to each job
        for job in jobs:
            job.accepted_application = job.applications.filter(status='accepted').first()
    else:
        jobs = Job.objects.none()

    return render(request, 'client/job_list.html', {'jobs': jobs})



# @login_required
# def job_list(request):
#     if hasattr(request.user, 'client_profile'):  
#         jobs = Job.objects.filter(client=request.user.client_profile).exclude(applications__status='accepted').distinct()
#     else:
#         jobs = Job.objects.none()  

#     return render(request, 'client/job_list.html', {'jobs': jobs})

@login_required
def edit_job(request, job_id):
    job = get_object_or_404(Job, id=job_id, client=request.user.client_profile)

    if request.method == 'POST':
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            return redirect('job_list')  # Redirect back to the job list after saving
    else:
        form = JobForm(instance=job)

    return render(request, 'client/edit_job.html', {'form': form})

@login_required
def post_job(request):
    try:
        client = Client.objects.get(user=request.user)
    except Client.DoesNotExist:
        return redirect('client_dashboard')  # Ensure client is logged in

    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.client = client
            job.save()
            return redirect('client_dashboard')
    else:
        form = JobForm()

    return render(request, 'client/post_job.html', {'form': form})

@login_required
def job_details(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    return render(request, 'client/job_details.html', {'job': job})


@login_required
def view_responses(request, job_id):
    job = get_object_or_404(Job, id=job_id, client=request.user.client_profile)
    applications = Application_Received.objects.filter(job=job)

    return render(request, 'client/view_responses.html', {'job': job, 'applications': applications})

@login_required
def freelancer_detail(request, freelancer_id, job_id):
    freelancer = get_object_or_404(FreelancerProfile, id=freelancer_id)
    job = get_object_or_404(Job, id=job_id)
    return render(request, 'client/freelancer_detail.html', {'freelancer': freelancer, 'job': job})
@login_required
def select_freelancer(request, job_id, application_id):
    job = get_object_or_404(Job, id=job_id)
    selected_application = get_object_or_404(Application_Received, id=application_id, job=job)

    # Mark selected freelancer
    selected_application.status = 'accepted'
    selected_application.save()

    # Reject all other applications for the same job
    Application_Received.objects.filter(job=job).exclude(id=application_id).update(status='rejected')

    messages.success(request, f"{selected_application.candidate.freelancer_name} has been selected for this job.")
    return redirect('view_responses', job_id=job.id)


@login_required
def completed_jobs(request):
    if hasattr(request.user, 'client_profile'):
        jobs = Job.objects.filter(client=request.user.client_profile, status='Completed')

        for job in jobs:
            job.assigned_worker = Application_Received.objects.filter(job=job, status="accepted").first()
    else:
        jobs = Job.objects.none()

    return render(request, 'client/completed_jobs.html', {'jobs': jobs})

@login_required
def make_payment(request, job_id):
    job = get_object_or_404(Job, id=job_id, status="Completed", payment_status="pending")
    assigned_worker = Application_Received.objects.filter(job=job, status="accepted").first()
    
    return render(request, 'client/make_payment.html', {'job': job, 'assigned_worker': assigned_worker})

@login_required
def process_payment(request, job_id):
    job = get_object_or_404(Job, id=job_id, status="Completed", payment_status="pending")

    if request.method == "POST":
        # Simulate successful payment (Replace with actual gateway logic)
        card_number = request.POST.get("card_number")
        expiry_date = request.POST.get("expiry_date")
        cvv = request.POST.get("cvv")

        if not (card_number and expiry_date and cvv):
            messages.error(request, "Invalid card details. Please try again.")
            return redirect('make_payment', job_id=job.id)

        # If payment is successful, update payment status
        job.payment_status = "paid"
        job.save()
        
        messages.success(request, "Payment successful! The freelancer has been paid.")
        return redirect('completed_jobs')

    return redirect('make_payment', job_id=job.id)





@login_required
def chat_view(request, job_id, freelancer_id):
    job = get_object_or_404(Job, id=job_id)
    freelancer = get_object_or_404(User, id=freelancer_id)  # Ensure the freelancer exists

    # Get previous chat messages
    messages = ChatMessage.objects.filter(job=job).order_by('timestamp')

    if request.method == "POST":
        message_text = request.POST.get("message")
        if message_text:
            ChatMessage.objects.create(
                job=job,
                sender=request.user, 
                receiver=freelancer if request.user != freelancer else job.client.user,
                message=message_text
            )
        return redirect('chat_view', job_id=job.id, freelancer_id=freelancer.id)

    return render(request, 'client/chat.html', {
        'job': job,
        'freelancer': freelancer,
        'messages': messages
    })



def update_client_profile(request):
    client = request.user.client_profile  # assuming one-to-one link

    if request.method == 'POST':
        form = ClientUpdateForm(request.POST, request.FILES, instance=client)
        if form.is_valid():
            form.save()
            return redirect('client_dashboard')  # change this to your actual dashboard view name
    else:
        form = ClientUpdateForm(instance=client)

    return render(request, 'client/update_profile.html', {'form': form})