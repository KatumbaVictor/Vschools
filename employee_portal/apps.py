from django.apps import AppConfig


class EmployeePortalConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'employee_portal'

    def ready(self):
        import employee_portal.signals
