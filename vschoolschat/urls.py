from django.urls import path
from .views import * 

app_name = 'vschoolschat'

urlpatterns = [
	path('dialogue/<str:user_token>', chat_page),
]