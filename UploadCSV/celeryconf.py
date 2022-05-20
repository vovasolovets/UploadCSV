from __future__ import absolute_import, unicode_literals

import os
from celery import Celery
from django.core import management

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')

app = Celery('csv_upload')

CELERY_TIMEZONE = 'UTC'

app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.update(BROKER_URL=os.environ['REDIS_URL'],
                CELERY_RESULT_BACKEND=os.environ['REDIS_URL'])
app.autodiscover_tasks()