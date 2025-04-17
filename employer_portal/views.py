from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count, Case, When, IntegerField
from formtools.wizard.views import SessionWizardView, NamedUrlSessionWizardView
from django.contrib.auth.decorators import login_required
from .forms import *
from django.conf import settings
from django_countries import countries
from django.core.files.storage import FileSystemStorage
from moneyed import list_all_currencies
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.utils.text import slugify
from django.http import JsonResponse
import json
from .models import *
from employee_portal.models import *
from main.models import *
import os
import pytz

User = get_user_model()

Templates = {'company_information':'employer-portal/registration/company-information.html',
             'company_representative':'employer-portal/registration/company-representative.html',
             'billing_information':'employer-portal/registration/billing-information.html',
             'account_information':'employer-portal/registration/account-information.html',
        }


class CompanySignUpWizard(SessionWizardView):
    file_storage = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'media'))

    form_list = [
        ('company_information', CompanyInformationForm), 
        ('company_representative', CompanyRepresentativeForm),
        ('billing_information', BillingInformationForm),
        ('account_information', AccountInformationForm),
    ]

    def get_template_names(self):
        return [Templates[self.steps.current]]

    def get_context_data(self, form, **kwargs):
        context = super().get_context_data(form=form, **kwargs)

        if self.steps.current == 'billing_information':
            context['countries'] = countries
        elif self.steps.current == 'company_information':
            context['countries'] = countries

        return context

    def done(self, form_list, **kwargs):
        form_data = {}
        for form in form_list:
            form_data.update(form.cleaned_data)

        print(form_data)

        #Save user login information
        user = User.objects.create_user(
            account_type='Employer',
            username=str({form_data['first_name']}) + ' ' + str({form_data['last_name']}),
            first_name=form_data['first_name'],
            last_name=form_data['last_name'],
            email=form_data['email'],
            password=form_data['confirm_password']
        )

        #Saving company information
        company_information_form = CompanyInformationForm(form_list[0].cleaned_data)
        company_information = company_information_form.save(commit=False)
        company_information.user = user
        company_information_form.save()

        #Saving account representative information
        account_representative_form = CompanyRepresentativeForm(form_list[1].cleaned_data)
        account_representative = account_representative_form.save(commit=False)
        account_representative.user = user
        account_representative.company = company_information
        account_representative_form.save()

        #Saving billing information
        billing_information_form = BillingInformationForm(form_list[2].cleaned_data)
        billing_information = billing_information_form.save(commit=False)
        billing_information.user = user
        billing_information.company = company_information
        billing_information_form.save()

        return redirect('verify_email')


class InternshipPostWizardView(NamedUrlSessionWizardView):
    file_storage = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'media'))

    form_list = [
        ('internship-details', InternshipDetailsForm),
        ('eligibility-criteria', InternshipEligibilityCriteriaForm),
        ('internship-compensation-details', InternshipCompensationDetailsForm),
        ('internship-application-details', InternshipApplicationDetailsForm)
    ]

    templates = {'internship-details':'employer-portal/post-internship/internship-details.html',
                 'eligibility-criteria':'employer-portal/post-internship/eligibility-criteria.html',
                 'internship-compensation-details':'employer-portal/post-internship/compensation-details.html',
                 'internship-application-details':'employer-portal/post-internship/application-details.html',
        }

    def get_template_names(self):
        return [self.templates[self.steps.current]]

    def get_context_data(self, form, **kwargs):
        context = super().get_context_data(form=form, **kwargs)

        if self.steps.current == 'internship-compensation-details':
            context['currencies'] = list_all_currencies()
        elif self.steps.current == 'internship-details':
            context['countries'] = countries

        return context

    def done(self, form_list, **kwargs):
        company = CompanyInformation.objects.get(user=self.request.user)

        #Saving Internship details
        internship_details_form = InternshipDetailsForm(form_list[0].cleaned_data)
        internship = internship_details_form.save(commit=False)
        internship.company = company
        internship.slug = slugify(internship.internship_title)
        internship_details_form.save()

        #Saving Eligibility criteria
        eligibility_criteria_form = InternshipEligibilityCriteriaForm(form_list[1].cleaned_data)
        eligibility_criteria = eligibility_criteria_form.save(commit=False)
        eligibility_criteria.internship = internship
        eligibility_criteria_form.save()

        #Saving Internship compensation details
        internship_compensation_details_form = InternshipCompensationDetailsForm(form_list[2].cleaned_data)
        internship_compensation_details = internship_compensation_details_form.save(commit=False)
        internship_compensation_details.internship = internship
        internship_compensation_details_form.save()

        #Saving Internship application details
        internship_application_details_form = InternshipApplicationDetailsForm(form_list[3].cleaned_data)
        internship_application_details = internship_application_details_form.save(commit=False)
        internship_application_details.internship = internship
        internship_application_details_form.save()

        return redirect('employer_portal:home')



