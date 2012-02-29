import logging
import math
from django.db import transaction
from recommends.storages.base import BaseRecommendationStorage
from recommends.settings import RECOMMENDS_LOGGER_NAME
from .settings import RECOMMENDS_STORAGE_COMMIT_THRESHOLD
from .models import Similarity, Recommendation


logger = logging.getLogger(RECOMMENDS_LOGGER_NAME)


class DjangoOrmStorage(BaseRecommendationStorage):
    def get_similarities_for_object(self, obj, limit=10):
        object_site_id = self.settings.SITE_ID
        return Similarity.objects.similar_to(obj, related_object_site=object_site_id, score__gt=0).order_by('-score')[:limit]

    def get_recommendations_for_user(self, user, limit=10):
        object_site_id = self.settings.SITE_ID
        return Recommendation.objects.filter(user=user.id, object_site=object_site_id).order_by('-score')[:limit]

    def get_votes(self):
        pass

    def store_votes(self, iterable):
        pass

    @transaction.commit_manually
    def store_similarities(self, itemMatch):
        import time

        count = 0
        t1 = time.clock()
        try:
            logger.info('saving similarities')
            tt = time.clock()
            for object_id, scores in itemMatch:
                object_target, object_target_site = self.resolve_identifier(object_id)

                for related_object_id, score in scores:
                    if not math.isnan(score):
                        object_related, object_related_site = self.resolve_identifier(related_object_id)
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
                                transaction.commit()
                                logger.info('saved %s similarities...' % count)
                                t2 = time.clock()
                                logger.info('time partial %s' % (t2 - tt))
                                logger.info('time total %s' % (t2 - t1))
                                tt = time.clock()
        finally:
            transaction.commit()
            logger.info('saved %s similarities...' % count)
            t2 = time.clock()
            logger.info('time %s' % (t2 - t1))
            logger.info('flipping table...')
            Similarity.objects.flip()

    @transaction.commit_manually
    def store_recommendations(self, recommendations):
        try:
            logger.info('saving recommendations')
            count = 0
            for (user, rankings) in recommendations:
                for object_id, score in rankings:
                    if not math.isnan(score):
                        count = count + 1
                        object_recommended, site = self.resolve_identifier(object_id)
                        Recommendation.objects.set_score_for_object(
                            user=user,
                            object_recommended=object_recommended,
                            object_site=site,
                            score=score
                        )
                        if count % RECOMMENDS_STORAGE_COMMIT_THRESHOLD == 0:
                            logger.info('saved %s recommendations...' % count)
                            transaction.commit()
        finally:
            logger.info('saved %s recommendations...' % count)
            transaction.commit()
            logger.info('flipping table...')
            Recommendation.objects.flip()

    def remove_recommendations(self, obj):
        Recommendation.objects.filter_for_object(obj=obj).delete()

    def remove_similarities(self, obj):
        Similarity.objects.filter_for_object(obj=obj).delete()
        Similarity.objects.filter_for_related_object(related_obj=obj).delete()
