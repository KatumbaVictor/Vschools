from django.urls import path
from .views import *

app_name = 'employee_portal'

urlpatterns = [
    path('sign-up/', SignUpWizardView.as_view(), name="employee_signup"),
    path('apply/<slug:slug>/', apply_for_job, name="apply_for_job"),
    path('job-details/<slug:slug>/', job_details, name="job_details"),
    path('company-profiles/', company_profiles, name="company_profiles"),
    path('company-profile/<slug:slug>', employer_profile, name="company_profile"),
    path('job-listings/', job_listings, name="job_listings"),
    path('applications/', job_applications_view, name="job_applications"),
]