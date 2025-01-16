from django.shortcuts import render, redirect
from formtools.wizard.views import SessionWizardView
from .forms import (PersonalInformationForm, EducationalBackgroundForm,
             WorkExperienceForm, CareerPrefencesForm)
from django.conf import settings
from django_countries import countries
from django.core.files.storage import FileSystemStorage
from .models import PersonalInformation, EducationalBackground, WorkExperience, CareerPreferences
from django.contrib.auth import get_user_model
import os

User = get_user_model()


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

    def get_context_data(self, form, **kwargs):
        context = super().get_context_data(form=form, **kwargs)

        if self.steps.current == 'personal_information':
            context['countries'] = countries

        return context

    def done(self, form_list, **kwargs):
        form_data = {}

        for form in form_list:
            print(form.cleaned_data)
            form_data.update(form.cleaned_data)

        #Save user login information
        user = User.objects.create_user(
                account_type='Employee',
                username=str({form_data['first_name']}) + ' ' + str({form_data['last_name']}),
                first_name=form_data['first_name'],
                last_name=form_data['last_name'],
                email=form_data['email'],
                password=form_data['confirm_password']
            )

        #Save personal information
        PersonalInformation.objects.create(
                user=user,
                country=form_data['country'],
                state=form_data['state_province_region'],
                city=form_data['city'],
                zip_code=form_data['zip_postal_code'],
                profile_picture=form_data['profile_picture'],
                date_of_birth=form_data['date_of_birth'],
                gender=form_data['gender'],
                biography=form_data['biography'],
                portfolio=form_data['portfolio_website'],
                linkedin_profile=form_data['linkedin_profile']
        )

        #Save Educational background information
        EducationalBackground.objects.create(
            user=user,
            institution_name=form_data['institution_name'],
            institution_location=form_data['institution_location'],
            highest_educational_level=form_data['highest_education_level'],
            degree_title=form_data['degree_title'],
            institution_type=form_data['institution_type'],
            gpa_grade=form_data['gpa_grade'],
            internships_attended=form_data['internships_attended'],
            graduation_date=form_data['graduation_date'],
            field_of_study=form_data['field_of_study'],
            transcript=form_data['transcript'],
            thesis_title=form_data['thesis_title']
        )


        #Save work experience information
        WorkExperience.objects.create(
            user=user,
            job_title=form_data['job_title'],
            company_name=form_data['company_name'],
            company_location=form_data['company_location'],
            company_size=form_data['company_size'],
            company_type=form_data['company_type'],
            employment_type=form_data['employment_type'],
            industry=form_data['industry'],
            role_description=form_data['role_description'],
            job_duration=form_data['job_duration'],
            reason_for_leaving=form_data['reason_for_leaving']
        )

        #Save career preferences information
        CareerPreferences.objects.create(
            user=user,
            desired_job_title=form_data['desired_job_title'],
            preferred_industry=form_data['preferred_industry'],
            desired_company_type=form_data['desired_company_type'],
            desired_company_size=form_data['desired_company_size'],
            desired_job_location=form_data['desired_job_location'],
            preferred_employment_type=form_data['preferred_employment_type'],
            desired_job_role=form_data['desired_job_role'],
            expected_salary=form_data['expected_salary'],
            resume=form_data['upload_resume']
        )

        return redirect('verify_email')

def apply_page(request):
    return render(request, 'employee-portal/apply.html')

def job_details(request):
    return render(request, 'employee-portal/job-details.html')

def employer_profile(request):
    return render(request, 'employee-portal/employer-profile.html')