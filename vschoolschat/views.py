from django.shortcuts import render
from main.models import account_info
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required(login_url='login')
def chat_page(request, user_token):
    #profile_picture = account_info.objects.get(user=request.user).profile_picture
	context = {'profile_picture':account_info.objects.get(user=request.user).profile_picture,
				'username':account_info.objects.get(user=request.user).username,
				'user_token':user_token}
	return render(request, 'chat.html', context)

@login_required(login_url='login')
def search_page(request):
	return render(request, 'search.html')

def getUser(request):
	data = request.GET
	users = account_info.objects.filter(username__contains=data['name'])
	response = list(users.values())

	for item in response:
		item['profile_picture'] = account_info.objects.get(id=item['id']).profile_picture.url

	return JsonResponse(response, safe=False)

def guest_page(request):
	context = {}

	if request.user.is_authenticated:
		context['user_token'] = account_info.objects.get(user=request.user).user_token

	return render(request, 'dialogue.html', context)