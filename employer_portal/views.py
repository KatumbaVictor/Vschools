from django.shortcuts import render

def company_information(request):
    return render(request,"employer-portal/registration/company-information.html")


def employee_profile(request):
    return render(request, 'employer-portal/employee-profile.html')

def home_page(request):
    return render(request, 'employer-portal/home.html')

def post_job(request):
    return render(request, 'employer-portal/post-job.html')