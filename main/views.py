from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.urls import reverse
from .forms import AccountTypeForm
from django_countries import countries
from django.contrib.auth.forms import AuthenticationForm
from .models import *


meta = {
        'url': 'https://careerconnect.com',
        'description': 'page description',
        'site_name':'Career Connect',
        'use_og': True,
        'use_twitter': True,
        'use_facebook': True,
        'use_schemaorg': True,
        'title':'Career connect home.',
        'locale':'en_US',
        'schemaorg_title': 'Career connect home page.',
        'object_type': 'website',
        'og_title':'Career connect home',
        'image': {
            'url':'https://careerconnect.com',
            'type':'some/mime',
            'width': 100,
            'height': 100,
            'alt': 'Career Connect Media'
        }
    }


def login_page(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request=request, username=username, password=password)

            if user is not None:
                login(request, user)
                print(user.account_type)
                if user.account_type == 'Employer':
                    return redirect('/employer-portal/home')
                else:
                    return redirect('/home')
            else:
                messages.error(request, 'Incorrect username or password, Please check your credentials and try again, If you continue to have trouble, consider resetting your password.')

    return render(request, 'login.html')

@login_required(login_url='login')
def settings_page(request):
    context = {'meta':meta}

    return render(request,"settings_page.html",context)

def handle_404(request, exception):
    return render(request, 'error-pages/404.html', status=404)

def handle_500(request):
    return render(request, 'error-pages/500.html', status=500)

def handle_403(request, reason=""):
    return render(request, 'error-pages/403.html', {"reason": reason}, status=403)

def verify_email_page(request):
    return render(request, 'verify_email_page.html')

def about_page(request):
    return render(request, 'about.html')

def terms_of_service(request):
    return render(request, 'terms_of_service.html')

def sign_up_page(request):
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == "POST":
        form = AccountTypeForm(request.POST)

        if form.is_valid():
            print(form.cleaned_data)
            account_type = form.cleaned_data['account_type']
            if account_type == 'employer':
                return redirect('/employer-portal/sign-up')
            else:
                return redirect('/employee-portal/sign-up')
    else:
        form = AccountTypeForm()

    context = {'form':AccountTypeForm()}

    return render(request, 'sign_up.html', context)


    return render(request,"sign_up.html")

@login_required(login_url='login')
def home_page(request):
    context = {'meta':meta}

    return render(request, "home.html", context) 

def billing_page(request):
    return render(request, 'settings-pages/billing.html')

def contact_page(request):
    context = {'meta':meta}
    return render(request, "contact.html", context)

def pricing_page(request):
    return render(request, 'pricing.html')

def FAQ_page(request):
    return render(request, 'FAQ.html')

def test_page(request):
    context = {'countries': countries}
    return render(request, "test.html", context)

def guest_page(request):
    return render(request, "guest.html")

def verify_email(request):
    return render(request, 'otp.html')


@login_required
def join_interview(request, interview_slug):
    interview = get_object_or_404(JobInterview, slug=interview_slug)

    context = {
        'interview': interview
    }

    return render(request, 'join-interview.html', context)