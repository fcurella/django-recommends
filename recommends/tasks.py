from celery.task import task, periodic_task
from celery.schedules import crontab
from .utils import filelock

from .settings import RECOMMENDS_TASK_RUN, RECOMMENDS_TASK_CRONTAB, RECOMMENDS_TASK_EXPIRES


def recommends_precompute():
    results = []
    from .providers import recommendation_registry

    # I know this is weird, but it's faster (tested on CPyhton 2.6.5)
    def _precompute(provider_instance):
        results.append(provider_instance.precompute())

    if recommendation_registry.storage.can_lock:
        locked = recommendation_registry.storage.get_lock()
        if locked:
            try:
                [_precompute(provider_instance) for provider_instance in recommendation_registry.get_vote_providers()]
            finally:
                recommendation_registry.storage.release_lock()
    else:
        with filelock('recommends_precompute.lock'):
            [_precompute(provider_instance)
             for provider_instance in recommendation_registry.get_vote_providers()]

    return results

if RECOMMENDS_TASK_RUN:
    @periodic_task(name='recommends_precompute', run_every=crontab(**RECOMMENDS_TASK_CRONTAB), expires=RECOMMENDS_TASK_EXPIRES)
    def _recommends_precompute():
        recommends_precompute()


@task(name='remove_suggestions')
def remove_suggestions(rated_model, object_id):
    from django.apps import apps
    from recommends.providers import recommendation_registry

    ObjectClass = apps.get_model(*rated_model.split('.'))
    provider_instance = recommendation_registry.get_provider_for_content(
        ObjectClass)
    obj = ObjectClass.objects.get(pk=object_id)

    provider_instance.storage.remove_recommendations(obj)


@task(name='remove_similarities')
def remove_similarities(rated_model, object_id):
    from django.apps import apps
    from recommends.providers import recommendation_registry

    ObjectClass = apps.get_model(*rated_model.split('.'))
    provider_instance = recommendation_registry.get_provider_for_content(
        ObjectClass)
    obj = ObjectClass.objects.get(pk=object_id)

    provider_instance.storage.remove_similarities(obj)
