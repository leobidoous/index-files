import os
from celery import Celery
from celery.schedules import crontab

from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'indexes.settings')
app = Celery('indexes')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


def core_job() -> dict:
    return {
        'processar_digitalizado_iop': {
            'task': 'core.routine.processar_digitalizado_iop',
            'schedule': crontab(minute='*/60'),
        },
        'processar_digitalizado_domed': {
            'task': 'core.routine.processar_digitalizado_domed',
            'schedule': crontab(minute='*/60'),
        },
        'processar_prontuarios': {
            'task': 'core.routine.processar_prontuarios',
            'schedule': crontab(minute='*/60'),
        },
    }


# https://docs.celeryproject.org/en/stable/userguide/periodic-tasks.html
app.conf.beat_schedule = {
    **core_job(),
}

app.conf.timezone = 'UTC'
