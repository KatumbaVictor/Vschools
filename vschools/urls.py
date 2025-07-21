"""vschools URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.views.generic import TemplateView
from django.contrib import admin
from django.urls import path, include, re_path
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings
#from machina import urls as machina_urls
import machina
from main.views import *

from django.contrib.sitemaps.views import sitemap
from main.sitemaps import *

sitemaps = {
    'static': StaticSitemap
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path("ckeditor5/", include('django_ckeditor_5.urls')),
    path('webpush/', include('webpush.urls')),
    path('employee-portal/', include('employee_portal.urls'), name="employee_portal"),
    path('employer-portal/', include('employer_portal.urls'), name="employer_portal"),
    path('accounts/', include('allauth.urls'), name="accounts"),
    path('', include('machina.urls'), name="machina"),
    path('blog/', include('blog.urls'), name='blog'),
    path('home/', home_page, name = "home"),
    path('verify-email/',verify_email_page, name = "verify_email_page"),
    path('join-interview/<slug:interview_slug>', join_interview, name="join_interivew"),
    path('', guest_page, name = "guest"),
    path('sign-up/',sign_up_page, name = "sign_up"),
    path('about/', about_page, name = "about"),
    path('settings/',settings_page, name = "settings"),
    path('test/', test_page, name = "test"),
    path('pricing/', pricing_page, name="pricing"),
    path('billing/', billing_page, name="billing"),
    path('faq/', FAQ_page),
    path('contact/', contact_page, name="contact"),
    path('verify-email', verify_email, name="verify_email"),
    path('hijack/', include('hijack.urls')),
    path('robots.txt', TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),
    path('sitemap.xml/', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('reset',auth_views.PasswordResetView.as_view(template_name="password-reset/forgot_password.html"), 
        name = "reset_password"),
    path('reset_sent/',
            auth_views.PasswordResetDoneView.as_view(template_name="password-reset/reset_sent.html"), 
            name = "password_reset_done"),
    path('reset/<uidb64>/<token>',
            auth_views.PasswordResetConfirmView.as_view(template_name="password-reset/change_password.html"), 
            name = "password_reset_confirm"), 
    path('reset_complete',
            auth_views.PasswordResetCompleteView.as_view(template_name="password-reset/reset_complete.html"), 
            name = "password_reset_complete")
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



handler404 = 'main.views.handle_404'
handler500 = 'main.views.handle_500'