from django.db import models
from django_countries.fields import CountryField
from django.contrib.auth import get_user_model

User = get_user_model()

class PersonalInformation(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	profile_picture = models.ImageField(upload_to="profile_pictures", blank=True, null=True)
	date_of_birth = models.DateField(blank=True, null=True)
	gender_choices = [
		('M', 'Male'),
		('F', 'Female')
	]
	gender = models.CharField(max_length=1, choices=gender_choices, blank=True, null=True)
	country = CountryField(blank_label='Select country', blank=True, null=True)
	state = models.CharField(max_length=255, blank=True, null=True, help_text="State/Province/Region")
	city = models.CharField(max_length=255, blank=True, null=True)
	zip_code = models.CharField(max_length=20, blank=True, null=True, help_text="Zip/Postal code")
	biography = models.TextField(blank=True, null=True, help_text="A short bio about yourself")
	portfolio = models.URLField(blank=True, null=True, help_text="Portfolio/Website URL")
	linkedin_profile = models.URLField(blank=True, null=True, help_text="Linkedin profile URL")

	def __str__(self):
		return self.username

class EducationalBackground(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='educations')
	institution_name = models.CharField(max_length=255)
	institution_location = CountryField(blank_label="Select Country", blank=True, null=True)

	EDUCATIONAL_LEVEL_CHOICES = [
		('high_school', 'High School'),
        ('associate', 'Associate Degree'),
        ('bachelor','Bachelor\'s Degree'),
        ('master', 'Master\'s Degree'),
        ('doctorate', 'Doctorate Degree')
	]

	highest_educational_level = models.CharField(max_length=50, choices=EDUCATIONAL_LEVEL_CHOICES)
	degree_title = models.CharField(max_length=255, blank=True, null=True)

	INSTITUTION_TYPE_CHOICES = [
        ('public','Public'),
        ('private', 'Private'),
        ('online', 'Online'),
        ('vocational', 'Vocational')
    ]

	institution_type = models.CharField(max_length=50, choices=INSTITUTION_TYPE_CHOICES)
	gpa_grade = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
	internships_attended = models.TextField(blank=True, null=True, help_text="List the internships attended")
	graduation_date = models.DateField(blank=True, null=True)
	field_of_study = models.CharField(max_length=255, blank=True, null=True)
	transcript = models.FileField(upload_to='transcripts/', blank=True, null=True)
	thesis_title = models.CharField(max_length=255, blank=True, null=True)


class WorkExperience(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='work_experiences')
	job_title = models.CharField(max_length=255)
	company_name = models.CharField(max_length=255)
	company_location = CountryField(blank_label="(Select County)", blank=True, null=True)

	COMPANY_SIZE_CHOICES = [
        ('small','1 - 50 employees'),
        ('medium', '51 - 200 employees'),
        ('large','201 - 500 employees'),
        ('enterprise', '500+ employees'),
    ]

	company_size = models.CharField(max_length=100, choices=COMPANY_SIZE_CHOICES)

	COMPANY_TYPE_CHOICES = [
        ('private','Private'),
        ('public','Public'),
        ('government','Government'),
        ('non_profit','Non-Profit'),
    ]

	company_type = models.CharField(max_length=50, choices=COMPANY_TYPE_CHOICES)

	EMPLOYMENT_TYPE_CHOICES = [
        ('full_time','Full-time'),
        ('part_time', 'Part-time'),
        ('contract','Contract'),
        ('internship','Internship'),
        ('freelance','Freelance'),
    ]

	employment_type = models.CharField(max_length=50, choices=EMPLOYMENT_TYPE_CHOICES)

	INDUSTRY_CHOICES = [
        ('tech','Technology'),
        ('finance','Finance'),
        ('healthcare','Healthcare'),
        ('education','Education'),
        ('manufacturing','Manufacturing'),
    ]

	industry = models.CharField(max_length=50, choices=INDUSTRY_CHOICES)
	role_description = models.TextField(blank=True, null=True)
	job_duration = models.CharField(max_length=255, blank=True, null=True)
	reason_for_leaving = models.TextField(blank=True, null=True)

	def __str__(self):
		return f"{self.job_title} at {self.company_name}"

class CareerPreferences(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='career_preferences')
	desired_job_title = models.CharField(max_length=255)

	PREFERRED_INDUSTRY_CHOICES = [
        ('tech','Technology'),
        ('finance','Finance'),
        ('healthcare','Healthcare'),
        ('education','Education'),
        ('manufacturing','Manufacturing'),
    ]

	preferred_industry = models.CharField(max_length=50, choices=PREFERRED_INDUSTRY_CHOICES)

	DESIRED_COMPANY_TYPE = [
        ('private','Private'),
        ('public','Public'),
        ('government','Government'),
        ('non_profit','Non-Profit'),
    ]

	desired_company_type = models.CharField(max_length=50, choices=DESIRED_COMPANY_TYPE)

	DESIRED_COMPANY_SIZE = [
        ('small','1 - 50 employees'),
        ('medium', '51 - 200 employees'),
        ('large','201 - 500 employees'),
        ('enterprise', '500+ employees'),
    ]	

	desired_company_size = models.CharField(max_length=50, choices=DESIRED_COMPANY_SIZE)
	desired_job_location = CountryField(blank_label='(Select Country)', blank=True, null=True)

	EMPLOYMENT_TYPE_CHOICES = [
		('full_time','Full-time'),
        ('part_time', 'Part-time'),
        ('contract','Contract'),
        ('internship','Internship'),
        ('freelance','Freelance'),
    ]

	preferred_employment_type = models.CharField(max_length=50, choices=EMPLOYMENT_TYPE_CHOICES)
	desired_job_role = models.CharField(max_length=255)
	expected_salary = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
	resume = models.FileField(upload_to='resumes/', blank=True, null=True)
	cover_letter = models.FileField(upload_to='cover_letters/', blank=True, null=True)

	def __str__(self):
		return f"{self.user.username} - Career Preferences"
