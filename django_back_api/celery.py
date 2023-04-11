import os
from celery import Celery


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_back_api.settings")
app = Celery("django_back_api")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
