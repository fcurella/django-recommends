from .models import SimilarityResult, Recommendation


class RecommendationStorage(object):
    def __init__(self):
        self.provider = None

    def get_similarities(self):
        raise NotImplementedError

    def store_recommended_items(self, user, rankings):
        raise NotImplementedError


class DummyStorage(RecommendationStorage):
    def store_similarities(self):
        pass

    def store_user_recommendations(self, user, rankings):
        pass


class DjangoOrmStorage(RecommendationStorage):
    def get_similarities(self):
        return SimilarityResult.objects.all()

    def store_similarities(self, itemMatch):
        for object_id, scores in itemMatch.items():
            for score, related_object_id in scores:
                object_target, object_target_site = self.provider.resolve_identifier(object_id)
                object_related, object_related_site = self.provider.resolve_identifier(related_object_id)
                SimilarityResult.objects.set_score_for_objects(
                    object_target=object_target,
                    object_target_site=object_target_site,
                    object_related=object_related,
                    object_related_site=object_related_site,
                    score=score
                )

    def store_user_recommendations(self, user, rankings):
        for score, object_id in rankings:
            object_recommended, site = self.provider.resolve_identifier(object_id)
            Recommendation.objects.set_score_for_object(
                user=user,
                object_recommended=object_recommended,
                object_site=site,
                score=score
            )
