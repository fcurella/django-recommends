import logging
import math
import redis
from recommends.models import MockModel, MockSimilarity
from recommends.storages.base import BaseRecommendationStorage
from recommends.settings import RECOMMENDS_LOGGER_NAME, RECOMMENDS_STORAGE_LOGGING_THRESHOLD
from .settings import RECOMMENDS_STORAGE_REDIS_DATABASE
from .managers import RedisStorageManager


logger = logging.getLogger(RECOMMENDS_LOGGER_NAME)


class RedisStorage(BaseRecommendationStorage):
    manager = RedisStorageManager()

    _redis = None

    can_lock = True
    LOCK_KEY = 'recommends-redis-lock-key'

    @property
    def redis(self):
        if self._redis is None:
            self._redis = redis.StrictRedis(host=RECOMMENDS_STORAGE_REDIS_DATABASE['HOST'], port=RECOMMENDS_STORAGE_REDIS_DATABASE['PORT'], db=RECOMMENDS_STORAGE_REDIS_DATABASE['NAME'])
        return self._redis

    def get_lock(self):
        return self.redis.setnx(self.LOCK_KEY, 1)

    def release_lock(self):
        return self.redis.delete(self.LOCK_KEY)

    def _get_mock_models(self, dicts, mock_class=MockModel):
        return map(lambda x: mock_class(**x), dicts)

    def get_similarities_for_object(self, obj, limit=10, raw_id=False):
        r = self.redis

        object_id = self.get_identifier(obj)
        key = 'recommends:similarity:%s' % object_id
        scores = r.zrevrangebyscore(key, min=0, max=1, num=limit, start=0, withscores=True)

        similarity_dicts = []
        for identifier, score in scores:
            similarity_dict = self.identifier_manager.identifier_to_dict(object_id)
            similarity_dict.update(self.identifier_manager.identifier_to_dict(identifier, score, related=True))
            similarity_dicts.append(similarity_dict)
        if raw_id:
            return [{
                'related_object_id': item['related_object_id'],
                'contect_type_id': item['object_ctype']}
                for item in similarity_dicts][:limit]
        return self._get_mock_models(similarity_dicts, mock_class=MockSimilarity)

    def get_recommendations_for_user(self, user, limit=10, raw_id=False):
        r = self.redis
        key = 'recommends:recommendation:%s' % user.id
        scores = r.zrevrangebyscore(key, min=0, max=1, num=limit, start=0, withscores=True)

        recommendation_dicts = [self.identifier_manager.identifier_to_dict(object_id, score) for object_id, score in scores]
        if raw_id:
            return [{
                    'object_id': item['object_id'],
                    'contect_type_id': item['object_ctype']}
                    for item in recommendation_dicts][:limit]
        return self._get_mock_models(recommendation_dicts, mock_class=MockModel)

    def get_votes(self):
        pass

    def store_votes(self, iterable):
        pass

    def store_similarities(self, itemMatch):
        r = self.redis

        logger.info('saving similarities')
        count = 0

        for object_id, scores in itemMatch:
            object_target, object_target_site = self.resolve_identifier(object_id)

            for related_object_id, score in scores:
                if not math.isnan(score) and score > self.threshold_similarities:
                    object_related, object_related_site = self.resolve_identifier(related_object_id)
                    if object_target != object_related:
                        key = 'recommends:similarity:%s' % object_id
                        r.zadd(key, score, related_object_id)

                        rev_key = 'recommends:similarity_reverse:%s' % related_object_id
                        r.sadd(rev_key, object_id)

                        index_key = 'recommends:similarity:index'
                        r.sadd(index_key, object_id)

                        count = count + 1

                        if count % RECOMMENDS_STORAGE_LOGGING_THRESHOLD == 0:
                            logger.debug('saved %s similarities...' % count)
        logger.info('saved %s similarities...' % count)

    def store_recommendations(self, recommendations):
        r = self.redis

        logger.info('saving recommendation')
        count = 0

        for (user, rankings) in recommendations:
            for object_id, score in rankings:
                if not math.isnan(score) and score > self.threshold_recommendations:
                    key = 'recommends:recommendation:%s' % user.id
                    r.zadd(key, score, object_id)

                    rev_key = 'recommends:recommendation_reverse:%s' % object_id
                    r.zadd(rev_key, score, user.id)

                    index_key = 'recommends:recommendation:index'
                    r.sadd(index_key, object_id)

                    count = count + 1
                    if count % RECOMMENDS_STORAGE_LOGGING_THRESHOLD == 0:
                        logger.debug('saved %s recommendations...' % count)
        logger.info('saved %s recommendation...' % count)

    def remove_similarities(self, obj):
        r = self.redis
        object_id = self.get_identifier(obj)
        key = 'recommends:similarity:%s' % object_id
        r.delete(key)

        rev_key = 'recommends:similarity_reverse:%s' % object_id
        values = r.smembers(rev_key)
        for value in values:
            r.zrem('recommends:similarity:%s' % value, object_id)
        r.delete(rev_key)

        index_key = 'recommends:similarity:index'
        r.srem(index_key, object_id)

    def remove_recommendations(self, obj):
        r = self.redis
        object_id = self.get_identifier(obj)

        rev_key = 'recommends:recommendation_reverse:%s' % object_id
        user_ids = r.zrevrangebyscore(rev_key, min=0, max=1, start=0, num=r.zcount(rev_key, min=0, max=1))
        for user_id in user_ids:
            r.zrem('recommends:recommendation:%s' % user_id, object_id)
        r.delete(rev_key)

        index_key = 'recommends:recommendation:index'
        r.srem(index_key, object_id)
