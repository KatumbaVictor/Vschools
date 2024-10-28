from django.shortcuts import render, redirect
from formtools.wizard.views import SessionWizardView
from .forms import CompanyInformationForm, BillingInformationForm, AccountInformationForm, CompanyRepresentativeForm
from django.conf import settings
from django_countries import countries
from django.core.files.storage import FileSystemStorage
import os

Templates = {'company_information':'employer-portal/registration/company-information.html',
             'company_representative':'employer-portal/registration/company-representative.html',
             'billing_information':'employer-portal/registration/billing-information.html',
             'account_information':'employer-portal/registration/account-information.html'
        }


class CompanySignUpWizard(SessionWizardView):
    file_storage = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'media'))

    form_list = [
        ('company_information', CompanyInformationForm), 
        ('company_representative', CompanyRepresentativeForm),
        ('billing_information', BillingInformationForm),
        ('account_information', AccountInformationForm),
    ]

    def get_template_names(self):
        return [Templates[self.steps.current]]

    def get_context_data(self, form, **kwargs):
        context = super().get_context_data(form=form, **kwargs)

        if self.steps.current == 'billing_information':
            context['countries'] = countries

        return context

    def done(self, form_list, **kwargs):
        for form in form_list:
            print(form.cleaned_data)
        return redirect('verify_email')



def company_information(request):
    return render(request,"employer-portal/registration/company-information.html")


def employee_profile(request):
    return render(request, 'employer-portal/employee-profile.html')

def home_page(request):
    return render(request, 'employer-portal/home.html')

def post_job(request):
    return render(request, 'employer-portal/post-job.html')