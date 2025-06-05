from django.db import models
from django.contrib.auth.models import AbstractUser
from employer_portal.models import JobDetails
import pytz


class User(AbstractUser):
    ACCOUNT_TYPES = [
        ('employee', 'Employee'),
        ('employer', 'Employer')
    ]
    account_type = models.CharField(max_length=10, choices=ACCOUNT_TYPES)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)

    def get_initials(self):
        first = self.first_name[:1] if self.first_name else ''
        last = self.last_name[:1] if self.last_name else ''

        if first and last:
            return f"{first}{last}".upper()
        else:
            return self.username[:2].upper()

    def __str__(self):
        return self.username


class JobApplication(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        REVIEWED = "reviewed", "Reviewed"
        INTERVIEW_SCHEDULED = "interview_scheduled", "Interview Scheduled"
        INTERVIEW_COMPLETED = "interview_completed", "Interview Completed"
        SHORTLISTED = "shortlisted", "Shortlisted"
        REJECTED = "rejected", "Rejected"

    job = models.ForeignKey(JobDetails, on_delete=models.CASCADE)
    candidate = models.ForeignKey('employee_portal.PersonalInformation', on_delete=models.CASCADE)
    company = models.ForeignKey('employer_portal.CompanyInformation', on_delete=models.CASCADE, null=True)
    status = models.CharField(max_length=30, choices=Status.choices, default=Status.PENDING)
    applied_at = models.DateTimeField(auto_now_add=True) 

    class Meta:
        unique_together = ('job', 'candidate')
        ordering = ["-applied_at"]

    def __str__(self):
        return f"{self.user.username} - {self.job.job_title} ({self.status})" 
  

class JobInterview(models.Model):
    company = models.ForeignKey("employer_portal.CompanyInformation", on_delete=models.CASCADE, null=True)
    candidate = models.ForeignKey('employee_portal.PersonalInformation', on_delete=models.CASCADE, null=True)
    job_application = models.ForeignKey(JobApplication, on_delete=models.CASCADE)
    interview_title = models.CharField(max_length=255)
    interview_description = models.TextField(blank=True, null=True)
    interviewer_name = models.CharField(max_length=200)
    interviewer_email = models.EmailField() 
    interviewer_job_role = models.CharField(max_length=255, null=True, blank=True)
    interviewer_linkedin_profile = models.URLField(blank=True, null=True, help_text="Linkedin profile URL")
    interviewer_github_profile = models.URLField(blank=True, null=True, help_text="GitHub profile URL")
    interview_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    TIMEZONE_CHOICES = [(tz, tz) for tz in pytz.common_timezones]

    timezone = models.CharField(max_length=50, choices=TIMEZONE_CHOICES, default='UTC')

    attachment = models.FileField(upload_to='interview_attachments/', null=True, blank=True)
    attachment_description = models.TextField()

    candidate_confirmation = models.BooleanField(default=False)
    candidate_confirmation_deadline = models.DateTimeField(null=True, blank=True)
    candidate_confirmed_at = models.DateTimeField(null=True, blank=True)

    class InterviewStatus(models.TextChoices):
        SCHEDULED = "scheduled","Scheduled"
        RESCHEDULED = "rescheduled", "Rescheduled"
        COMPLETED = "completed", "Completed"
        CANCELLED = "cancelled", "Cancelled"

    status = models.CharField(max_length=20, choices=InterviewStatus.choices, default=InterviewStatus.SCHEDULED)

    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, blank=True, null=True)

    class Meta:
        ordering = ["-created_at"]



class JobOffer(models.Model):
    company = models.ForeignKey("employer_portal.CompanyInformation", on_delete=models.CASCADE, related_name="sent_offers")
    candidate = models.ForeignKey('employee_portal.PersonalInformation', on_delete=models.CASCADE, related_name="received_offers")
    job = models.ForeignKey("employer_portal.JobDetails", on_delete=models.CASCADE)
    offer_title = models.CharField(max_length=255)
    message = models.TextField()
    offer_document = models.FileField(null=True, blank=True)

    class JobOfferStatus(models.TextChoices):
        PENDING = "pending", "Pending"
        ACCEPTED = "accepted", "Accepted"
        DECLINED = "declined", "Declined"
        EXPIRED = "expired", "Expired"

    status = models.CharField(max_length=10, choices=JobOfferStatus.choices, default=JobOfferStatus.PENDING)
    offer_date = models.DateTimeField(auto_now_add=True)
    expiry_date = models.DateTimeField()
    viewed_at = models.DateTimeField(null=True, blank=True)
    responded_at = models.DateTimeField(null=True, blank=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return f"{self.company.company_name} -> {self.candidate.user.username}: {self.offer_title}"


class JobView(models.Model):
    job = job = models.ForeignKey("employer_portal.JobDetails", on_delete=models.CASCADE, related_name='job_views')
    viewer = models.ForeignKey('employee_portal.PersonalInformation', on_delete=models.CASCADE, null=True, blank=True)
    viewed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('job', 'viewer')
        ordering = ['-viewed_at']

    def __str__(self):
        return f"{self.viewer.user.username} viewed {self.job.job_title} at {self.viewed_at}"



class JobShare(models.Model):
    job =  models.ForeignKey("employer_portal.JobDetails", on_delete=models.CASCADE, related_name='job_shares')
    shared_by = models.ForeignKey('employee_portal.PersonalInformation', on_delete=models.CASCADE, null=True, blank=True)
    shared_at = models.DateTimeField(auto_now_add=True)

    class SharePlatform(models.TextChoices):
        EMAIL = 'email', 'Email'
        FACEBOOK = 'facebook', 'Facebook'
        X = 'twitter', 'X'
        LINKEDIN = 'linkedin', 'LinkedIn'
        WHATSAPP = 'whatsapp', 'WhatsApp'
        OTHER = 'other', 'Other'

    platform = models.CharField(max_length=20, choices=SharePlatform.choices, default=SharePlatform.OTHER)

    def __str__(self):
        return f"{self.shared_by.user.username} shared {self.job.job_title} on {self.shared_at}"


class JobImpression(models.Model):
    job =  models.ForeignKey("employer_portal.JobDetails", on_delete=models.CASCADE, related_name='job_impressions')
    candidate = models.ForeignKey('employee_portal.PersonalInformation', on_delete=models.CASCADE, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('job', 'candidate')
        ordering = ["-timestamp"]

    def __str__(self):
        return f"Impression: {self.candidate.user.username} -> {self.job.job_title} at {self.timestamp}"



class JobRating(models.Model):
    job =  models.ForeignKey("employer_portal.JobDetails", on_delete=models.CASCADE, related_name='job_ratings')
    candidate = models.ForeignKey('employee_portal.PersonalInformation', on_delete=models.CASCADE)

    class JobRatingChoices(models.IntegerChoices):
        ONE_STAR = 1, "Very Poor"
        TWO_STARS = 2, "Poor"
        THREE_STARS = 3, "Average"
        FOUR_STARS = 4, "Good"
        FIVE_STARS = 5, "Excellent"

    rating = models.PositiveIntegerField(choices=JobRatingChoices.choices, default=JobRatingChoices.ONE_STAR)
    title = models.CharField(max_length=100)
    comment = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('job', 'candidate')
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.candidate} rated {self.job} {self.get_rating_display()}"