from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from employee_portal.models import *
from django.db.models import Avg


@receiver(post_save, sender=CandidateRatingAndReview)
def update_candidate_average_rating(sender, instance, created, **kwargs):
	if created:
		average_rating = CandidateRatingAndReview.objects.filter(candidate=instance.candidate).aggregate(average=Avg('rating'))['average']

		candidate = PersonalInformation.objects.get(user=instance.candidate.user)
		candidate.average_rating = average_rating
		candidate.save()