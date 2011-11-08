from celery.decorators import periodic_task
from celery.task.schedules import crontab

from .providers import recommendation_registry


@periodic_task(run_every=crontab(hour="*/24"))
def precompute_items():
    for provider in recommendation_registry.providers:
        prefs = provider.prefs()
        provider.precompute(prefs)
