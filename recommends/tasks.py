from celery import task
from .utils import filelock


@task(name='recommends_precompute')
def recommends_precompute():
    results = []
    from .providers import recommendation_registry

    # I know this is weird, but it's faster (tested on CPyhton 2.6.5)
    def _precompute(provider_instance):
        results.append(provider_instance.precompute())

    with filelock('recommends_precompute.lock'):
        [_precompute(provider_instance)
            for provider_instance in recommendation_registry.get_vote_providers()]

    return results


@task(name='remove_suggestions')
def remove_suggestions(rated_model, object_id):
    from django.db.models import get_model
    from recommends.providers import recommendation_registry

    ObjectClass = get_model(*rated_model.split('.'))
    provider_instance = recommendation_registry.get_provider_for_content(
        ObjectClass)
    obj = ObjectClass.objects.get(pk=object_id)

    provider_instance.storage.remove_recommendations(obj)


@task(name='remove_similarities')
def remove_similarities(rated_model, object_id):
    from django.db.models import get_model
    from recommends.providers import recommendation_registry

    ObjectClass = get_model(*rated_model.split('.'))
    provider_instance = recommendation_registry.get_provider_for_content(
        ObjectClass)
    obj = ObjectClass.objects.get(pk=object_id)

    provider_instance.storage.remove_similarities(obj)
