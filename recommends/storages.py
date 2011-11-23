import math
from django.contrib.sites.models import Site
from .converters import resolve_identifier, get_identifier
from .models import Similarity, Recommendation
from django.conf import settings


class RecommendationStorage(object):
    def get_identifier(self, obj, *args, **kwargs):
        """Given an object and optional parameters, returns a string identifying the object uniquely"""
        raise NotImplementedError

    def resolve_identifier(self, identifier):
        """Returns an object corresponding to an identifier in the format returned by ``get_identifier``"""
        raise NotImplementedError

    def get_similarities_for_object(self, obj, limit):
        raise NotImplementedError

    def get_recommendations_for_user(self, user, limit):
        raise NotImplementedError

    def store_similarities(self, itemMatch):
        raise NotImplementedError

    def store_recommendations(self, recommendations):
        """
        ``recommendations`` is an iterable with the following schema:

        ::

            (
                (
                    <user>,
                    (
                        (<object_identifier>, <score>),
                        (<object_identifier>, <score>)
                    ),
                )
            )
        """
        raise NotImplementedError
    
    def remove_recommendation(self, user, obj):
        raise NotImplementedError


class DjangoOrmStorage(RecommendationStorage):
    def get_identifier(self, obj, site=None, rating=None, *args, **kwargs):
        if rating is not None:
            site = self.get_rating_site(rating)
        if site is None:
            site = Site.objects.get_current()
        return get_identifier(obj, site)

    def resolve_identifier(self, identifier):
        return resolve_identifier(identifier)

    def get_similarities_for_object(self, obj, limit):
        object_site = Site.objects.get_current()
        return Similarity.objects.similar_to(obj, site=object_site, score__gt=0).order_by('-score')[:limit]

    def get_recommendations_for_user(self, user, limit):
        object_site_id = settings.SITE_ID
        return Recommendation.objects.filter(user=user, object_site__id=object_site_id).order_by('-score')[:limit]

    def store_similarities(self, itemMatch):
        for object_id, scores in itemMatch:
            object_target, object_target_site = self.resolve_identifier(object_id)

            for related_object_id, score in scores:
                if not math.isnan(score):
                    object_related, object_related_site = self.resolve_identifier(related_object_id)
                    if object_target != object_related:
                        Similarity.objects.set_score_for_objects(
                            object_target=object_target,
                            object_target_site=object_target_site,
                            object_related=object_related,
                            object_related_site=object_related_site,
                            score=score
                        )

    def store_recommendations(self, recommendations):
        for (user, rankings) in recommendations:
            for object_id, score in rankings:
                if not math.isnan(score):
                    object_recommended, site = self.resolve_identifier(object_id)
                    Recommendation.objects.set_score_for_object(
                        user=user,
                        object_recommended=object_recommended,
                        object_site=site,
                        score=score
                    )

    def remove_recommendation(self, user, obj):
        app_label = obj._meta.app_label
        model = obj._meta.object_name.lower()

        try:
            Recommendation.objects.get(user=user, object_ctype__app_label=app_label, object_ctype__model=model, object_id=obj.id).delete()
        except Recommendation.DoesNotExist:
            pass
