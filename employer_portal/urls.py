from django.urls import path
from .views import *

app_name = 'employer_portal'

urlpatterns = [
    path('sign-up/', CompanySignUpWizard.as_view(), name="company_sign_up"),
    path('employee-profile/', employee_profile, name="employee_profile"),
    path('home/', home_page, name="home"),
    path('post-job/', post_job, name="post_job"),
    path('post-job/job-details', post_job_details, name="job_details"),
    path('post-job/job-requirements', post_job_requirements, name="job_requirements"),
    path('post-job/compensation-details', compensation_details, name="compensation_details"),
    path('post-job/application-details', application_details, name="application_details"),
    path('post-job/review-and-publish', review_and_publish, name="review_and_publish")
]