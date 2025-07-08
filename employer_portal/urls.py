from django.urls import path, re_path
from .views import *
from .forms import *

app_name = 'employer_portal'

JobPostForms = [
        ('job-details', JobDetailsForm), 
        ('job-requirements', JobRequirementsForm),
        ('compensation-details', CompensationDetailsForm),
        ('application-details', ApplicationDetailsForm),
        ('review-and-publish', JobPostTermsAndConditionsForm),
    ]

InternshipPostForms = [
        ('internship-details', InternshipDetailsForm),
        ('eligibility-criteria', InternshipEligibilityCriteriaForm),
        ('internship-compensation-details', InternshipCompensationDetailsForm),
        ('internship-application-details', InternshipApplicationDetailsForm)
    ]

urlpatterns = [
    path('sign-up/', CompanySignUpWizard.as_view(), name="company_sign_up"),
    path('candidate-profile/<slug:slug>/', candidate_profile, name="candidate_profile"),
    path('dashboard/', dashboard_page, name="dashboard"),
    path('company-profile/', company_profile, name="company_profile"),
    re_path('post-job/(?P<step>.+)', JobPostWizardView.as_view(JobPostForms, url_name='employer_portal:job_post_wizard'), name="job_post_wizard"),
    re_path('post-internship/(?P<step>.+)', InternshipPostWizardView.as_view(InternshipPostForms, url_name='employer_portal:internship_post_wizard'), name="internship_post_wizard"),
    path('job-overview/<slug:slug>', job_overview, name='job_overview'),
    path('manage-jobs/<str:status>/', manage_jobs, name="manage_jobs"),
    path('manage-internships/<str:status>/', manage_internship_listings, name="manage_internships"),
    path('candidate-profiles/', candidate_profiles, name="candidate_profiles"),
    path('job-applications/<slug:slug>/<str:category>/', job_applications, name="job_applications"),
    path('manage-applicant/<slug:job_slug>/<slug:applicant_slug>', manage_applicant, name="manage_applicant"),
    path('schedule-interview/<slug:job_slug>/<slug:applicant_slug>', schedule_interview, name="schedule_interview"),
    path('hiring-decisions/<slug:job_slug>/<slug:applicant_slug>', hiring_decisions, name="hiring_decisions"),
    path('job-interview-schedules/<str:category>/', job_interview_schedules, name="job_interview_schedules"),
    path('job-interview-details/<slug:interview_slug>', job_interview_details, name="job_interview_details"),
    path('candidate-reviews/<slug:candidate_slug>/<str:category>/', candidate_reviews, name="candidate_reviews"),
    path('job-details/<slug:job_slug>/', job_details, name="job_details"),
    path('update-job/<slug:job_slug>', update_job, name="update_job"),
]