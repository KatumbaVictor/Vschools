from django.shortcuts import render
from main.models import account_info
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required(login_url='login')
def chat_page(request, user_token):
    #profile_picture = account_info.objects.get(user=request.user).profile_picture
	context = {'profile_picture':account_info.objects.get(user=request.user).profile_picture,
				'username':account_info.objects.get(user=request.user).username,
				'user_token':account_info.objects.get(user=request.user).user_token}
	return render(request, 'chat.html', context)