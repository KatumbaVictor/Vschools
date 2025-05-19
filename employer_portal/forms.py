from django import forms
from django.core.exceptions import ValidationError
from django_countries.fields import CountryField
from .models import *
from main.models import *


class CompanyInformationForm(forms.ModelForm):
	class Meta:
		model = CompanyInformation
		fields = [
			'company_name',
			'company_website',
			'company_type',
			'company_size',
			'company_profile_picture',
			'company_email',
			'country',
			'state',
			'city',
			'company_linkedin',
			'industry',
			'company_overview',
			'company_vision',
			'date_established'
		]


class BillingInformationForm(forms.ModelForm):
	class Meta:
		model = BillingInformation
		fields = [
			'country',
			'billing_address_1',
			'billing_address_2',
			'billing_email',
			'city',
			'state_province_region',
			'postal_code',
			'full_name_on_card',
			'card_number',
			'card_expiration',
			'cvv_number',
		]


class AccountInformationForm(forms.Form):
	first_name = forms.CharField(max_length=80, required=True)
	last_name = forms.CharField(max_length=80, required=True)
	email = forms.EmailField(required=True)
	password = forms.CharField(required=True)
	confirm_password = forms.CharField(required=True)

	def clean(self):
		cleaned_data = super().clean()
		password = cleaned_data.get('password')
		confirm_password = cleaned_data.get('confirm_password')

		if password != confirm_password:
			raise ValidationError('The passwords provided do not match')
		return cleaned_data


class CompanyRepresentativeForm(forms.ModelForm):
	class Meta:
		model = AccountRepresentative
		fields = [
			'first_name',
			'last_name',
			'email',
			'linkedin_profile',
			'job_title',
			'department',
			'portfolio_website',
			'biography',
			'roles_responsibilities',
		]


class JobDetailsForm(forms.ModelForm):
	class Meta:
		model = JobDetails
		fields = [
			'job_title',
			'country',
			'state_or_region',
			'employment_type',
			'company_department',
			'industry',
			'job_description',
			'key_responsibilities',
			'work_location_mode',
			'seniority_level',
			'job_description_document'
		]


class JobRequirementsForm(forms.ModelForm):
	class Meta:
		model = JobRequirements
		fields = [
			'minimum_education_level',
			'field_of_study',
			'certifications_and_licenses',
			'required_skills',
			'age_requirements',
			'languages_required',
			'language_proficiency',
			'gender_preferences',
			'required_experience',
			'additional_requirements',
			'required_rating',
		]

	

class CompensationDetailsForm(forms.ModelForm):
	class Meta:
		model = CompensationDetails
		fields = [
			'minimum_salary',
			'maximum_salary',
			'payment_currency',
			'payment_frequency',
			'compensation_type',
			'benefits_and_incentives',
			'salary_negotiability'
		]


class ApplicationDetailsForm(forms.ModelForm):
	class Meta:
		model = ApplicationDetails
		fields = [
			'application_start_date',
			'application_deadline',
			'application_limit',
			'contact_information',
			'application_instructions',
			'custom_application_url',
		]


class JobPostTermsAndConditionsForm(forms.Form):
	accept_terms = forms.BooleanField(required=True, error_messages={'required':'You must accept the terms and conditions to continue.'})


class InternshipDetailsForm(forms.ModelForm):
	class Meta:
		model = InternshipDetails
		fields = [
			'internship_title',
			'country',
			'industry',
			'company_department',
			'start_date',
			'end_date',
			'internship_type',
			'working_hours',
			'internship_description',
			'key_responsibilities',
			'internship_description_document'
		]


class InternshipEligibilityCriteriaForm(forms.ModelForm):
	class Meta:
		model = InternshipEligibilityCriteria
		fields = [
			'education_level',
			'field_of_study',
			'certifications_and_licenses',
			'age_requirements',
			'languages_required',
			'language_proficiency',
			'gender_preferences',
			'required_experience',
			'required_skills'
		]


class InternshipCompensationDetailsForm(forms.ModelForm):
	class Meta:
		model = InternshipCompensationDetails
		fields = [
			'payment_amount',
			'payment_currency',
			'payment_frequency',
			'compensation_type',
			'benefits_and_incentives',
			'non_monetary_benefits',
			'salary_negotiability'
		]


class InternshipApplicationDetailsForm(forms.ModelForm):
	class Meta:
		model = InternshipApplicationDetails
		fields = [
			'application_start_date',
			'application_deadline',
			'application_limit',
			'contact_information',
			'application_instructions',
			'custom_application_url'
		]



class JobInterviewForm(forms.ModelForm):
    class Meta:
        model = JobInterview
        fields = [
            'interview_title',
            'interview_description',
            'interviewer_name',
            'interviewer_email',
            'interview_date',
            'start_time',
            'end_time',
            'timezone',
            'attachment',
            'attachment_description',
        ]