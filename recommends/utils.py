from .models import SimilarityResult, Recommendation
from .converters import resolve_identifier


def store_calculated_similar_items(itemMatch, provider):
    for object_id, scores in itemMatch.items():
        for score, related_object_id in scores:
            object_target = provider.resolve_identifier(object_id)
            object_related = provider.resolve_identifier(related_object_id)

            SimilarityResult.objects.set_score_for_objects(
                object_target=object_target,
                object_related=object_related,
                score=score
            )


def store_recommended_items(user, rankings, provider):
    for score, object_id in rankings:
        object_recommended = provider.resolve_identifier(object_id)
        Recommendation.objects.set_score_for_object(
            user=user,
            object_recommended=object_recommended,
            score=score
        )
