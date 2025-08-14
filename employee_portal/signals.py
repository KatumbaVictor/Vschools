from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from employee_portal.models import *
from main.models import *
from django.utils.text import slugify
from django.db.models import Avg
from django.conf import settings
from io import BytesIO
from django.core.files import File
import segno




@receiver(post_save, sender=CandidateRatingAndReview)
def update_candidate_average_rating(sender, instance, created, **kwargs):
	if created:
		average_rating = instance.objects.filter(candidate=instance.candidate).aggregate(average=Avg('rating'))['average']

		instance.candidate.average_rating = average_rating
		instance.candidate.save()



@receiver(post_save, sender=PersonalInformation)
def generate_slug_and_qr_code(sender, instance, created, **kwargs):
	if created:
		# Generate a unique slug for the new candidate's profile
		base_slug = slugify(f"{instance.first_name} {instance.last_name}")
		slug = base_slug
		counter = 1

		while PersonalInformation.objects.filter(slug=slug).exists():
			slug = f"{base_slug}-{counter}"
			counter += 1

		instance.slug = slug

		profile_url = f"{settings.META_SITE_DOMAIN}{instance.get_absolute_url()}"

		qr_code = segno.make(profile_url)

		buffer = BytesIO()
		filename = f"candidate_qr_{instance.slug}.png"
		qr_code.save(buffer, kind='png', scale=5)

		instance.qr_code.save(filename, File(buffer), save=False)

		instance.save(update_fields=['slug', 'qr_code'])



@receiver(post_save, sender=JobRating)
def update_job_average_rating(sender, instance, created, **kwargs):
	if created:
	    job = instance.job
	    # Aggregate average rating and total count
	    average_rating = instance.objects.filter(job=job).aggregate(average=Avg('rating'))['average']

	    instance.job.average_rating = average_rating
	    instance.job.save()