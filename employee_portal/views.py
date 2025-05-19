from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Case, When, IntegerField
from formtools.wizard.views import SessionWizardView
from .forms import (PersonalInformationForm, EducationalBackgroundForm,
             WorkExperienceForm, CareerPrefencesForm)
from django.conf import settings
from django_countries import countries
from django.core.files.storage import FileSystemStorage
from django.db.models import Count
from .models import *
from employer_portal.models import *
from main.models import *
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
import os
import json

User = get_user_model()


Templates = {'personal_information': 'employee-portal/registration/personal-information.html',
            'educational_background': 'employee-portal/registration/educational-background.html',
            'work_experience':'employee-portal/registration/professional-information.html',
            'career_preferences': 'employee-portal/registration/career-preferences.html'}

class SignUpWizardView(SessionWizardView):
    file_storage = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'media'))

    form_list = [
        ('personal_information', PersonalInformationForm),
        ('educational_background', EducationalBackgroundForm),
        ('work_experience', WorkExperienceForm),
        ('career_preferences', CareerPrefencesForm),
    ]

    def get_template_names(self):
        return [Templates[self.steps.current]]

    def get_context_data(self, form, **kwargs):
        context = super().get_context_data(form=form, **kwargs)
        context['countries'] = countries

        return context

    def process_step(self, form):
        step_data = form.cleaned_data
        print(f"Step {self.steps.current} Data:", step_data)

        return super().process_step(form)

    def done(self, form_list, **kwargs):
        personal_information_form = PersonalInformationForm(form_list[0].cleaned_data)
        educational_background_form = EducationalBackgroundForm(form_list[1].cleaned_data)
        work_experience_form = WorkExperienceForm(form_list[2].cleaned_data)
        career_preferences_form = CareerPrefencesForm(form_list[3].cleaned_data)

        if personal_information_form.is_valid() and educational_background_form.is_valid() and work_experience_form.is_valid() and career_preferences_form.is_valid():
            user = personal_information_form.save()

            #Save Educational background information
            educational_background = educational_background_form.save(commit=False)
            educational_background.user = user
            educational_background_form.save()

            #Save work experience information
            work_experience = work_experience_form.save(commit=False)
            work_experience.user = user
            work_experience_form.save()

            #Save career preferences information
            career_preferences = career_preferences_form.save(commit=False)
            career_preferences.user = user
            career_preferences_form.save()

            return redirect('verify_email')

def apply_for_job(request, slug):
    job = get_object_or_404(JobDetails, slug=slug)

    context = {
        'job': job
    }

    return render(request, 'employee-portal/apply.html', context)

@login_required
def job_applications_view(request, category):
    candidate = PersonalInformation.objects.get(user=request.user)
    applications = JobApplication.objects.filter(candidate=candidate).order_by('-applied_at')

    if category == 'all-applications':
        applications = applications
    elif category == "reviewed":
        applications = JobApplication.objects.filter(candidate=candidate, status='Reviewed').order_by('-applied_at')
    elif category == "shortlisted":
        applications = JobApplication.objects.filter(candidate=candidate, status='Shortlisted').order_by('-applied_at')
    elif category == "interview-scheduled":
        applications = JobApplication.objects.filter(candidate=candidate, status="Interview Scheduled").order_by('-applied_at')
    elif category == "rejected":
        applications = JobApplication.objects.filter(candidate=candidate, status="Rejected").order_by('-applied_at')
    elif category == "pending":
        applicants = JobApplication.objects.filter(candidate=candidate, status="Pending").order_by('-applied_at')


    category_counts = JobApplication.objects.filter(candidate=candidate).aggregate(
        all_count=Count('id'),
        reviewed_count=Count(Case(When(status='Reviewed', then=1), output_field=IntegerField())),
        shortlisted_count=Count(Case(When(status='Shortlisted', then=1), output_field=IntegerField())),
        rejected_count=Count(Case(When(status='Rejected', then=1), output_field=IntegerField())),
        interview_scheduled_count=Count(Case(When(status='Interview Scheduled', then=1), output_field=IntegerField())),
        pending_count=Count(Case(When(status='Pending', then=1), output_field=IntegerField())),
    )


    context = {
        'applications': applications,
        'category': category, 
        'category_counts': category_counts
    }

    return render(request, 'employee-portal/job-applications.html', context)

