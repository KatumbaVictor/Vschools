from django.shortcuts import render, redirect
from formtools.wizard.views import SessionWizardView
from .forms import (PersonalInformationForm, EducationalBackgroundForm,
             WorkExperienceForm, CareerPrefencesForm)
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import os


Templates = {'personal_information': 'employee-portal/registration/personal-information.html',
            'educational_background': 'employee-portal/registration/educational-background.html',
            'work_experience':'employee-portal/registration/professional-information.html',
            'career_preferences': 'employee-portal/registration/career-preferences.html'}

class SignUpWizardView(SessionWizardView):
    file_storage = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'media'))

    form_list = [
        ('personal_information',PersonalInformationForm),
        ('educational_background', EducationalBackgroundForm),
        ('work_experience', WorkExperienceForm),
        ('career_preferences', CareerPrefencesForm),
    ]

    def get_template_names(self):
        return [Templates[self.steps.current]]

    def done(self, form_list, **kwargs):
        for form in form_list:
            print(form.cleaned_data)
        return redirect('verify_email')

def apply_page(request):
    return render(request, 'employee-portal/apply.html')

def job_details(request):
    return render(request, 'employee-portal/job-details.html')

def employer_profile(request):
    return render(request, 'employee-portal/employer-profile.html')