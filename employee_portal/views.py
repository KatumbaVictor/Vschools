from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.db.models import Count, Case, When, IntegerField, OuterRef, Exists
from formtools.wizard.views import SessionWizardView
from .forms import (PersonalInformationForm, EducationalBackgroundForm,
             WorkExperienceForm, CareerPrefencesForm)
from django.conf import settings
from django_countries import countries
from django.core.files.storage import FileSystemStorage
from django.utils import timezone
from django.db.models import Count
from .models import *
from employer_portal.models import *
from main.models import *
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.core.paginator import Paginator
from meta.views import Meta
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
            first_name = self.cleaned_data.get("first_name")
            last_name = self.cleaned_data.get("last_name")
            email = self.cleaned_data.get("email")
            username = f"{first_name} {last_name}"
            password = self.cleaned_data.get("confirm_password")

            user = User.objects.create_user(
                        username=username,
                        email=email,
                        password=password,
                        first_name=first_name,
                        last_name=last_name, 
                        account_type='Employee'
                    )

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
def dashboard_view(request):
    candidate = PersonalInformation.objects.get(user=request.user)

    total_applications = JobApplication.objects.filter(candidate=candidate).count()
    pending_applications = JobApplication.objects.filter(candidate=candidate, status="Pending").count()
    shortlisted_applications = JobApplication.objects.filter(candidate=candidate, status="Shortlisted").count()
    pending_interviews = JobInterview.objects.filter(candidate=candidate).count()
    pending_job_offers = JobOffer.objects.filter(candidate=candidate, status=JobOffer.JobOfferStatus.PENDING).count()
    profile_views = CandidateProfileView.objects.filter(candidate=candidate).count()
    recent_job_application_invites = JobApplicationInvite.objects.filter(candidate=candidate, candidate_response=JobApplicationInvite.CandidateResponseChoices.PENDING)[:3]


    meta = Meta(
        title=f"My Dashboard | {settings.META_SITE_NAME}",
        description="Access your personal job seeker dashboard. View saved jobs, applications, interviews, and profile details all in one place",
        keywords=["Job seeker dashboard", "career tools"],
        use_title_tag=True
    )


    context = {
        'total_applications': total_applications,
        'pending_applications': pending_applications,
        'shortlisted_applications': shortlisted_applications,
        'pending_interviews': pending_interviews,
        'pending_job_offers': pending_job_offers,
        'profile_views': profile_views,
        'job_application_invites': recent_job_application_invites,
        'meta': meta
    }

    return render(request, 'employee-portal/dashboard.html', context)

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

    viewer = PersonalInformation.objects.get(user=request.user)

    already_viewed = JobView.objects.filter(job=job, viewer=viewer).exists()

    if not already_viewed:
        JobView.objects.create(job=job, viewer=viewer)

    context = {
        'job': job,
        'job_requirements': job_requirements,
        'compensation_details': compensation_details,
        'application_details': application_details,
        'meta': job.as_meta()
    }

    if request.method == "POST":
        candidate = PersonalInformation.objects.get(user=request.user)
        company = job.company

        JobApplication.objects.create(job=job, candidate=candidate, company=company)


    return render(request, 'employee-portal/job-details.html', context)


@login_required
def company_profile(request, slug):
    candidate = PersonalInformation.objects.get(user=request.user)
    company = get_object_or_404(CompanyInformation, slug=slug)
    
    following = company in candidate.followed_employers.all()

    jobs = JobDetails.objects.filter(company=company, status="active").order_by("-created_at")

    context = {
        'company': company,
        'following': following,
        'jobs': jobs
    }

    return render(request, 'employee-portal/company-profile.html', context)

@login_required
def company_profiles(request):
    company_profiles = CompanyInformation.objects.all().annotate(job_count=Count('jobs'))

    context = {'company_profiles': company_profiles}

    return render(request, 'employee-portal/company-profiles.html', context)

