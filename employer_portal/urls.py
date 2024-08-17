from django.urls import path
from .views import *

app_name = 'employer_portal'

urlpatterns = [
    path('sign-up/step-one/', company_information, name="company_information"),
    path('employee-profile/', employee_profile, name="employee_profile"),
    path('home/', home_page, name="home"),
    path('post-job/', post_job, name="post_job")
]