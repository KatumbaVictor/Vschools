from django.urls import path
from .views import *

app_name = 'employee_portal'

urlpatterns = [
    path('sign-up/', SignUpWizardView.as_view(), name="employee_signup"),
    path('apply/<slug:slug>/', apply_for_job, name="apply_for_job"),
    path('dashboard/', dashboard_view, name="dashboard"),
    path('job-details/<slug:slug>/', job_details, name="job_details"),
    path('company-profiles/', company_profiles, name="company_profiles"),
    path('company-profile/<slug:slug>', company_profile, name="company_profile"),
    path('job-listings/', job_listings, name="job_listings"),
    path('job-reviews/<slug:slug>/', job_reviews, name="job_reviews"),
    path('applications/<str:category>/', job_applications_view, name="job_applications"),
    path('settings/profile/', settings_profile, name="profile_settings"),
    path('job-interview-schedules/<str:category>/', job_interviews, name="job_interview_schedules"),
    path('job-interview-details/<slug:interview_slug>', job_interview_details, name="job_interview_details"),
    path('job-save-toggle/<slug:job_slug>', job_save_toggle, name="job_save_toggle"),
    path('saved-jobs', saved_jobs, name='saved_jobs'),
    path('withdraw-application/<int:job_application_id>', withdraw_job_application, name="withdraw_application"),
    path('job-application/<int:job_application_id>', application_detail, name="job_application_details"),
    path('toggle-follow/<slug:company_slug>', toggle_follow, name="toggle_follow"),
]