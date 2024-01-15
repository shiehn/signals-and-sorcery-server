'''
Loads Celery configuration
'''

from .main_celery import APP as celery_app

__all__ = ('celery_app',)
