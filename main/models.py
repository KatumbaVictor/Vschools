from django.db import models
from django.contrib.auth.models import AbstractUser
from employer_portal.models import JobDetails


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
        OFFERED = "Offered", "Offered"
        REJECTED = "Rejected", "Rejected"

    job = models.ForeignKey(JobDetails, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=30, choices=Status.choices, default=Status.PENDING)
    applied_at = models.DateTimeField(auto_now_add=True) 

    class Meta:
        unique_together = ('job', 'user')

    def __str__(self):
        return f"{self.user.username} - {self.job.job_title} ({self.status})" 