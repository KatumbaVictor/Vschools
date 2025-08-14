from django.db import models
from django.db.models import Count
from django.conf import settings
from django_countries.fields import CountryField
from moneyed import list_all_currencies
from django.utils.text import slugify
from meta.models import ModelMeta
import json


class CompanyInformation(models.Model):
    user = models.OneToOneField('main.User', on_delete=models.CASCADE)
    company_name = models.CharField(max_length=255)
    company_website = models.URLField(max_length=255, blank=True, null=True)

    COMPANY_TYPE_CHOICES = [
        ('private','Private'),
        ('public','Public'),
        ('government','Government'),
        ('non_profit','Non-Profit'),
    ]

    company_type = models.CharField(max_length=50, choices=COMPANY_TYPE_CHOICES)

    COMPANY_SIZE_CHOICES = [
        ('small','1 - 50 employees'),
        ('medium', '51 - 200 employees'),
        ('large','201 - 500 employees'),
        ('enterprise', '500+ employees'),
    ]

    company_size = models.CharField(max_length=50, choices=COMPANY_SIZE_CHOICES)
    company_profile_picture = models.ImageField(upload_to="profile_pictures", blank=True, null=True)
    company_email = models.EmailField(max_length=255, blank=True, null=True)
    country = CountryField(blank_label='Select country', blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True, help_text="State/Province/Region")
    city = models.CharField(max_length=255, blank=True, null=True)
    company_linkedin = models.URLField(max_length=255, blank=True, null=True)

    INDUSTRY_CHOICES = [
        ('tech','Technology'),
        ('finance','Finance'),
        ('healthcare','Healthcare'),
        ('education','Education'),
        ('manufacturing','Manufacturing'),
    ]

    industry = models.CharField(max_length=255, choices=INDUSTRY_CHOICES)
    biography = models.TextField(blank=True, null=True)
    company_overview = models.TextField()
    company_vision = models.TextField()
    date_established = models.DateField()
    slug = models.SlugField(unique=True, blank=True, null=True)
    average_rating = models.FloatField(default=0.0)

    def __str__(self):
        return self.company_name



class AccountRepresentative(models.Model):
    user = models.OneToOneField('main.User', on_delete=models.CASCADE)
    company = models.ForeignKey('CompanyInformation', on_delete=models.CASCADE, related_name='representatives')
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    linkedin_profile = models.URLField(max_length=255, blank=True, null=True)
    job_title = models.CharField(max_length=255)
    department = models.CharField(max_length=255)
    portfolio_website = models.URLField(max_length=255, blank=True, null=True)
    biography = models.TextField()
    roles_responsibilities = models.TextField()

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.job_title})"


class BillingInformation(models.Model):
    user = models.OneToOneField('main.User', on_delete=models.CASCADE, related_name='billing_information')
    company = models.ForeignKey('CompanyInformation', on_delete=models.CASCADE, related_name='billing_information')
    country = CountryField(blank_label='Select country', blank=True, null=True)
    billing_address_1 = models.CharField(max_length=255)
    billing_address_2 = models.CharField(max_length=255, blank=True, null=True)
    billing_email = models.EmailField(max_length=255)
    city = models.CharField(max_length=255)
    state_province_region = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=20)
    full_name_on_card = models.CharField(max_length=255)
    card_number = models.CharField(max_length=16)
    card_expiration = models.CharField(max_length=5)
    cvv_number = models.CharField(max_length=3)

    def __str__(self):
        return f"Billing Information for {self.user.username}"


