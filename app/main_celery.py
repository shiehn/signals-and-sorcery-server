'''This file configures a Celery app server'''
import logging

from celery import Celery
from celery.app.log import Logging

from django.conf import settings


APP = Celery(
    'django-seed',
    broker=settings.REDIS_URL,
    include=['tasks.tasks']
)
APP.conf.update(
    task_default_queue=settings.CELERY_QUEUE,
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='Asia/Dubai',
    enable_utc=True,
    result_backend='django-db',
)
APP.log = Logging(APP)
APP.log.setup(
    loglevel=logging.INFO,
    redirect_stdouts=True,
    redirect_level=logging.INFO,
    colorize=True,
)

# Load task modules from all registered Django app configs.
APP.autodiscover_tasks()