class JobPostWizardView(NamedUrlSessionWizardView):
    file_storage = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'media'))

    form_list = [
        ('job-details', JobDetailsForm), 
        ('job-requirements', JobRequirementsForm),
        ('compensation-details', CompensationDetailsForm),
        ('application-details', ApplicationDetailsForm),
        ('review-and-publish', JobPostTermsAndConditionsForm),
    ]

    templates = {'job-details':'employer-portal/post-job/job-details.html',
                 'job-requirements':'employer-portal/post-job/job-requirements.html',
                 'compensation-details':'employer-portal/post-job/compensation-details.html',
                 'application-details':'employer-portal/post-job/application-details.html',
                 'review-and-publish': 'employer-portal/post-job/review-and-publish.html'
        }

    def get_template_names(self):
        return [self.templates[self.steps.current]]

    def get_context_data(self, form, **kwargs):
        context = super().get_context_data(form=form, **kwargs)

        if self.steps.current == 'compensation-details':
            context['currencies'] = list_all_currencies()
        elif self.steps.current == 'job-details':
            context['countries'] = countries
        elif self.steps.current == 'review-and-publish':
            context['data'] = self.get_all_cleaned_data()

        return context


    def done(self, form_list, **kwargs):
        company = CompanyInformation.objects.get(user=self.request.user)

        #Saving job details
        job_details_form = JobDetailsForm(form_list[0].cleaned_data)
        job_details = job_details_form.save(commit=False)
        job_details.company = company
        job_details.slug = slugify(job_details.job_title)
        job_details_form.save()

        #Saving job requirements
        job_requirements_form = JobRequirementsForm(form_list[1].cleaned_data)
        job_requirements = job_requirements_form.save(commit=False)
        job_requirements.job_post = job_details
        job_requirements_form.save()

        #Saving compensation details
        compensation_details_form = CompensationDetailsForm(form_list[2].cleaned_data)
        compensation_details = compensation_details_form.save(commit=False)
        compensation_details.job_post = job_details
        compensation_details_form.save()

        #Saving application details
        application_details_form = ApplicationDetailsForm(form_list[3].cleaned_data)
        application_details = application_details_form.save(commit=False)
        application_details.job_post = job_details
        application_details_form.save()


        return redirect('/employer-portal/home')


def home_page(request):
    company = CompanyInformation.objects.get(user=request.user)
    jobs = JobDetails.objects.filter(company=company)

    context = {'jobs':jobs, 'user':request.user}

    return render(request, 'employer-portal/home.html', context)

