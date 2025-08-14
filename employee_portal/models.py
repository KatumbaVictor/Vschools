from django.db import models
from meta.models import ModelMeta
from django_countries.fields import CountryField
from django.contrib.auth import get_user_model
from django_ckeditor_5.fields import CKEditor5Field
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.conf import settings
from django.urls import reverse
from employer_portal.models import *

User = get_user_model()

class PersonalInformation(models.Model, ModelMeta):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to="profile_pictures", blank=True, null=True)
    cover_photo = models.ImageField(upload_to="profile_covers", blank=True, null=True, default="profile_covers/default_cover.png", help_text="Upload a professional cover photo (1200x300px recommended)")
    qr_code = models.ImageField(upload_to="candidate_qr_codes", blank=True, null=True)
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
    biography = CKEditor5Field('Biography', config_name='default', blank=True, null=True)
    skills = models.JSONField(default=list, help_text='Describe required skills', blank=True, null=True)
    portfolio = models.URLField(blank=True, null=True)
    linkedin_profile = models.URLField(blank=True, null=True, help_text="Linkedin profile URL")
    github_profile = models.URLField(blank=True, null=True, help_text="GitHub profile URL")
    slug = models.SlugField(unique=True, blank=True, null=True)
    average_rating = models.FloatField(default=0.0)

    _metadata = {
        "use_title_tag": True,
        "use_schemaorg": True,
        "use_twitter": True,
        "use_og": True,
        "use_facebook": True,
        'title': 'get_meta_title',
        'description': 'get_meta_description',
        'keywords': 'get_meta_keywords',
        'url': 'get_absolute_url'
    }


    def get_meta_title(self):
        return f"{self.user.get_full_name()} | Professional Candidate Profile | {settings.META_SITE_NAME}"

    def get_meta_description(self):
        return self.biography or f"Profile of {self.user.get_full_name()}, a professional job seeker."

    def get_meta_keywords(self):
        return [self.user.get_full_name(), 'candidate', 'job seeker']

    def get_absolute_url(self):
        return reverse('employer_portal:candidate_profile', args=[self.slug])


    def __str__(self):
        return f"{self.user.username}"


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
    start_date = models.DateField(blank=True, null=True)
    graduation_date = models.DateField(blank=True, null=True)
    field_of_study = models.CharField(max_length=255, blank=True, null=True)
    transcript = models.FileField(upload_to='transcripts/', blank=True, null=True)
    honors_or_awards = models.TextField(blank=True, null=True)
    certifications = models.TextField(blank=True, null=True)
    projects = models.TextField(blank=True, null=True)
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
    job_start_date = models.DateField()
    job_end_date = models.DateField()

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
    minimum_salary = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    maximum_salary = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    cover_letter = models.FileField(upload_to='cover_letters/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - Career Preferences"


class CandidateProfileView(models.Model):
    candidate = models.ForeignKey(PersonalInformation, on_delete=models.CASCADE, related_name='profile_views')
    viewed_by = models.ForeignKey("employer_portal.CompanyInformation", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['candidate', 'viewed_by', 'timestamp']
        ordering = ['-timestamp']


    def __str__(self):
        return f"{self.viewed_by.company_name} viewed {self.candidate.user.username} at {self.timestamp}"


class CandidateRatingAndReview(models.Model):
    class RatingChoices(models.IntegerChoices):
        ONE_STAR = 1, "Very Poor"
        TWO_STARS = 2, "Poor"
        THREE_STARS = 3, "Average"
        FOUR_STARS = 4, "Good"
        FIVE_STARS = 5, "Excellent"

    employer = models.ForeignKey("employer_portal.CompanyInformation", on_delete=models.CASCADE)
    candidate = models.ForeignKey(PersonalInformation, on_delete=models.CASCADE, related_name='candidate_ratings')
    rating = models.PositiveIntegerField(choices=RatingChoices.choices, default=RatingChoices.ONE_STAR)
    review_title = models.CharField(max_length=200, null=True, blank=True)
    review = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('employer', 'candidate')
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.employer.company_name} rated {self.candidate.user.username} - {self.rating} Starts"



class SavedJob(models.Model):
    candidate = models.ForeignKey(PersonalInformation, on_delete=models.CASCADE)
    job = models.ForeignKey('employer_portal.JobDetails', on_delete=models.CASCADE, related_name='saved_jobs')
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('candidate', 'job')
        ordering = ['saved_at']

    def __str__(self):
        return f"{self.candidate.user.username} saved {self.job.job_title}"



class CandidateEndorsement(models.Model):
    candidate = models.ForeignKey(PersonalInformation, on_delete=models.CASCADE, related_name='endorsements_received')
    endorser_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    endorser_object_id = models.PositiveIntegerField()
    endorser = GenericForeignKey('endorser_content_type', 'endorser_object_id')
    endorsement_text = models.TextField()
    relationship = models.CharField(max_length=200, help_text="E.g. Supervisor, Hiring Manager")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (('endorser_content_type', 'endorser_object_id', 'candidate'),)

    def __str__(self):
        return f"{self.endorser} endorsed {self.candidate}"