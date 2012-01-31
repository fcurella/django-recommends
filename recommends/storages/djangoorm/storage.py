import math
from recommends.storages.base import BaseRecommendationStorage
from recommends.converters import resolve_identifier, get_identifier
from .models import Similarity, Recommendation


class DjangoOrmStorage(BaseRecommendationStorage):
    def get_identifier(self, obj, site_id=None, rating=None, *args, **kwargs):
        if rating is not None:
            site_id = self.get_rating_site(rating).id
        if site_id is None:
            site_id = self.settings.SITE_ID
        return get_identifier(obj, site_id)

    def resolve_identifier(self, identifier):
        return resolve_identifier(identifier)

    def get_similarities_for_object(self, obj, limit):
        object_site_id = self.settings.SITE_ID
        return Similarity.objects.similar_to(obj, related_object_site=object_site_id, score__gt=0).order_by('-score')[:limit]

    def get_recommendations_for_user(self, user, limit):
        object_site_id = self.settings.SITE_ID
        return Recommendation.objects.filter(user=user.id, object_site=object_site_id).order_by('-score')[:limit]

    def get_votes(self):
        pass

    def store_votes(self, iterable):
        pass

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

    def remove_recommendations(self, obj):
        Recommendation.objects.filter_for_object(obj=obj).delete()

    def remove_similarities(self, obj):
        Similarity.objects.filter_for_object(obj=obj).delete()
        Similarity.objects.filter_for_related_object(related_obj=obj).delete()
