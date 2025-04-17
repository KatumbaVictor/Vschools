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

    def __str__(self):
        return self.username


class JobApplication(models.Model):
    class Status(models.TextChoices):
        PENDING = "Pending", "Pending"
        REVIEWED = "Reviewed", "Reviewed"
        INTERVIEW = "Interview Scheduled", "Interview Scheduled"
        SHORTLISTED = "Shortlisted", "Shortlisted"
        REJECTED = "Rejected", "Rejected"

    job = models.ForeignKey(JobDetails, on_delete=models.CASCADE)
    candidate = models.ForeignKey('employee_portal.PersonalInformation', on_delete=models.CASCADE)
    status = models.CharField(max_length=30, choices=Status.choices, default=Status.PENDING)
    applied_at = models.DateTimeField(auto_now_add=True) 

    class Meta:
        unique_together = ('job', 'candidate')

    def __str__(self):
        return f"{self.user.username} - {self.job.job_title} ({self.status})" 
  

class JobInterview(models.Model):
    job_application = models.ForeignKey(JobApplication, on_delete=models.CASCADE)
    interview_title = models.CharField(max_length=255)
    interview_description = models.TextField(blank=True, null=True)
    interviewer_name = models.CharField(max_length=200)
    interviewer_email = models.EmailField()  
    interview_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    TIMEZONE_CHOICES = [(tz, tz) for tz in pytz.common_timezones]

    timezone = models.CharField(max_length=50, choices=TIMEZONE_CHOICES, default='UTC')

    attachment = models.FileField(upload_to='interview_attachments/', null=True, blank=True)
    attachment_description = models.TextField()

    candidate_confirmation = models.BooleanField(default=False)
    candidate_confirmation_deadline = models.DateTimeField()
    candidate_confirmed_at = models.DateTimeField(null=True, blank=True)

    class InterviewStatus(models.TextChoices):
        SCHEDULED = "scheduled","Scheduled"
        RESCHEDULED = "rescheduled", "Rescheduled"
        COMPLETED = "completed", "Completed"
        CANCELLED = "cancelled", "Cancelled"

    status = models.CharField(max_length=20, choices=InterviewStatus.choices, default=InterviewStatus.SCHEDULED)

    created_at = models.DateTimeField(auto_now_add=True)