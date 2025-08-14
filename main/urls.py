from django.urls import path
from .views import *


app_name = 'main'

urlpatterns = [
	path('endorse-candidate/<slug:candidate_slug>/', endorse_candidate, name="endorse_candidate"),
]