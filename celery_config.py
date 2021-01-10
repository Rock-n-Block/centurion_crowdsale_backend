import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'centurion_crowdsale.settings')
import django
django.setup()
from centurion_crowdsale.projects.models import CenturionProject
from centurion_crowdsale.settings import DUCX_STAKING_TIMEZONE, DUCX_STAKING_HOUR, DUCX_STAKING_MINUTE

app = Celery('centurion_crowdsale', broker='amqp://rabbit:rabbit@rabbitmq:5672/rabbit', include=['celery_tasks'])
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.update(result_expires=3600, enable_utc=True, timezone=DUCX_STAKING_TIMEZONE)

schedule = {}
projects = CenturionProject.objects.all()

for project in projects:
    if project.raise_start_datetime is None:
        continue

    schedule[f'{project.string_id}_ducx_staking'] = {
        'task': "celery_tasks.ducx_staking",
        'args': (project,),
        'schedule':
            crontab(hour=DUCX_STAKING_HOUR, minute=DUCX_STAKING_MINUTE, day_of_month=project.raise_start_datetime.day,),
        'eta': project.taking_start_datetime,
        'expires': project.staking_finish_datetime,
    },

app.conf.beat_schedule = schedule
