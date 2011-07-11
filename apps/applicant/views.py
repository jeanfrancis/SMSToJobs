from django.db.models import Q

from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from django.contrib.auth.decorators import user_passes_test
from forms import ApplicantProfileForm, MobileNotificationForm
from models import ApplicantProfile, ApplicantJob
from job.models import Job
from job_recommendation.models import JobRecommendation

@user_passes_test(lambda u: u.is_authenticated(), login_url='/applicant/login')
def applicant_profile(request, first_time_setup=False, template='applicant/account/profile.html'):
    form = None 
    ctxt = {}
    ctxt['first_time_setup'] = first_time_setup
    profile = ApplicantProfile.objects.get(user=request.user)
    if request.method == 'POST':
        form = ApplicantProfileForm(data=request.POST, files=request.FILES, instance=profile, first_time_setup=first_time_setup, user=request.user)
        if form.is_valid():
            form.save()

            if 'first_name' in form.cleaned_data and form.cleaned_data['first_name'] != '':
                user = request.user
                user.first_name = form.cleaned_data['first_name']
                user.last_name = form.cleaned_data['last_name']
                user.email = form.cleaned_data['email']

                if 'password1' in form.cleaned_data and form.cleaned_data['password1'] != '':
                    user.set_password(form.cleaned_data['password1'])

                user.save()

            return redirect(reverse('applicant_dashboard'))
    else:
        form = ApplicantProfileForm(instance=profile, first_time_setup=first_time_setup, user=request.user)

    ctxt['form'] = form
    return render_to_response(template,
                              ctxt,
                              context_instance=RequestContext(request))

@user_passes_test(lambda u: u.is_authenticated(), login_url='/applicant/login')
def applicant_dashboard(request, template='applicant/account/dashboard.html'):
    profile = ApplicantProfile.objects.get(user=request.user)
    job_recommendations = JobRecommendation.objects.filter(applicant=profile).filter(job__state=Job.JOB_OPEN).filter(Q(state=JobRecommendation.NEW_REC) | Q(state=JobRecommendation.KEPT_NEW_REC) | Q(state=JobRecommendation.SAVED_REC))
    applicant_jobs = ApplicantJob.objects.filter(applicant=profile, state=ApplicantJob.APPLICATION_APPLIED).filter(job__state=Job.JOB_OPEN)
    return render_to_response(template, 
                              {'profile' : profile,
                               'applicant_jobs' : applicant_jobs,
                               'job_recommendations': job_recommendations, },
                              context_instance=RequestContext(request))


def apply(request, job_code=None, redirect_url=None):

    profile = ApplicantProfile.objects.get(user=request.user)
    try:
        job = Job.objects.get(job_code = job_code)
        application = ApplicantJob(applicant=profile, job=job)
        application.save()
    except Job.DoesNotExist:
        pass

    return redirect(reverse(redirect_url))

def remove_job(request, job_code=None, redirect_url=None):
    profile = ApplicantProfile.objects.get(user=request.user)
    try:
        job = Job.objects.get(job_code = job_code)
        recommendation = JobRecommendation.objects.get(job=job, applicant=profile)
        recommendation.state = JobRecommendation.DELETED_REC
        recommendation.save()
        try:
            application = ApplicantJob.objects.get(job=job, applicant=profile)
            application.state = 2
            application.save()
        except ApplicantJob.DoesNotExist:
            pass
    except Job.DoesNotExist, JobRecommendation.DoesNotExist:
        pass

    return redirect(reverse(redirect_url))

def view_profile(request, applicant_id=None, template='applicant/profile/profile.html'):
    applicant = ApplicantProfile.objects.get(pk=applicant_id)
    return render_to_response(template,
                              {'applicant':applicant},
                              context_instance=RequestContext(request))

