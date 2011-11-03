from django.contrib.auth.models import User
from celery.decorators import periodic_task
from celery.task.schedules import crontab

from .providers import recommendation_registry
from .models import SimilarityResult
from .filtering import calculate_similar_items, get_recommended_items
from .utils import store_calculated_similar_items, store_recommended_items


@periodic_task(run_every=crontab(hour="*/24"))
def compute_similar_items():
    for provider in recommendation_registry.providers:
        prefs = provider.prefs()
        itemMatch = calculate_similar_items(prefs)
        store_calculated_similar_items(itemMatch, provider)


@periodic_task(run_every=crontab(hour="*/24"))
def compute_recommended_items():
    itemMatch = SimilarityResult.objects.all()

    for provider in recommendation_registry.providers:
        prefs = provider.prefs()
        for user in User.objects.filter(is_active=True):
            rankings = get_recommended_items(prefs, itemMatch, user)
            store_recommended_items(user, rankings, provider)
