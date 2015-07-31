import logging
import math
from recommends.storages.base import BaseRecommendationStorage
from recommends.settings import RECOMMENDS_LOGGER_NAME
from .settings import RECOMMENDS_STORAGE_COMMIT_THRESHOLD
from .models import Similarity, Recommendation


logger = logging.getLogger(RECOMMENDS_LOGGER_NAME)


class DjangoOrmStorage(BaseRecommendationStorage):
    def get_similarities_for_object(self, obj, limit=10, raw_id=False):
        object_site_id = self.settings.SITE_ID
        qs = Similarity.objects.similar_to(
            obj,
            related_object_site=object_site_id,
            score__gt=0).order_by('-score')
        if raw_id:
            qs = qs.extra(
                select={'contect_type_id': 'object_ctype_id'}).values(
                    'related_object_id', 'contect_type_id'
                )
        return qs[:limit]

    def get_recommendations_for_user(self, user, limit=10, raw_id=False):
        object_site_id = self.settings.SITE_ID
        qs = Recommendation.objects.filter(
            user=user.id,
            object_site=object_site_id).order_by('-score')
        if raw_id:
            qs = qs.extra(
                select={'contect_type_id': 'object_ctype_id'}).values(
                    'object_id', 'contect_type_id'
                )
        return qs[:limit]

    def get_votes(self):
        pass

    def store_votes(self, iterable):
        pass

    def store_similarities(self, itemMatch):
        try:
            logger.info('saving similarities')
            count = 0
            for object_id, scores in itemMatch:
                object_target, object_target_site = self.resolve_identifier(
                    object_id)

                for related_object_id, score in scores:
                    if not math.isnan(score) and score > self.threshold_similarities:
                        object_related, object_related_site = self.resolve_identifier(
                            related_object_id)
                        if object_target != object_related:
                            count = count + 1
                            Similarity.objects.set_score_for_objects(
                                object_target=object_target,
                                object_target_site=object_target_site,
                                object_related=object_related,
                                object_related_site=object_related_site,
                                score=score
                            )
                            if count % RECOMMENDS_STORAGE_COMMIT_THRESHOLD == 0:
                                logger.debug(
                                    'saved %s similarities...' %
                                    count)
        finally:
            logger.info('saved %s similarities...' % count)

    def store_recommendations(self, recommendations):
        try:
            logger.info('saving recommendations')
            count = 0
            for (user, rankings) in recommendations:
                for object_id, score in rankings:
                    if not math.isnan(score) and score > self.threshold_recommendations:
                        count = count + 1
                        object_recommended, site = self.resolve_identifier(
                            object_id)
                        Recommendation.objects.set_score_for_object(
                            user=user,
                            object_recommended=object_recommended,
                            object_site=site,
                            score=score
                        )
                        if count % RECOMMENDS_STORAGE_COMMIT_THRESHOLD == 0:
                            logger.debug('saved %s recommendations...' % count)
        finally:
            logger.info('saved %s recommendations...' % count)

    def remove_recommendations(self, obj):
        Recommendation.objects.filter_for_object(obj=obj).delete()

    def remove_similarities(self, obj):
        Similarity.objects.filter_for_object(obj=obj).delete()
        Similarity.objects.filter_for_related_object(related_obj=obj).delete()
