from celery import shared_task
from django.utils import timezone
from .models import JobDetails


@shared_task
def activate_scheduled_jobs():
    #Activate all jobs that are scheduled to be published now or earlier.

    now = timezone.now()

    JobDetails.objects.filter(status='scheduled', publish_date__lte=now).update(status='active')



@shared_task
def expire_jobs():
    now = timezone.now()
    JobDetails.objects.filter(status='active', expiry_date__lte=now)