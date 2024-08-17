from django.urls import path
from .views import *

app_name = 'employee_portal'

urlpatterns = [
    path('sign-up/step-one/', personal_information, name="personal_info"),
    path('sign-up/step-two/', professional_information, name="professional_info"),
    path('apply/', apply_page, name="apply"),
    path('job-details/', job_details, name="job_details"),
    path('company-profile/', employer_profile, name="company_profile")
]