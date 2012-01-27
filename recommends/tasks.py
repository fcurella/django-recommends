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
            [_precompute(provider_instance) for model, provider_instance in recommendation_registry.providers.iteritems()]


@task
def remove_suggestion(user_id, rating_model, model_path, object_id):
    from django.contrib.auth.models import User
    from django.db.models import get_model
    from recommends.providers import recommendation_registry

    provider_instance = recommendation_registry.providers[rating_model]
    user = User.objects.get(id=user_id)

    ObjectClass = get_model(*model_path.split('.'))
    obj = ObjectClass.objects.get(pk=object_id)

    provider_instance.storage.remove_recommendation(user, obj)


@task
def remove_similarity(rating_model, model_path, object_id):
    from django.db.models import get_model
    from recommends.providers import recommendation_registry

    provider_instance = recommendation_registry.providers[rating_model]

    ObjectClass = get_model(*model_path.split('.'))
    obj = ObjectClass.objects.get(pk=object_id)

    provider_instance.storage.remove_similarity(obj)
