from django.shortcuts import render, redirect, get_object_or_404
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

def job_applications_view(request):
    applications_list = JobApplication.objects.filter(user=request.user).order_by('-applied_at')

    paginator = Paginator(applications_list, 10)
    page_number = request.GET.get('page')
    applications = paginator.get_page(page_number)

    context = {'applications': applications}

    return render(request, 'employee-portal/job-applications.html', context)

def job_details(request, slug):
    job = get_object_or_404(JobDetails, slug=slug)
    job_requirements = JobRequirements.objects.get(job_post=job)
    compensation_details = CompensationDetails.objects.get(job_post=job)
    application_details = ApplicationDetails.objects.get(job_post=job)

    job_requirements.certifications_and_licenses = job_requirements.certifications_and_licenses
    job_requirements.additional_requirements = job_requirements.additional_requirements

    context = {
        'job': job,
        'job_requirements': job_requirements,
        'compensation_details': compensation_details,
        'application_details': application_details,
        'meta': job.as_meta()
    }

    if request.method == "POST":
        user = request.user

        JobApplication.objects.create(job=job, user=user)


    return render(request, 'employee-portal/job-details.html', context)

def employer_profile(request, slug):
    company = get_object_or_404(CompanyInformation, slug=slug)

    context = {
        'company': company
    }

    return render(request, 'employee-portal/employer-profile.html', context)

def company_profiles(request):
    company_profiles = CompanyInformation.objects.all().annotate(job_count=Count('jobs'))

    context = {'company_profiles': company_profiles}

    return render(request, 'employee-portal/company-profiles.html', context)

def job_listings(request):
    jobs = JobDetails.objects.all()

    context = {
        'jobs': jobs
    }

    return render(request, 'employee-portal/job-listings.html', context)