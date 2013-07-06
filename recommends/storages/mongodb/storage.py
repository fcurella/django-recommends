import logging
import math
import pymongo
from recommends.models import MockModel, MockSimilarity
from recommends.storages.base import BaseRecommendationStorage
from recommends.settings import RECOMMENDS_LOGGER_NAME, RECOMMENDS_STORAGE_LOGGING_THRESHOLD
from .settings import (
    RECOMMENDS_STORAGE_MONGODB_DATABASE,
    RECOMMENDS_STORAGE_MONGODB_SIMILARITY_COLLECTION,
    RECOMMENDS_STORAGE_MONGODB_RECOMMENDATION_COLLECTION,
    RECOMMENDS_STORAGE_MONGODB_FSYNC
)
from .managers import MongoStorageManager


logger = logging.getLogger(RECOMMENDS_LOGGER_NAME)


class MongoStorage(BaseRecommendationStorage):
    manager = MongoStorageManager()

    def _get_mock_models(self, spec, collection_name, limit, raw_id, mock_class=MockModel):
        connection = pymongo.Connection(RECOMMENDS_STORAGE_MONGODB_DATABASE['HOST'], RECOMMENDS_STORAGE_MONGODB_DATABASE['PORT'])
        db = connection[RECOMMENDS_STORAGE_MONGODB_DATABASE['NAME']]
        collection = db[collection_name]

        documents = collection.find(spec, limit=limit, sort=[('score', pymongo.DESCENDING)])
        if raw_id:
            if mock_class is MockModel:
                return [{
                        'object_id': item['object_id'],
                        'contect_type_id': item['object_ctype']}
                        for item in documents]
            elif mock_class is MockSimilarity:
                return [{
                    'related_object_id': item['related_object_id'],
                    'contect_type_id': item['object_ctype']}
                    for item in documents]
        return map(lambda x: mock_class(**x), documents)

    def get_similarities_for_object(self, obj, limit=10, raw_id=False):
        object_site_id = self.settings.SITE_ID
        spec = dict(related_object_site=object_site_id, **self.manager.filter_for_object(obj))
        collection_name = RECOMMENDS_STORAGE_MONGODB_SIMILARITY_COLLECTION

        return self._get_mock_models(spec, collection_name, limit, raw_id, mock_class=MockSimilarity)

    def get_recommendations_for_user(self, user, limit=10, raw_id=False):
        spec = {'user': user.id, 'object_site': self.settings.SITE_ID}
        collection_name = RECOMMENDS_STORAGE_MONGODB_RECOMMENDATION_COLLECTION

        return self._get_mock_models(spec, collection_name, limit, raw_id)

    def get_votes(self):
        pass

    def store_votes(self, iterable):
        pass

    def store_similarities(self, itemMatch):
        connection = pymongo.Connection(RECOMMENDS_STORAGE_MONGODB_DATABASE['HOST'], RECOMMENDS_STORAGE_MONGODB_DATABASE['PORT'])
        db = connection[RECOMMENDS_STORAGE_MONGODB_DATABASE['NAME']]
        collection = db[RECOMMENDS_STORAGE_MONGODB_SIMILARITY_COLLECTION]

        logger.info('saving similarities')
        count = 0

        for object_id, scores in itemMatch:
            object_target, object_target_site = self.resolve_identifier(object_id)

            for related_object_id, score in scores:
                if not math.isnan(score) and score > self.threshold_similarities:
                    object_related, object_related_site = self.resolve_identifier(related_object_id)
                    if object_target != object_related:
                        spec = self.manager.similarity_for_objects(object_target=object_target, object_target_site=object_target_site, object_related=object_related, object_related_site=object_related_site)
                        collection.update(spec, {'$set': {'score': score}}, upsert=True, fsync=RECOMMENDS_STORAGE_MONGODB_FSYNC)
                        count = count + 1

                        if count % RECOMMENDS_STORAGE_LOGGING_THRESHOLD == 0:
                            logger.debug('saved %s similarities...' % count)

        logger.info('saved %s similarities...' % count)

    def store_recommendations(self, recommendations):
        connection = pymongo.Connection(RECOMMENDS_STORAGE_MONGODB_DATABASE['HOST'], RECOMMENDS_STORAGE_MONGODB_DATABASE['PORT'])
        db = connection[RECOMMENDS_STORAGE_MONGODB_DATABASE['NAME']]
        collection = db[RECOMMENDS_STORAGE_MONGODB_RECOMMENDATION_COLLECTION]

        logger.info('saving recommendation')
        count = 0

        for (user, rankings) in recommendations:
            for object_id, score in rankings:
                if not math.isnan(score) and score > self.threshold_recommendations:
                    count = count + 1
                    object_recommended, site = self.resolve_identifier(object_id)
                    spec = self.manager.suggestion_for_object(
                        user=user,
                        object_recommended=object_recommended,
                        object_site=site
                    )
                    collection.update(spec, {'$set': {'score': score}}, upsert=True, fsync=RECOMMENDS_STORAGE_MONGODB_FSYNC)

                    if count % RECOMMENDS_STORAGE_LOGGING_THRESHOLD == 0:
                        logger.debug('saved %s recommendations...' % count)
        logger.info('saved %s recommendation...' % count)

    def remove_recommendations(self, obj):
        connection = pymongo.Connection(RECOMMENDS_STORAGE_MONGODB_DATABASE['HOST'], RECOMMENDS_STORAGE_MONGODB_DATABASE['PORT'])
        db = connection[RECOMMENDS_STORAGE_MONGODB_DATABASE['NAME']]
        collection = db[RECOMMENDS_STORAGE_MONGODB_RECOMMENDATION_COLLECTION]
        collection.remove(self.manager.filter_for_object(obj), fsync=RECOMMENDS_STORAGE_MONGODB_FSYNC)

    def remove_similarities(self, obj):
        connection = pymongo.Connection(RECOMMENDS_STORAGE_MONGODB_DATABASE['HOST'], RECOMMENDS_STORAGE_MONGODB_DATABASE['PORT'])
        db = connection[RECOMMENDS_STORAGE_MONGODB_DATABASE['NAME']]

        collection = db[RECOMMENDS_STORAGE_MONGODB_SIMILARITY_COLLECTION]

        collection.remove(self.manager.filter_for_object(obj), fsync=RECOMMENDS_STORAGE_MONGODB_FSYNC)
        collection.remove(self.manager.filter_for_related_object(obj), fsync=RECOMMENDS_STORAGE_MONGODB_FSYNC)
