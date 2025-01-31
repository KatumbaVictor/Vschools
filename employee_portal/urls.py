from django.urls import path
from .views import *

app_name = 'employee_portal'

urlpatterns = [
    path('sign-up/', SignUpWizardView.as_view(), name="employee_signup"),
    path('apply/', apply_page, name="apply"),
    path('job-details/<slug:slug>/', job_details, name="job_details"),
    path('company-profile/', employer_profile, name="company_profile"),
    path('job-listings/', job_listings, name="job_listings"),
]