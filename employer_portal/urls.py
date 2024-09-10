from django.urls import path
from .views import *

app_name = 'employer_portal'

urlpatterns = [
    path('sign-up/', CompanySignUpWizard.as_view(), name="company_sign_up"),
    path('employee-profile/', employee_profile, name="employee_profile"),
    path('home/', home_page, name="home"),
    path('post-job/', post_job, name="post_job")
]