@login_required
def job_listings(request):
    candidate = PersonalInformation.objects.get(user=request.user)
    saved_jobs_subquery = SavedJob.objects.filter(candidate=candidate, job=OuterRef('pk'))

    jobs = JobDetails.objects.annotate(is_saved=Exists(saved_jobs_subquery))

    meta = Meta(
        title=f"Browse Jobs | {settings.META_SITE_NAME}",
        description="Explore the latest job opportunities across industries. Find your next role and apply online today.",
        keywords=["job listings", "open jobs", "careers", "apply for jobs", "job opportunites"],
        use_title_tag=True
    )

    for job in jobs:
        candidate = PersonalInformation.objects.get(user=request.user)
        already_impressed = JobImpression.objects.filter(job=job, candidate=candidate).exists()

        if not already_impressed:
            JobImpression.objects.create(job=job, candidate=candidate)

    context = {
        'jobs': jobs,
        'meta': meta
    }

    return render(request, 'employee-portal/job-listings.html', context)


@login_required
def job_reviews(request, slug):
    job = get_object_or_404(JobDetails, slug=slug)
    job_reviews = JobRating.objects.filter(job=job)

    rating_percentages = job.rating_percentages()

    context = {
        'job': job,
        'reviews': job_reviews,
        'rating_percentages': rating_percentages
    }

    return render(request, 'employee-portal/job-reviews.html', context)


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


@require_POST
@login_required
def job_save_toggle(request, job_slug):
    job = get_object_or_404(JobDetails, slug=job_slug)
    candidate = PersonalInformation.objects.get(user=request.user)

    saved_job, created = SavedJob.objects.get_or_create(candidate=candidate, job=job)

    if not created:
        saved_job.delete()
        return JsonResponse({'saved':False, 'message': 'Job unsaved'})
    else:
        return JsonResponse({'saved': True, 'message': 'Job saved successfully!'})


@login_required
def saved_jobs(request):
    candidate = PersonalInformation.objects.get(user=request.user)
    saved_jobs = SavedJob.objects.select_related('job').filter(candidate=candidate)

    meta = Meta(
        title=f"Saved Jobs | {settings.META_SITE_NAME}",
        description="View all the jobs you have saved for future applications. Stay organized and apply when ready.",
        keywords=["saved jobs", "job seeker"],
        use_title_tag=True 
    )

    context = {
        'saved_jobs': saved_jobs,
        'meta': meta
    }

    return render(request, 'employee-portal/saved-jobs.html', context)



@require_POST
@login_required
def withdraw_job_application(request, job_application_id):
    candidate = PersonalInformation.objects.get(user=request.user)
    job_application = get_object_or_404(JobApplication, id=job_application_id, candidate=candidate)

    job_application.withdrawn = True
    job_application.withdrawn_at = timezone.now()
    job_application.withdraw_reason = request.POST.get('withdraw_reason', None)
    job_application.save(update_fields=['withdrawn', 'withdrawn_at', 'withdraw_reason'])

    return JsonResponse({'success': True, 'message': 'Your application has been withdrawn'})


@require_POST
@login_required
def toggle_follow(request, company_slug):
    company = get_object_or_404(CompanyInformation, slug=company_slug)
    candidate = PersonalInformation.objects.get(user=request.user)

    if company in candidate.followed_employers.all():
        candidate.followed_employers.remove(company)
        return JsonResponse({'status': 'unfollowed', 'message': f'You have unfollowed {company.company_name}'})
    else:
        candidate.followed_employers.add(company)
        return JsonResponse({'status': 'followed', 'message': f'You have followed {company.company_name}'})


@login_required
def application_detail(request, job_application_id):
    candidate = PersonalInformation.objects.get(user=request.user)
    job_application = get_object_or_404(JobApplication, id=job_application_id, candidate=candidate)

    context = {
        'job_application': job_application
    }

    return render(request, 'employee-portal/application-detail.html', context)