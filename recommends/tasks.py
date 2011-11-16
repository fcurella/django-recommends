from celery.decorators import periodic_task
from celery.schedules import crontab

from .providers import recommendation_registry
from .settings import RECOMMENDS_TASK_CRONTAB


@periodic_task(run_every=crontab(**RECOMMENDS_TASK_CRONTAB))
def recommends_precompute():
    for Provider in recommendation_registry.providers:
        provider_instance = Provider()
        prefs = provider_instance.prefs()
        provider_instance.precompute(prefs)
