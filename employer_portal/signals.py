from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from employer_portal.models import *
from django.db.models import Avg


@receiver(post_save, sender=CompanyRatingAndReview)
def update_company_average_rating(sender, instance, created, **kwargs):
    if created:
        average_rating = CompanyRatingAndReview.objects.filter(employer=instance.employer).aggregate(average=Avg('rating'))['average']

        employer = CompanyInformation.objects.get(user=instance.employer.user)
        employer.average_rating = average_rating
        employer.save()