@login_required
def manage_jobs(request, status=None):
    company = CompanyInformation.objects.get(user=request.user)
    jobs = JobDetails.objects.filter(company=company)

    if status == 'all-jobs':
        jobs = JobDetails.objects.filter(company=company).annotate(application_count=Count('jobapplication'))
    elif status == "active":
        jobs = JobDetails.objects.filter(company=company, status='active').annotate(application_count=Count('jobapplication'))
    elif status == 'expired':
        jobs = JobDetails.objects.filter(company=company, status='expired').annotate(application_count=Count('jobapplication'))
    elif status == 'drafts':
        jobs = JobDetails.objects.filter(company=company, status='drafts').annotate(application_count=Count('jobapplication'))
    elif status == 'closed':
        jobs = JobDetails.objects.filter(company=company, status='closed').annotate(application_count=Count('jobapplication'))
    elif status == 'paused':
        jobs = JobDetails.objects.filter(company=company, status='paused').annotate(application_count=Count('jobapplication'))
    else:
        jobs = JobDetails.objects.filter(company=company).annotate(application_count=Count('jobapplication'))

    job_category_counts = JobDetails.objects.filter(company=company).aggregate(
        all_job_count=Count('id'),
        active_job_count=Count(Case(When(status='active', then=1), output_field=IntegerField())),
        expired_job_count=Count(Case(When(status='expired', then=1), output_field=IntegerField())),
        draft_job_count=Count(Case(When(status='drafts', then=1), output_field=IntegerField())),
        closed_job_count=Count(Case(When(status='closed', then=1), output_field=IntegerField())),
        paused_job_count=Count(Case(When(status='paused', then=1), output_field=IntegerField())),
    )

    context = {'jobs':jobs, 'status': status, 'job_counts': job_category_counts}

    return render(request, 'employer-portal/manage-jobs.html', context)


def job_overview(request, slug):
    company = CompanyInformation.objects.get(user=request.user)
    job = get_object_or_404(JobDetails, slug=slug, company=company)

    compensation_details = CompensationDetails.objects.get(job_post=job)
    job_requirements = JobRequirements.objects.get(company=company)
    application_details = ApplicationDetails.objects.get(job_post=job)

    context = {
        'job': job,
        'compensation': compensation_details,
        'job_requirements': job_requirements,
        'application_details': application_details
    }

    return render(request, 'employer-portal/job-details.html', context)


def manage_internship_listings(request, status=None):
    company = CompanyInformation.objects.get(user=request.user)
    internships = InternshipDetails.objects.filter(company=company)

    if status == 'all-internships':
        internships = InternshipDetails.objects.filter(company=company)
    elif status == "active":
        internships = InternshipDetails.objects.filter(company=company, status='active')
    elif status == 'expired':
        internships = InternshipDetails.objects.filter(company=company, status='expired')
    elif status == 'drafts':
        internships = InternshipDetails.objects.filter(company=company, status='drafts')
    elif status == 'closed':
        internships = InternshipDetails.objects.filter(company=company, status='closed')
    else:
        internships = InternshipDetails.objects.filter(company=company)

    context = {'internships':internships, 'status': status}
    return render(request, 'employer-portal/manage-internships.html', context)


def update_job_details(request, id, slug):
    if request.method == "POST" and request.headers.get('x-requested-with') == "XMLHttpRequest":
        job = get_object_or_404(JobDetails, id=id, slug=slug)
        form = JobDetailsForm(request.POST, instance=job)

        if form.is_valid():
            form.save()
            return JsonResponse({'success': True, 
                                'message': 'Job details updated successfully'}, 
                                status=200)
        else:
            return JsonResponse({'success': False, 'erros': form.erros}, status=400)


def edit_job_details(request, id, slug):
    job = get_object_or_404(JobDetails, id=id, slug=slug)
    form = JobDetailsForm(instance=job)

    context = {'job':job, 'countries':countries, 'form':form}

    return render(request, 'employer-portal/edit-jobs/edit-job-details.html', context)

def edit_requirement_details(request, id, slug):
    job = get_object_or_404(JobDetails, id=id, slug=slug)

    context = {'job':job}

    return render(request, 'employer-portal/edit-jobs/edit-job-requirements.html', context)

def edit_compensation_details(request, id, slug):
    job = get_object_or_404(JobDetails,id=id, slug=slug)
    compensation_details = CompensationDetails.objects.get(job_post=job)

    context = {
            'job': job, 
            'compensation_details':compensation_details,
            'currencies': list_all_currencies()
        }

    return render(request, 'employer-portal/edit-jobs/edit-compensation-details.html', context)

def edit_application_details(request, id, slug):
    job = get_object_or_404(JobDetails, id=id, slug=slug)
    application_details = ApplicationDetails.objects.get(job_post=job)

    context = {'job': job, 'application_details':application_details}

    return render(request, 'employer-portal/edit-jobs/edit-application-details.html', context)

