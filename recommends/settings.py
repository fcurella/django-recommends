from django.conf import settings

RECOMMENDS_TASK_CRONTAB = getattr(settings, 'RECOMMENDS_TASK_CRONTAB', {'hour': '*/24'})
RECOMMENDS_CACHE_TEMPLATETAGS_TIMEOUT = getattr(settings, 'RECOMMENDS_CACHE_TEMPLATETAGS_TIMEOUT', 86400)
RECOMMENDS_STORAGE_BACKEND = getattr(settings, 'RECOMMENDS_STORAGE_BACKEND', 'recommends.storages.DjangoOrmStorage')
