from django import forms
from django_countries.fields import CountryField
from cities_light.models import City



class AccountTypeForm(forms.Form):
    ACCOUNT_CHOICES = [('employer', 'Employer'),
                        ('job_seeker', 'Job Seeker')
                ]

    account_type = forms.ChoiceField(choices=ACCOUNT_CHOICES, widget=forms.RadioSelect, required=True)    


class PersonalInformationForm(forms.Form):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    country = CountryField().formfield()
    state_province_region = forms.CharField(max_length=100)
    city = forms.CharField(max_length=200)
    zip_postal_code = forms.CharField(max_length=100)
    profile_picture = forms.FileField()
    date_of_birth = forms.DateField()

    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]
    gender = forms.ChoiceField(choices=GENDER_CHOICES)
    biography = forms.CharField(widget=forms.Textarea, required=False)
    portfolio_website = forms.URLField(required=False)
    linkedin_profile = forms.URLField(required=False)
    email = forms.EmailField()
    password = forms.CharField()
    confirm_password = forms.CharField()    

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and  confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")  



class EducationalBackgroundForm(forms.Form):
    institution_name = forms.CharField(max_length=100, required=True)
    institution_location = forms.CharField(max_length=100, required=True)
    highest_education_level = forms.ChoiceField(
                                choices=[
                                    ('high_school', 'High School'),
                                    ('associate', 'Associate Degree'),
                                    ('bachelor','Bachelor\'s Degree'),
                                    ('master', 'Master\'s Degree'),
                                    ('doctorate', 'Doctorate Degree')
                                ],
                                required=True
        )
    degree_title = forms.CharField(max_length=100, required=True)
    institution_type = forms.ChoiceField(
                        choices=[
                            ('public','Public'),
                            ('private', 'Private'),
                            ('online', 'Online'),
                            ('vocational', 'Vocational')
                        ],
                        required=True
        )
    gpa_grade = forms.DecimalField(max_digits=4, decimal_places=2, required=True)
    internships_attended = forms.CharField(max_length=400, required=True)
    graduation_date = forms.DateField(required=True)
    field_of_study = forms.CharField(max_length=100, required=True)
    transcript = forms.FileField(required=True)
    thesis_title = forms.CharField(max_length=200, required=False)    



class WorkExperienceForm(forms.Form):
    job_title = forms.CharField(max_length=100)
    company_name = forms.CharField(max_length=100)
    company_location = forms.CharField(max_length=100)
    company_size = forms.ChoiceField(
                    choices=[
                        ('small','1 - 50 employees'),
                        ('medium', '51 - 200 employees'),
                        ('large','201 - 500 employees'),
                        ('enterprise', '500+ employees'),
                    ]
        )
    company_type = forms.ChoiceField(
                    choices=[
                        ('private','Private'),
                        ('public','Public'),
                        ('government','Government'),
                        ('non_profit','Non-Profit'),
                    ]
        )
    employment_type = forms.ChoiceField(
                        choices=[
                            ('full_time','Full-time'),
                            ('part_time', 'Part-time'),
                            ('contract','Contract'),
                            ('internship','Internship'),
                            ('freelance','Freelance'),
                        ]
        )
    industry = forms.ChoiceField(
                choices=[
                    ('tech','Technology'),
                    ('finance','Finance'),
                    ('healthcare','Healthcare'),
                    ('education','Education'),
                    ('manufacturing','Manufacturing'),
                ]
        )
    role_description = forms.CharField(max_length=200)
    job_start_date = forms.DateField()
    job_end_date = forms.DateField()
    reason_for_leaving = forms.CharField(max_length=200)


class CareerPrefencesForm(forms.Form):
    desired_job_title = forms.CharField(max_length=100, required=True)
    preferred_industry = forms.ChoiceField(
                            choices=[
                                ('tech','Technology'),
                                ('finance','Finance'),
                                ('healthcare','Healthcare'),
                                ('education','Education'),
                                ('manufacturing','Manufacturing'),
                            ]
        )
    desired_company_type = forms.ChoiceField(
                            choices=[
                                ('private','Private'),
                                ('public','Public'),
                                ('government','Government'),
                                ('non_profit','Non-Profit'),
                            ],
                            required=True
        )
    desired_company_size = forms.ChoiceField(
                            choices=[
                                ('small','1 - 50 employees'),
                                ('medium', '51 - 200 employees'),
                                ('large','201 - 500 employees'),
                                ('enterprise', '500+ employees'),
                            ],
                            required=True
        )
    desired_job_location = forms.CharField(max_length=100, required=True)
    preferred_employment_type = forms.ChoiceField(
                                choices=[
                            ('full_time','Full-time'),
                            ('part_time', 'Part-time'),
                            ('contract','Contract'),
                            ('internship','Internship'),
                            ('freelance','Freelance'),
                        ]
        )
    desired_job_role = forms.CharField(max_length=100, required=True)
    expected_salary = forms.DecimalField(max_digits=10, decimal_places=2, required=True)
    upload_resume = forms.FileField(required=True)




