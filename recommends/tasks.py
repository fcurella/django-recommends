from celery.decorators import periodic_task
from celery.schedules import crontab

from .providers import recommendation_registry


@periodic_task(run_every=crontab(hour="*/24"))
def precompute_items():
    for Provider in recommendation_registry.providers:
        provider_instance = Provider()
        prefs = provider_instance.prefs()
        provider_instance.precompute(prefs)
