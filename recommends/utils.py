from .models import SimilarityResult, Recommendation


def store_calculated_similar_items(itemMatch, provider):
    for object_id, scores in itemMatch.items():
        for score, related_object_id in scores:
            object_target, object_target_site = provider.resolve_identifier(object_id)
            object_related, object_related_site = provider.resolve_identifier(related_object_id)
            SimilarityResult.objects.set_score_for_objects(
                object_target=object_target,
                object_target_site=object_target_site,
                object_related=object_related,
                object_related_site=object_related_site,
                score=score
            )


def store_recommended_items(user, rankings, provider):
    for score, object_id in rankings:
        object_recommended, site = provider.resolve_identifier(object_id)
        Recommendation.objects.set_score_for_object(
            user=user,
            object_recommended=object_recommended,
            object_site=site,
            score=score
        )
