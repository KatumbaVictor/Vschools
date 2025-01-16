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
    path('employee-profile/', employee_profile, name="employee_profile"),
    path('home/', home_page, name="home"),
    re_path('post-job/(?P<step>.+)', JobPostWizardView.as_view(JobPostForms, url_name='employer_portal:job_post_wizard'), name="job_post_wizard"),
    re_path('post-internship/(?P<step>.+)', InternshipPostWizardView.as_view(InternshipPostForms, url_name='employer_portal:internship_post_wizard'), name="internship_post_wizard"),
    path('job-overview/<slug:slug>', job_overview, name='job_overview'),
    path('manage-jobs/<str:status>/', manage_jobs, name="manage_jobs"),
    path('manage-internships/<str:status>/', manage_internship_listings, name="manage_internships"),
    path('candidate-profiles/', candidate_profiles, name="candidate_profiles"),
]