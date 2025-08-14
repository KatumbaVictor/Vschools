from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Avg
from django.utils.text import slugify
from io import BytesIO
from django.core.files import File
from django.conf import settings
import segno
from employer_portal.models import *


@receiver(post_save, sender=CompanyRatingAndReview)
def update_company_average_rating(sender, instance, created, **kwargs):
    if created:
        average_rating = CompanyRatingAndReview.objects.filter(employer=instance.employer).aggregate(average=Avg('rating'))['average']

        employer = CompanyInformation.objects.get(user=instance.employer.user)
        employer.average_rating = average_rating
        employer.save()



@receiver(post_save, sender=JobDetails)
def generate_job_slug_and_qr_code(sender, instance, created, **kwargs):
    if created:
        base_slug = slugify(instance.job_title)
        slug = base_slug
        counter = 1

        while JobDetails.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1

        instance.slug = slug

        profile_url = f"{settings.META_SITE_DOMAIN}{instance.get_absolute_url()}"

        qr_code = segno.make(profile_url)

        buffer = BytesIO()
        filename = f"job_qr_{instance.slug}.png"
        qr_code.save(buffer, kind='png', scale=5)

        instance.qr_code.save(filename, File(buffer), save=False)

        instance.save(update_fields=['slug', 'qr_code'])



@receiver(post_save, sender=CompanyInformation)
def generate_company_slug(sender, instance, created, **kwargs):
    if created:
        base_slug = slugify(instance.company_name)
        slug = base_slug
        counter = 1

        while CompanyInformation.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1

        instance.slug = slug
        instance.save(update_fields=['slug'])