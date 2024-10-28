from django import forms
from django.core.exceptions import ValidationError
from django_countries.fields import CountryField


class CompanyInformationForm(forms.Form):
	company_name = forms.CharField(max_length=255, required=True)
	company_website = forms.URLField(required=True)
	company_type = forms.ChoiceField(
					choices=[
                        ('private','Private'),
                        ('public','Public'),
                        ('government','Government'),
                        ('non_profit','Non-Profit'),
                    ],
                    required=True
		)
	company_size = forms.ChoiceField(
					choices=[
                        ('small','1 - 50 employees'),
                        ('medium', '51 - 200 employees'),
                        ('large','201 - 500 employees'),
                        ('enterprise', '500+ employees'),
                    ] 
		)
	company_email = forms.EmailField(required=True)
	company_location = forms.CharField(required=True)
	company_linkedin = forms.URLField(required=True)
	industry = forms.ChoiceField(
                choices=[
                    ('tech','Technology'),
                    ('finance','Finance'),
                    ('healthcare','Healthcare'),
                    ('education','Education'),
                    ('manufacturing','Manufacturing'),
                ]
        )
	company_overview = forms.CharField(max_length=200, required=True)
	company_vision = forms.CharField(max_length=200, required=True)
	date_established = forms.CharField(max_length=200, required=True)




class BillingInformationForm(forms.Form):
	country = CountryField().formfield()
	billing_address_1 = forms.CharField(max_length=255)
	billing_address_2 = forms.CharField(max_length=255)
	billing_email = forms.EmailField(required=True)
	city = forms.CharField(max_length=100)
	state_province_region = forms.CharField(max_length=100)
	postal_code = forms.CharField(max_length=40)
	full_name_on_card = forms.CharField(max_length=255)
	card_number = forms.CharField(max_length=19, required=True)
	card_expiration = forms.CharField(max_length=5, required=True)
	cvv_number = forms.CharField(max_length=4, required=True)



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



class CompanyRepresentativeForm(forms.Form):
	first_name = forms.CharField(max_length=80, required=True)
	last_name = forms.CharField(max_length=80, required=True)
	email = forms.EmailField(required=True)
	linkedin_profile = forms.URLField(required=False)
	job_title = forms.CharField(max_length=80)
	department = forms.CharField(max_length=80)
	portfolio_website = forms.URLField(required=True)
	biography = forms.CharField(max_length=200)
	roles_responsibilities = forms.CharField(max_length=200)
