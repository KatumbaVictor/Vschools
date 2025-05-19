from django import forms
from allauth.account.forms import LoginForm
from django.core.exceptions import ValidationError
from .models import *

class AccountTypeForm(forms.Form):
    ACCOUNT_CHOICES = [('employer', 'Employer'),
                        ('job_seeker', 'Job Seeker')
                ]

    account_type = forms.ChoiceField(choices=ACCOUNT_CHOICES, widget=forms.RadioSelect, required=True)


class CustomLoginForm(LoginForm):
    def clean(self):
        try:
            super().clean()
        except ValidationError as e:
            raise ValidationError('The username or password is incorrect, please try again later')



class JobOfferForm(forms.ModelForm):
    class Meta:
        model = JobOffer
        fields = [
            'offer_title',
            'message',
            'expiry_date'
        ]