@login_required
def job_details(request, slug):
    job = get_object_or_404(JobDetails, slug=slug)
    job_requirements = JobRequirements.objects.get(job_post=job)
    compensation_details = CompensationDetails.objects.get(job_post=job)
    application_details = ApplicationDetails.objects.get(job_post=job)

    compensation_details.benefits_and_incentives = [item.strip() for item in json.loads(compensation_details.benefits_and_incentives).split(',')]

    job_requirements.certifications_and_licenses = job_requirements.certifications_and_licenses
    job_requirements.additional_requirements = job_requirements.additional_requirements
    job_requirements.required_skills = [skill.strip() for skill in job_requirements.required_skills.split(',')]

    context = {
        'job': job,
        'job_requirements': job_requirements,
        'compensation_details': compensation_details,
        'application_details': application_details,
        'meta': job.as_meta()
    }

    if request.method == "POST":
        candidate = PersonalInformation.objects.get(user=request.user)

        JobApplication.objects.create(job=job, candidate=candidate)


    return render(request, 'employee-portal/job-details.html', context)

def employer_profile(request, slug):
    company = get_object_or_404(CompanyInformation, slug=slug)

    context = {
        'company': company
    }

    return render(request, 'employee-portal/employer-profile.html', context)

@login_required
def company_profiles(request):
    company_profiles = CompanyInformation.objects.all().annotate(job_count=Count('jobs'))

    context = {'company_profiles': company_profiles}

    return render(request, 'employee-portal/company-profiles.html', context)

@login_required
def job_listings(request):
    jobs = JobDetails.objects.all()

    context = {
        'jobs': jobs
    }

    return render(request, 'employee-portal/job-listings.html', context)


@login_required
def settings_profile(request):
    personal_information = PersonalInformation.objects.get(user=request.user)

    context = {
        'personal_information': personal_information
    }

    return render(request, 'employee-portal/settings/profile.html', context)

 
@login_required
def job_interviews(request, category):
    candidate = PersonalInformation.objects.get(user=request.user)
    job_interviews = JobInterview.objects.filter(candidate=candidate)

    if category == 'all-interviews':
        job_interviews = JobInterview.objects.filter(candidate=candidate)
    elif category == 'rescheduled-interviews':
        job_interviews = JobInterview.objects.filter(candidate=candidate, status=JobInterview.InterviewStatus.RESCHEDULED)
    elif category == 'completed-interviews':
        job_interviews = JobInterview.objects.filter(candidate=candidate, status=JobInterview.InterviewStatus.COMPLETED)
    elif category == 'canceled-interviews':
        job_interviews = JobInterview.objects.filter(candidate=candidate, status=JobInterview.InterviewStatus.CANCELLED)
    else:
        job_interviews = JobInterview.objects.filter(candidate=candidate)

    category_counts = JobInterview.objects.filter(candidate=candidate).aggregate(
        all_count=Count('id'),
        rescheduled_count=Count(Case(When(status=JobInterview.InterviewStatus.RESCHEDULED, then=1), output_field=IntegerField())),
        completed_count=Count(Case(When(status=JobInterview.InterviewStatus.COMPLETED, then=1), output_field=IntegerField())),
        canceled_count=Count(Case(When(status=JobInterview.InterviewStatus.CANCELLED, then=1), output_field=IntegerField())),
    )

    context = {
        'category':category,
        'category_counts': category_counts,
        'job_interviews': job_interviews
    }

    return render(request, 'employee-portal/job-interviews.html', context)


@login_required
def job_interview_details(request, interview_slug):
    interview = get_object_or_404(JobInterview, slug=interview_slug)

    context = {
        'interview': interview
    }

    return render(request, 'employee-portal/interview-details.html', context)