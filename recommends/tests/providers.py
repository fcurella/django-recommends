from django.conf import settings
from django.contrib.auth.models import User
from recommends.providers import RecommendationProvider
from recommends.providers import recommendation_registry
try:
    from recommends.storages.mongodb.storage import MongoStorage
except ImportError:
    MongoStorage = None
try:
    from recommends.storages.redis.storage import RedisStorage
except ImportError:
    RedisStorage = None

from recommends.tests.tests import RecommendsTestCase
from recommends.tests.models import  RecProduct, RecVote


class ProductRecommendationProvider(RecommendationProvider):
    def get_users(self):
        return User.objects.filter(is_active=True, rec_votes__isnull=False).distinct()

    def get_items(self):
        return RecProduct.objects.all()

    def get_ratings(self, obj):
        return RecVote.objects.filter(product=obj)

    def get_rating_score(self, rating):
        return rating.score

    def get_rating_site(self, rating):
        return rating.site

    def get_rating_user(self, rating):
        return rating.user

    def get_rating_item(self, rating):
        return rating.product

recommendation_registry.register(RecVote, [RecProduct], ProductRecommendationProvider)


class GhettoRecommendationProvider(RecommendationProvider):
    def get_users(self):
        return User.objects.filter(is_active=True, rec_votes__isnull=False).distinct()

    def get_items(self):
        return RecProduct.objects.all()

    def get_ratings(self, obj):
        return RecVote.objects.filter(product=obj)

    def get_rating_score(self, rating):
        return rating.score

    def get_rating_site(self, rating):
        return rating.site

    def get_rating_user(self, rating):
        return rating.user

    def get_rating_item(self, rating):
        return rating.product


if RedisStorage is not None and getattr(settings, 'RECOMMENDS_TEST_REDIS', False):
    class RedisRecommendationProvider(GhettoRecommendationProvider):
        storage = RedisStorage(settings=settings)

    class RecommendsRedisStorageTestCase(RecommendsTestCase):
        def setUp(self):
            recommendation_registry.unregister(RecVote, [RecProduct], ProductRecommendationProvider)
            recommendation_registry.register(RecVote, [RecProduct], RedisRecommendationProvider)
            super(RecommendsRedisStorageTestCase, self).setUp()


if MongoStorage is not None and getattr(settings, 'RECOMMENDS_TEST_MONGO', False):
    class MongoRecommendationProvider(GhettoRecommendationProvider):
        storage = MongoStorage(settings=settings)

    class RecommendsMongoStorageTestCase(RecommendsTestCase):
        def setUp(self):
            recommendation_registry.unregister(RecVote, [RecProduct], ProductRecommendationProvider)
            recommendation_registry.register(RecVote, [RecProduct], MongoRecommendationProvider)
            super(RecommendsMongoStorageTestCase, self).setUp()
