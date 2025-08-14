from django.contrib import admin
from employee_portal.models import *

# Register your models here.
admin.site.register(PersonalInformation)
admin.site.register(CareerPreferences)
admin.site.register(CandidateProfileView)
admin.site.register(CandidateRatingAndReview)
admin.site.register(SavedJob)
admin.site.register(CandidateEndorsement)