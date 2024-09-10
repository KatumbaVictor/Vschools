from django import forms


class AccountTypeForm(forms.Form):
    ACCOUNT_CHOICES = [('employer', 'Employer'),
                        ('job_seeker', 'Job Seeker')
                ]

    account_type = forms.ChoiceField(choices=ACCOUNT_CHOICES, widget=forms.RadioSelect, required=True)  