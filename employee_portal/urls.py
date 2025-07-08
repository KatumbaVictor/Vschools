from django.urls import path
from .views import *

app_name = 'employee_portal'

urlpatterns = [
    path('sign-up/', SignUpWizardView.as_view(), name="employee_signup"),
    path('apply/<slug:slug>/', apply_for_job, name="apply_for_job"),
    path('job-details/<slug:slug>/', job_details, name="job_details"),
    path('company-profiles/', company_profiles, name="company_profiles"),
    path('company-profile/<slug:slug>', company_profile, name="company_profile"),
    path('job-listings/', job_listings, name="job_listings"),
    path('applications/<str:category>/', job_applications_view, name="job_applications"),
    path('settings/profile/', settings_profile, name="profile_settings"),
    path('job-interview-schedules/<str:category>/', job_interviews, name="job_interview_schedules"),
    path('job-interview-details/<slug:interview_slug>', job_interview_details, name="job_interview_details"),
]