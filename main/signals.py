from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import *
from django.db.models import Avg


@receiver(post_save, sender=JobRating)
def update_job_average_rating(sender, instance, created, **kwargs):
    if created:
        average_rating = JobRating.objects.filter(job=instance.job).aggregate(average=Avg('rating'))['average']

        job = JobDetails.objects.get(job=instance.job)
        job.average_rating = average_rating
        job.save()