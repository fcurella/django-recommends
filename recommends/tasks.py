from celery.decorators import task, periodic_task
from celery.schedules import crontab
from .utils import filelock

from .settings import RECOMMENDS_TASK_RUN, RECOMMENDS_TASK_CRONTAB


if RECOMMENDS_TASK_RUN:

    @periodic_task(run_every=crontab(**RECOMMENDS_TASK_CRONTAB))
    def recommends_precompute():
        from .providers import recommendation_registry

        # I know this is weird, but it's faster (tested on CPyhton 2.6.5)
        def _precompute(provider_instance):
            provider_instance.precompute()

        with filelock('recommends_precompute.lock'):
            [_precompute(provider_instance) for provider_instance in recommendation_registry.get_vote_providers()]


@task
def remove_suggestions(rated_model, object_id):
    from django.db.models import get_model
    from recommends.providers import recommendation_registry

    ObjectClass = get_model(*rated_model.split('.'))
    provider_instance = recommendation_registry.get_provider_for_content(ObjectClass)
    obj = ObjectClass.objects.get(pk=object_id)

    provider_instance.storage.remove_recommendations(obj)


@task
def remove_similarities(rated_model, object_id):
    from django.db.models import get_model
    from recommends.providers import recommendation_registry

    ObjectClass = get_model(*rated_model.split('.'))
    provider_instance = recommendation_registry.get_provider_for_content(ObjectClass)
    obj = ObjectClass.objects.get(pk=object_id)

    provider_instance.storage.remove_similarities(obj)
