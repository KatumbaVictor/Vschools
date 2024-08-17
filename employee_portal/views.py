from django.shortcuts import render

def personal_information(request):
    return render(request,"employee-portal/registration/personal-information.html")

def professional_information(request):
    return render(request,"employee-portal/registration/professional-information.html")

def apply_page(request):
    return render(request, 'employee-portal/apply.html')

def job_details(request):
    return render(request, 'employee-portal/job-details.html')

def employer_profile(request):
    return render(request, 'employee-portal/employer-profile.html')