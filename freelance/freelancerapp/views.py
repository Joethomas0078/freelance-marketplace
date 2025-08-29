from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from clientapp.models import Application_Received, Job
from freelance_app.forms import FreelancerProfileForm
from freelance_app.models import FreelancerProfile
from django.contrib import messages


# Create your views here.

def freelancerindex(request):
    jobs = Job.objects.all()
    applied_jobs = Application_Received.objects.filter(candidate=request.user.freelancer_profile).values_list('job_id', flat=True)
    
    return render(request, 'freelancer/index.html', {
        'jobs': jobs,
        'applied_jobs': applied_jobs,
    })



@login_required
def update_profile(request):
    profile = get_object_or_404(FreelancerProfile, user=request.user)

    if request.method == 'POST':
        form = FreelancerProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('freelancer_dashboard')
        else:
            messages.error(request, "There was an error updating your profile. Please check the form.")
    else:
        form = FreelancerProfileForm(instance=profile)

    return render(request, 'freelancer/update_profile.html', {'form': form})


@login_required
def view_job_lists(request):
    if hasattr(request.user, 'freelancer_profile'):
        jobs = Job.objects.all()

        # Apply filters
        search = request.GET.get('search')
        location = request.GET.get('location')
        min_salary = request.GET.get('min_salary')

        if search:
            jobs = jobs.filter(job_name__icontains=search)
        if location:
            jobs = jobs.filter(client__company_location__icontains=location)
        if min_salary:
            try:
                min_salary = int(min_salary)
                jobs = jobs.filter(salary__gte=min_salary)
            except ValueError:
                pass  # If salary is not a number, ignore the filter

        # Distinct locations for the dropdown
        locations = Job.objects.values_list('client__company_location', flat=True).distinct()

        applications = Application_Received.objects.filter(
            candidate=request.user.freelancer_profile
        ).values('job_id', 'status')

        applied_jobs_status = {app['job_id']: app['status'] for app in applications}
    else:
        jobs = Job.objects.none()
        applied_jobs_status = {}
        locations = []

    return render(request, 'freelancer/job_list.html', {
        'jobs': jobs,
        'applied_jobs_status': applied_jobs_status,
        'locations': locations,
    })

def free_job_details(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    # Check if there's any accepted application
    accepted_app = job.applications.filter(status='accepted').first()

    return render(request, 'freelancer/job_details.html', {
        'job': job,
        'accepted_app': accepted_app
    })


@login_required
def apply_for_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    
    # Check if the user has already applied
    if Application_Received.objects.filter(job=job, candidate=request.user.freelancer_profile).exists():
        messages.warning(request, "You have already applied for this job.")
    else:
        Application_Received.objects.create(job=job, candidate=request.user.freelancer_profile)
        messages.success(request, "Application submitted successfully.")
    
    return redirect('view_job_lists')




def myjobs(request):
    if hasattr(request.user, 'freelancer_profile'):
        applications = Application_Received.objects.filter(candidate=request.user.freelancer_profile, status='accepted')
    else:
        applications = Application_Received.objects.none()

    return render(request, 'freelancer/myjobs.html', {
        'applications': applications,
        'now': now()  # Pass current time to the template
    })

from django.utils.timezone import now


def start_job(request, job_id):
    application = get_object_or_404(Application_Received, job__id=job_id, candidate=request.user.freelancer_profile)
    job = application.job

    if job.job_start_time > now().date():
        messages.error(request, "You cannot start this job before the start date.")
    elif job.deadline < now():
        messages.error(request, "Deadline has passed. Contract is cancelled.")
    else:
        job.status = "In progress"
        job.save()
        messages.success(request, "Job started successfully.")

    return redirect('myjobs')

def end_job(request, job_id):
    application = get_object_or_404(Application_Received, job__id=job_id, candidate=request.user.freelancer_profile)
    job = application.job

    if job.status == "In progress":
        job.status = "Completed"
        job.completed_at = now()
        job.save()
        messages.success(request, "Job ended successfully.")
    else:
        messages.error(request, "You can only end an ongoing job.")

    return redirect('myjobs')


from clientapp.models import ChatMessage
@login_required
def freelancer_chat_view(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    freelancer = request.user  # Freelancer is the logged-in user
    client = job.client.user  # Get the client who posted the job

    # Get chat messages for this job
    messages = ChatMessage.objects.filter(job=job).order_by('timestamp')

    if request.method == "POST":
        message_text = request.POST.get("message")
        if message_text:
            ChatMessage.objects.create(
                job=job,
                sender=freelancer, 
                receiver=client,  
                message=message_text
            )
        return redirect('freelancer_chat', job_id=job.id)  

    return render(request, 'freelancer/chat.html', {
        'job': job,
        'client': client,
        'messages': messages
    })
