from django.conf import settings

RECOMMENDS_STORAGE_DATABASE_ALIAS = getattr(settings, 'RECOMMENDS_STORAGE_DATABASE_ALIAS', 'recommends')
