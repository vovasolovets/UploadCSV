from __future__ import absolute_import, unicode_literals

import os
from celery import Celery

celery = Celery('UploadCSV')

CELERY_TIMEZONE = 'UTC'

celery.conf.update(BROKER_URL=os.environ['REDIS_URL'],)
celery.autodiscover_tasks()