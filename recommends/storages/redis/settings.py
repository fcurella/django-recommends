from django.conf import settings

RECOMMENDS_REDIS_HOST = getattr(settings, 'RECOMMENDS_REDIS_HOST', 'localhost')
RECOMMENDS_REDIS_PORT = getattr(settings, 'RECOMMENDS_REDIS_PORT', 6379)
RECOMMENDS_REDIS_DB = getattr(settings, 'RECOMMENDS_REDIS_DB', 0)
