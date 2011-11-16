from django.conf import settings

RECOMMENDS_TASK_CRONTAB = getattr(settings, 'RECOMMENDS_TASK_CRONTAB', {'hour': '*/24'})