class JobDetails(models.Model, ModelMeta):
    company = models.ForeignKey(CompanyInformation, on_delete=models.CASCADE, related_name='jobs')
    job_title = models.CharField(max_length=200)
    country = CountryField()
    state_or_region = models.CharField(max_length=200)
    qr_code = models.ImageField(upload_to="job_qr_codes", blank=True, null=True)

    EMPLOYMENT_TYPE_CHOICES = [
        ('full_time','Full-time'),
        ('part_time', 'Part-time'),
        ('contract','Contract'),
        ('apprenticeship','Apprenticeship'),
        ('freelance','Freelance'),
        ('returnship','Returnship'),
    ]

    employment_type = models.CharField(max_length=100, choices=EMPLOYMENT_TYPE_CHOICES)
    company_department = models.CharField(max_length=200)

    INDUSTRY_CHOICES = [
        ('tech','Technology'),
        ('finance','Finance'),
        ('healthcare','Healthcare'),
        ('education','Education'),
        ('manufacturing','Manufacturing'),
    ]

    industry = models.CharField(max_length=200, choices=INDUSTRY_CHOICES)
    job_description = models.TextField()
    key_responsibilities = models.JSONField(null=True, help_text='Describe key responsibilities and duties')

    WORK_MODES = [
        ('ONSITE','On-site'),
        ('REMOTE','Remote'),
        ('HYBRID','Hybrid'),
    ]

    work_location_mode = models.CharField(max_length=10, choices=WORK_MODES)

    SENIORITY_LEVELS = [
        ('JR','Junior'),
        ('MD','Mid-level'),
        ('SR','Senior'),
        ('LD','Leadership'),
    ]

    seniority_level = models.CharField(max_length=2, choices=SENIORITY_LEVELS)
    job_description_document = models.FileField(upload_to='job_descriptions/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True)

    JOB_STATUS_CHOICES = [
        ('active', 'Active'),
        ('closed', 'Closed'),
        ('expired', 'Expired'),
        ('paused', 'Paused'),
        ('draft', 'Draft')
    ]

    status = models.CharField(max_length=10, choices=JOB_STATUS_CHOICES, default='active')
    average_rating = models.FloatField(default=0.0)
    slug = models.SlugField(unique=True, blank=True, null=True)

    _metadata = {
        "use_title_tag": True,
        "use_schemaorg": True,
        "use_twitter": True,
        "use_og": True,
        "use_facebook": True,
        "site_name": "CareerConnect",
        "title": "get_meta_title",
        "description": "get_meta_description",
        "keywords": "get_meta_keywords",
        "og_type": "article",
        "url": "get_absolute_url",
    }

    _schema = {
        "use_title_tag": True,
        "use_schemaorg": True,
        "use_twitter": True,
        "use_og": True,
        "use_facebook": True,
        "site_name": "CareerConnect",
        "title": "get_meta_title",
        "description": "get_meta_description",
        "keywords": "get_meta_keywords",
        "og_title": "get_meta_title",
        "og_description": "get_meta_description",
        "og_type": "article",
        "twitter_card": "summary_large_image",
        "twitter_title": "get_meta_title",
        "twitter_description": "get_meta_description",
        "schemaorg_title": "get_meta_title",
        "url": "get_absolute_url",
    }

    def get_meta_title(self):
        return f"{self.job_title} at {self.company.company_name} - {self.country}"

    def get_meta_description(self):
        return f"Apply for {self.job_title} at {self.company.company_name} in {self.country}, Industry: {self.industry}, Employment Type: {self.employment_type}"

    def get_meta_keywords(self):
        return [self.job_title, self.company.company_name, self.country, self.industry, self.employment_type, 'jobs', 'hiring']

    def get_absolute_url(self):
        return f"/employee-portal/job-details/{self.slug}/"

    def get_schema_org(self):
        schema_data = {
            "@context": "https://schema.org",
            "@type": "JobPosting",
            "title": self.job_title,
            "hiringOrganization": {
                "@type": "Organization",
                "name": self.company.company_name
            },
            "jobLocation": {
                '@type': 'Place',
                'address': {
                '@type': "PostalAddress",
                "addressLocality": self.country
                }
            }
        }

        return json.dumps(schema_data, indent=4)

    def rating_percentages(self):
        rating_counts = self.job_ratings.values('rating').annotate(count=Count('rating'))

        total_ratings = self.job_ratings.aggregate(total=Count('id'))['total'] or 0

        percentages = {str(i): 0.0 for i in range(5, 0, -1)}

        if total_ratings > 0:
            for rating_data in rating_counts:
                rating_value = str(rating_data['rating'])
                count = rating_data['count']
                percentage = (count / total_ratings) * 100
                percentages[rating_value] = round(percentage, 2)

        return percentages

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.job_title	


class JobRequirements(models.Model):
    job_post = models.OneToOneField(JobDetails, on_delete=models.CASCADE, related_name='job_requirements')

    EDUCATIONAL_LEVEL_CHOICES = [
        ('none', 'No Formal Education'),
        ('high_school', 'High School'),
        ('associate', 'Associate Degree'),
        ('bachelor','Bachelor\'s Degree'),
        ('master', 'Master\'s Degree'),
        ('doctorate', 'Doctorate Degree (PhD)'),
        ('professional', 'Professional Certification'),
    ]

    minimum_education_level = models.CharField(max_length=100, choices=EDUCATIONAL_LEVEL_CHOICES)
    field_of_study = models.CharField(max_length=200, blank=True, null=True)
    certifications_and_licenses = models.JSONField(blank=True, help_text='List certifications/licenses seperated by commas')
    required_skills = models.JSONField(help_text='Describe required skills', blank=True, null=True)

    AGE_RANGE_CHOICES = [
        ('none', 'No age preference'),
        ('18-25', '18-25 years'),
        ('26-35', '26-35 years'),
        ('36-45', '36-45 years'),
        ('46-60', '46-60 years'),
        ('60+', '60+ years'),
    ]

    age_requirements = models.CharField(max_length=20, choices=AGE_RANGE_CHOICES, default='none')
    languages_required = models.CharField(max_length=255, help_text="Specify the required languages seperated by commas")

    LANGUAGE_PROFICIENCY_CHOICES = [
        ('basic', 'Basic'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
        ('native', 'Native'),
    ]

    language_proficiency = models.CharField(max_length=50, choices=LANGUAGE_PROFICIENCY_CHOICES, blank=True)
    additional_requirements = models.JSONField(blank=True, null=True, help_text='Enter additional requirements')


    GENDER_CHOICES = [
        ('any', 'Any'),
        ('male', 'Male'),
        ('female', 'Female'),
    ]

    gender_preferences = models.CharField(max_length=50, choices=GENDER_CHOICES, default='any')

    class RequiredRating(models.TextChoices):
        NONE = 'none', 'No rating required'
        ONE_STAR = '1', '1 Star & Above'
        TWO_STAR = '2', '2 Stars & Above'
        THREE_STARS = '3', '3 Stars & Above'
        FOUR_STARS = '4', '4 Stars & Above'
        FIVE_STARS = '5', '5 Stars Only'

    required_rating = models.CharField(max_length=10, choices=RequiredRating.choices, default=RequiredRating.NONE, help_text='Minimum candidate rating required for this job.')

    required_experience = models.PositiveIntegerField(help_text='Specify required years of experience')


class CompensationDetails(models.Model):
    job_post = models.OneToOneField(JobDetails, on_delete=models.CASCADE, related_name='compensation_details')
    minimum_salary = models.DecimalField(max_digits=10, decimal_places=2, help_text='Enter the minimum salary')
    maximum_salary = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, help_text='Enter the maximum salary (if applicable)')

    PAYMENT_CURRENCY_CHOICES = [(item.code, item.name) for item in list_all_currencies()]

    payment_currency = models.CharField(max_length=100, choices=PAYMENT_CURRENCY_CHOICES, help_text='Enter payment currency', default='USD')

    PAYMENT_FREQUENCY_CHOICES = [
        ('hourly', 'Hourly'),
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('biweekly', 'Bi-weekly'),
        ('monthly', 'Monthly'),
        ('annually', 'Annually'),
    ]

    payment_frequency = models.CharField(max_length=50, choices=PAYMENT_FREQUENCY_CHOICES, default='monthly')

    COMPENSATION_TYPE_CHOICES = [
        ('fixed', 'Fixed'),
        ('commission', 'Commission-based'),
        ('bonus', 'Bonus'),
        ('hybrid', 'Hybrid (Fixed + Commission/Bonus)'),
    ]

    compensation_type = models.CharField(max_length=50, choices=COMPENSATION_TYPE_CHOICES, default='fixed')
    benefits_and_incentives = models.TextField(blank=True, help_text='List non-monetary benefits separated by commas.')

    SALARY_NEGOTIABILITY_CHOICES = [
        ('non_negotiable', 'Non-negotiable'),
        ('negotiable', 'Negotiable'),
    ]

    salary_negotiability = models.CharField(max_length=50, choices=SALARY_NEGOTIABILITY_CHOICES, default='non_negotiable')

    def __str__(self):
        return f"Compensation for {self.job_post.job_title}"



class ApplicationDetails(models.Model):
    job_post = models.OneToOneField(JobDetails, on_delete=models.CASCADE, related_name='job_application_details')
    application_start_date = models.DateField(help_text='Date when applications open.')
    application_deadline = models.DateField(help_text='Date when applications close.')
    application_limit = models.PositiveIntegerField(blank=True, null=True, help_text='Maximum number of applications (leave blank for no limit).')
    contact_information = models.TextField(help_text='Contact details for inquiries (e.g., email, phone).')
    application_instructions = models.TextField(blank=True, help_text='Specific instructions for applicants.')
    custom_application_url = models.URLField(blank=True, null=True, help_text='Custom URL for external application submission.')

    def __str__(self):
    	return f"Application details for {self.job_post.job_title}"

    class Meta:
    	verbose_name = "Application Details"
    	verbose_name_plural = "Application Details"


class InternshipDetails(models.Model):
    company = models.ForeignKey(CompanyInformation, on_delete=models.CASCADE, related_name='internships')
    internship_title = models.CharField(max_length=200)
    country = CountryField()

    INDUSTRY_CHOICES = [
        ('tech','Technology'),
        ('finance','Finance'),
        ('healthcare','Healthcare'),
        ('education','Education'),
        ('manufacturing','Manufacturing'),
    ]

    industry = models.CharField(max_length=255, choices=INDUSTRY_CHOICES)
    company_department = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()

    INTERNSHIP_CHOICES = [
        ('FT', 'Full-Time Internship'),
        ('PT', 'Part-Time Internship'),
    ]
    
    internship_type = models.CharField(max_length=100, choices=INTERNSHIP_CHOICES)
    working_hours = models.CharField(max_length=255)
    internship_description = models.TextField()
    key_responsibilities = models.TextField(help_text='Describe key responsibilities and duties')
    internship_description_document = models.FileField(upload_to='internship_descriptions/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True)

    INTERNSHIP_STATUS_CHOICES = [
        ('active', 'Active'),
        ('closed', 'Closed'),
        ('expired', 'Expired'),
        ('paused', 'Paused'),
        ('draft', 'Draft')
    ]

    status = models.CharField(max_length=10, choices=INTERNSHIP_STATUS_CHOICES, default='active')
    slug = models.SlugField(unique=True, blank=True, null=True)

    def __str__(self):
        return self.internship_title   


class InternshipEligibilityCriteria(models.Model):
    internship = models.OneToOneField(InternshipDetails, on_delete=models.CASCADE, related_name='internship_details')

    EDUCATIONAL_LEVEL_CHOICES = [
        ('high_school', 'High School'),
        ('associate', 'Associate Degree'),
        ('bachelor','Bachelor\'s Degree'),
        ('master', 'Master\'s Degree'),
        ('doctorate', 'Doctorate Degree')
    ]

    education_level = models.CharField(max_length=100, choices=EDUCATIONAL_LEVEL_CHOICES)
    field_of_study = models.CharField(max_length=200, blank=True)
    certifications_and_licenses = models.TextField(blank=True, null=True, help_text='List certifications/licenses seperated by commas')

    AGE_RANGE_CHOICES = [
        ('none', 'No age preference'),
        ('18-25', '18-25 years'),
        ('26-35', '26-35 years'),
        ('36-45', '36-45 years'),
        ('46-60', '46-60 years'),
        ('60+', '60+ years'),
    ]

    age_requirements = models.CharField(max_length=20, choices=AGE_RANGE_CHOICES, default='none')
    languages_required = models.CharField(max_length=255, help_text="Specify the required languages seperated by commas")

    LANGUAGE_PROFICIENCY_CHOICES = [
        ('basic', 'Basic'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
        ('native', 'Native'),
    ]

    language_proficiency = models.CharField(max_length=50, choices=LANGUAGE_PROFICIENCY_CHOICES, blank=True)

    GENDER_CHOICES = [
        ('any', 'Any'),
        ('male', 'Male'),
        ('female', 'Female'),
    ]

    gender_preferences = models.CharField(max_length=50, choices=GENDER_CHOICES, default='any')
    required_experience = models.PositiveIntegerField(help_text='Specify required years of experience')
    required_skills = models.TextField(help_text='Describe required skills', blank=True, null=True)

    def __str__(self):
        return f"Eligibility Criteria for {self.internship.internship_title}"


class InternshipCompensationDetails(models.Model):
    internship = models.OneToOneField(InternshipDetails, on_delete=models.CASCADE, related_name='internship_compensation_details')
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    PAYMENT_CURRENCY_CHOICES = [(item.code, item.name) for item in list_all_currencies()]

    payment_currency = models.CharField(max_length=100, choices=PAYMENT_CURRENCY_CHOICES, help_text='Enter payment currency', default='USD')

    PAYMENT_FREQUENCY_CHOICES = [
        ('hourly', 'Hourly'),
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('biweekly', 'Bi-weekly'),
        ('monthly', 'Monthly'),
        ('annually', 'Annually'),
    ]

    payment_frequency = models.CharField(max_length=50, choices=PAYMENT_FREQUENCY_CHOICES, default='monthly')

    COMPENSATION_TYPE_CHOICES = [
        ('fixed', 'Fixed'),
        ('commission', 'Commission-based'),
        ('bonus', 'Bonus'),
        ('hybrid', 'Hybrid (Fixed + Commission/Bonus)'),
    ]

    compensation_type = models.CharField(max_length=50, choices=COMPENSATION_TYPE_CHOICES, default='fixed')
    benefits_and_incentives = models.TextField(blank=True, help_text='List non-monetary benefits separated by commas.')
    non_monetary_benefits = models.TextField(blank=True, help_text='List non-monetary benefits separated by commas.')

    SALARY_NEGOTIABILITY_CHOICES = [
        ('non_negotiable', 'Non-negotiable'),
        ('negotiable', 'Negotiable'),
    ]

    salary_negotiability = models.CharField(max_length=50, choices=SALARY_NEGOTIABILITY_CHOICES, default='non_negotiable')

    def __str__(self):
        return f"Internship compensation details for {self.internship.internship_title}"


class InternshipApplicationDetails(models.Model):
    internship = models.OneToOneField(InternshipDetails, on_delete=models.CASCADE, related_name='internship_application_details')
    application_start_date = models.DateField(help_text='Date when applications open.')
    application_deadline = models.DateField(help_text='Date when applications close.')
    application_limit = models.PositiveIntegerField(blank=True, null=True, help_text='Maximum number of applications (leave blank for no limit).')
    contact_information = models.TextField(help_text='Contact details for inquiries (e.g., email, phone).')
    application_instructions = models.TextField(blank=True, help_text='Specific instructions for applicants.')
    custom_application_url = models.URLField(blank=True, null=True, help_text='Custom URL for external application submission.')

    def __str__(self):
        return f"Internship Application details for {self.internship.internship_title}"

    class Meta:
        verbose_name = "Internship Application Details"
        verbose_name_plural = "Internship Application Details"


class CompanyRatingAndReview(models.Model):
    class RatingChoices(models.IntegerChoices):
        ONE_STAR = 1, "Very Poor"
        TWO_STARS = 2, "Poor"
        THREE_STARS = 3, "Average"
        FOUR_STARS = 4, "Good"
        FIVE_STARS = 5, "Excellent"

    candidate = models.ForeignKey("employee_portal.PersonalInformation", on_delete=models.CASCADE)
    employer = models.ForeignKey(CompanyInformation, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(choices=RatingChoices.choices, default=RatingChoices.ONE_STAR)
    review_title = models.CharField(max_length=200, null=True, blank=True)
    review = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('candidate', 'employer')

    def __str__(self):
        return f"{self.candidate.user.username}  rated {self.employer.company_name} - {self.rating} Starts"



class SavedCandidate(models.Model):
    employer = models.ForeignKey(CompanyInformation, on_delete=models.CASCADE)
    candidate = models.ForeignKey('employee_portal.PersonalInformation', on_delete=models.CASCADE, related_name='saved_candidates')
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('employer', 'candidate')

    def __str__(self):
        return f"{self.employer.company_name} saved {self.candidate.user.username}"



class JobApplicationInvite(models.Model):
    employer = models.ForeignKey(CompanyInformation, on_delete=models.CASCADE)
    candidate = models.ForeignKey('employee_portal.PersonalInformation', on_delete=models.CASCADE)
    job = models.OneToOneField(JobDetails, on_delete=models.CASCADE)
    employer_message = models.TextField(blank=True, null=True)
    sent_at = models.DateTimeField(auto_now_add=True)
    viewed = models.BooleanField(default=False)
    viewed_at = models.DateTimeField(blank=True, null=True)
    deadline = models.DateTimeField()
    responded_at = models.DateTimeField(null=True, blank=True)

    class CandidateResponseChoices(models.TextChoices):
        PENDING = 'pending', 'Pending'
        ACCEPTED = 'accepted', 'Accepted'
        DECLINED = 'declined', 'Declined'
        EXPIRED = 'expired', 'Expired'

    candidate_response = models.CharField(max_length=25, choices=CandidateResponseChoices.choices, default=CandidateResponseChoices.PENDING)

    class Meta:
        unique_together = ('job', 'employer', 'candidate')

    def __str__(self):
        return f"{self.candidate} invited for {self.job}"

