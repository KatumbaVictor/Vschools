from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.views.decorators.http import require_POST
from django.urls import reverse
from .forms import *
from django_countries import countries
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse
from employer_portal.models import *
from employee_portal.models import *
from .models import *


@require_POST
@login_required
def endorse_candidate(request, candidate_slug):
    endorser = request.user.profile_instance
    candidate = get_object_or_404(PersonalInformation, slug=candidate_slug)  
    endorsement_form = CandidateEndorsementForm(request.POST)

    if endorsement_form.is_valid():
        endorsement = endorsement_form.save(commit=False)
        endorsement.candidate = candidate
        endorsement.endorser_content_type = ContentType.objects.get_for_model(type(endorser))
        endorsement.endorser_object_id = endorser.id

        endorsement.save()

        return JsonResponse({'success': True, 'message': 'Endorsement submitted successfully'})
    else:
        endorsement_form = CandidateEndorsementForm()
        print(endorsement_form.errors)
        return JsonResponse({'success': False, 'errors': endorsement_form.errors}, status=400)


@login_required(login_url='login')
def settings_page(request):
    return render(request,"settings_page.html")

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
    return render(request, "test.html")

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