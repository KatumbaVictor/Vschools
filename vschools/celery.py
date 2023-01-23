from __future__ import absolute_import, unicode_literals
import os

from celery import Celery
from django.conf import settings
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE','vschools.settings')

app = Celery('vschools')
app.conf.enable_utc = False

app.conf.update(timezone='Africa/Kampala')

app.config_from_object(settings, namespace='CELERY')

app.conf.beat_schedule = {
    'execute_func': {
        'task': 'main.tasks.test_function',
        'schedule': crontab(hour=00,minute=26)
    }
}

app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')