def delete_job(request, id, slug):
    job = get_object_or_404(JobDetails, id=id, slug=slug)
    context = {'job': job}

    return render(request, 'employer-portal/delete-job.html', context)
    
def company_information(request):
    return render(request,"employer-portal/registration/company-information.html")

def candidate_profile(request, slug):
    candidate = get_object_or_404(PersonalInformation, slug=slug)
    candidate.skills = [skill.strip() for skill in candidate.skills.split(',')]

    total_reviews = CandidateRatingAndReview.objects.filter(candidate=candidate).aggregate(
            total_reviews=Count('review')
        )

    candidate.total_reviews = total_reviews['total_reviews']

    context = {'candidate': candidate}

    if request.method == "POST":
        print(request.POST)

    return render(request, 'employer-portal/candidate-profile.html', context)

def post_job(request):
    return render(request, 'employer-portal/post-job.html')

def candidate_profiles(request):
    candidates = PersonalInformation.objects.all()

    context = {
        'candidates': candidates
    }

    return render(request, 'employer-portal/candidate-profiles.html', context)

@login_required
def job_applications(request, slug, category):
    job = get_object_or_404(JobDetails, slug=slug)
    applicants = JobApplication.objects.filter(job=job)

    if category == 'all-applicants':
        applicants = JobApplication.objects.filter(job=job)
    elif category == "reviewed":
        applicants = JobApplication.objects.filter(job=job, status='Reviewed')
    elif category == "shortlisted":
        applicants = JobApplication.objects.filter(job=job, status='Shortlisted')
    elif category == "rejected":
        applicants = JobApplication.objects.filter(job=job, status="Rejected")
    elif category == "interview-scheduled":
        applicants = JobApplication.objects.filter(job=job, status="Interview Scheduled")
    elif category == "pending":
        applicants = JobApplication.objects.filter(job=job, status="Pending")
    else:
        applicants = JobApplication.objects.filter(job=job)

    category_counts = JobApplication.objects.filter(job=job).aggregate(
        all_count=Count('id'),
        reviewed_count=Count(Case(When(status='Reviewed', then=1), output_field=IntegerField())),
        shortlisted_count=Count(Case(When(status='Shortlisted', then=1), output_field=IntegerField())),
        rejected_count=Count(Case(When(status='Rejected', then=1), output_field=IntegerField())),
        interview_scheduled_count=Count(Case(When(status='Interview Scheduled', then=1), output_field=IntegerField())),
        pending_count=Count(Case(When(status='Pending', then=1), output_field=IntegerField())),
    )

    context = {
        'job': job,
        'applicants': applicants,
        'category': category, 
        'category_counts': category_counts
    }

    return render(request, 'employer-portal/job-applications.html', context)

@login_required
def manage_applicant(request, job_slug, applicant_slug):
    job = get_object_or_404(JobDetails, slug=job_slug)
    candidate = PersonalInformation.objects.get(slug=applicant_slug)
    job_application = JobApplication.objects.get(job=job, candidate=candidate)
    education_background = EducationalBackground.objects.get(user=candidate.user)
    work_experience = WorkExperience.objects.get(user=candidate.user)

    candidate.skills = [skill.strip() for skill in candidate.skills.split(',')]

    context = {
        'job': job,
        'candidate': candidate,
        'application': job_application,
        'education_background': education_background,
        'work_experience': work_experience,
        'career_preferences': CareerPreferences
    }

    return render(request, 'employer-portal/applicant-overview/manage-applicant.html', context)

@login_required
def schedule_interview(request, job_slug, applicant_slug):
    job = get_object_or_404(JobDetails, slug=job_slug)
    candidate = PersonalInformation.objects.get(slug=applicant_slug)
    job_application = JobApplication.objects.get(job=job, candidate=candidate)
    timezones = pytz.common_timezones

    context = {
        'job': job,
        'candidate': candidate,
        'application': job_application,
        'timezones': timezones
    }

    return render(request, 'employer-portal/applicant-overview/schedule-interview.html', context)