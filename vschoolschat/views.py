from django.shortcuts import render, redirect
from main.models import account_info
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from webpush import send_user_notification
from django.contrib.auth import authenticate, login, logout
from django_hosts.resolvers import reverse
from geopy.geocoders import Nominatim
import reverse_geocode as rg

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

def invite(request):
	return render(request, "invite_page.html")

def logout_view(request):
	logout(request)
	return redirect('login')

@login_required(login_url='login')
def fingerprint_page(request):
	user = account_info.objects.get(user=request.user)
	context = {'user':user}
	return render(request, 'fingerprint.html', context)

def faceid_page(request):
	return render(request, 'faceid.html')

def login_page(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        user = authenticate(request=request,username=request.POST['username'],password=request.POST['password'])
        
        if user is not None:
            if account_info.objects.get(user=user).email_verified:
                login(request, user)
                return redirect('home')
            else:
                return redirect('verify_email_page')
        else:
            messages.info(request, "<i class = 'fas fa-exclamation-circle'></i> Wrong log in details")

    return render(request, "login.html")

def reverse_geocode(request):
	if request.method == 'GET':
		latitude = request.GET['latitude']
		longitude = request.GET['longitude']

		geolocator = Nominatim(user_agent='vschoolschat')
		location = geolocator.reverse((f"{latitude}, {longitude}"), exactly_one=True)

		city = location.raw.get('address').get('city','')
		state = location.raw.get('address').get('state','')
		country = location.raw.get('address').get('country','')

		address = (f"{city}, {state}, {country}")

		return JsonResponse({'address':address})