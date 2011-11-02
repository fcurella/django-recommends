from django.contrib.auth.models import User
from celery.decorators import task, periodic_task
from celery.task.schedules import crontab

from .models import SimilarityResult
from .utils import calculate_similar_items, store_calculated_similar_items
from .utils import get_recommended_items, store_recommended_items


@periodic_task(run_every=crontab(hour="*/24"))
def compute_similar_items(prefs):
    for user in User.objects.filter(is_active=True):
        itemMatch = calculate_similar_items(prefs)
        store_calculated_similar_items(itemMatch)


@periodic_task(run_every=crontab(hour="*/24"))
def compute_reccomended_items(prefs):
    itemMatch = SimilarityResult.objects.all()

    for user in User.objects.filter(is_active=True):
        rankings = get_recommended_items(prefs, itemMatch, user)
        store_recommended_items(user, rankings)
