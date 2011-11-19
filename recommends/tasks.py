from celery.decorators import periodic_task
from celery.schedules import crontab

from .providers import recommendation_registry
from .settings import RECOMMENDS_TASK_CRONTAB


@periodic_task(run_every=crontab(**RECOMMENDS_TASK_CRONTAB))
def recommends_precompute():
    # I know this is weird, but it's faster (tested on CPyhton 2.6.5)
    def _precompute(ProviderClass):
        provider_instance = ProviderClass()
        prefs = provider_instance.prefs()
        provider_instance.precompute(prefs)
    [_precompute(Provider) for model, Provider in recommendation_registry.providers.iteritems()]
