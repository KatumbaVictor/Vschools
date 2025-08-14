from django import forms
from django_countries.fields import CountryField
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django_ckeditor_5.widgets import CKEditor5Widget
from .models import *

User = get_user_model()


class AccountTypeForm(forms.Form):
    ACCOUNT_CHOICES = [('employer', 'Employer'),
                        ('job_seeker', 'Job Seeker')
                ]
 
    account_type = forms.ChoiceField(choices=ACCOUNT_CHOICES, widget=forms.RadioSelect, required=True)  


class PersonalInformationForm(forms.ModelForm):
    #User model fields
    first_name = forms.CharField(max_length=30, required=True, label="First name")
    last_name = forms.CharField(max_length=30, required=True, label="Last name")
    email = forms.EmailField(required=True, label="Email Address")
    password = forms.CharField(required=True, label="Password")
    confirm_password = forms.CharField(required=True ,label="Confirm Password")

    class Meta:
        model = PersonalInformation
        fields = [
            'profile_picture',
            'date_of_birth',
            'gender',
            'country',
            'state',
            'city',
            'zip_code',
            'biography',
            'skills',
            'portfolio',
            'linkedin_profile',
            'github_profile',
        ]

        widgets = {
            'biography': CKEditor5Widget(
                  attrs={"class": "django_ckeditor_5", 'placeholder':'Tell us about yourself (e.g., your background, passions, and career goals)'}, config_name="default"
              )
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match")


class EducationalBackgroundForm(forms.ModelForm):
    class Meta:
        model = EducationalBackground
        fields = [
            'institution_name',
            'institution_location',
            'highest_educational_level',
            'degree_title',
            'institution_type',
            'gpa_grade',
            'start_date',
            'graduation_date',
            'field_of_study',
            'transcript',
            'honors_or_awards',
            'certifications',
            'projects',
            'thesis_title',
        ]    


class WorkExperienceForm(forms.ModelForm):
    class Meta:
        model = WorkExperience
        fields = [
            'job_title',
            'company_name',
            'company_location',
            'company_size',
            'company_type',
            'employment_type',
            'industry',
            'role_description',
            'job_start_date',
            'job_end_date',
        ]  


class CareerPrefencesForm(forms.ModelForm):
    class Meta:
        model = CareerPreferences
        fields = [
            'desired_job_title',
            'preferred_industry',
            'desired_company_type',
            'desired_company_size',
            'desired_job_location',
            'preferred_employment_type',
            'desired_job_role',
            'minimum_salary',
            'maximum_salary',
            'resume',
            'cover_letter'
        ]