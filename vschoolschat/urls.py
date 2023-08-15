from django.urls import path, include
from .views import * 

app_name = 'vschoolschat'

urlpatterns = [
	path('dialogue/<str:user_token>', chat_page),
	path('search/', search_page, name='search_user'),
	path('getUser/',getUser),
	path('webpush/', include('webpush.urls')),
	path('invite/', invite),
	path('logout/', logout_view),
	path('login/',login_page, name = "login"),
	path('', guest_page, name = 'home')
]