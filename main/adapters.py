from allauth.account.adapter import DefaultAccountAdapter
from django.shortcuts import resolve_url

class LoginRedirectAccountAdapter(DefaultAccountAdapter):
	def get_login_redirect_url(self, request):
		user = request.user
		if user.is_authenticated:
			if user.account_type == 'Employer':
				return resolve_url('employer_portal:home')
			elif user.account_type == 'Employee':
				return resolve_url('employee_portal:job_listings')

		return super().get_login_redirect_url(request)