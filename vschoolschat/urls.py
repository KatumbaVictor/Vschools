from django.urls import path, include
from .views import * 

app_name = 'vschoolschat'

urlpatterns = [
	path('dialogue/<str:user_token>', chat_page),
	path('search/', search_page, name='search_user'),
	path('getUser/',getUser),
	path('webpush/', include('webpush.urls')),
	path('logout/', logout_view),
	path('', guest_page)
]