from django.apps import AppConfig


class EmployerPortalConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'employer_portal'

    def ready(self):
        import employer_portal.signals
