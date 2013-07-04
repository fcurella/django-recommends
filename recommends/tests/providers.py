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
try:
    from recommends.algorithms.pyrecsys import RecSysAlgorithm
except ImportError:
    RecSysAlgorithm = None
try:
    from recommends.tasks import recommends_precompute
except ImportError:
    recommends_precompute = None

if recommends_precompute is not None:
    from recommends.tests.tests import RecommendsTestCase

from recommends.tests.models import RecProduct, RecVote


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

recommendation_registry.register(
    RecVote,
    [RecProduct],
    ProductRecommendationProvider)


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


if recommends_precompute is not None and RecSysAlgorithm is not None and getattr(settings, 'RECOMMENDS_TEST_RECSYS', False):
    class RecSysRecommendationProvider(ProductRecommendationProvider):
        algorithm = RecSysAlgorithm()

    class RecSysAlgoTestCase(RecommendsTestCase):
        results = {
            'len_recommended': 4,
            'len_similar_to_mug': 5
        }

        def setUp(self):
            recommendation_registry.unregister(
                RecVote,
                [RecProduct],
                ProductRecommendationProvider)
            recommendation_registry.register(
                RecVote,
                [RecProduct],
                RecSysRecommendationProvider)
            super(RecSysAlgoTestCase, self).setUp()

        def tearDown(self):
            super(RecSysAlgoTestCase, self).tearDown()
            recommendation_registry.unregister(
                RecVote,
                [RecProduct],
                RecSysRecommendationProvider)
            recommendation_registry.register(
                RecVote,
                [RecProduct],
                ProductRecommendationProvider)

if recommends_precompute is not None and RedisStorage is not None and getattr(settings, 'RECOMMENDS_TEST_REDIS', False):
    class RedisRecommendationProvider(GhettoRecommendationProvider):
        storage = RedisStorage(settings=settings)

    class RecommendsRedisStorageTestCase(RecommendsTestCase):

        def setUp(self):
            recommendation_registry.unregister(
                RecVote,
                [RecProduct],
                ProductRecommendationProvider)
            recommendation_registry.register(
                RecVote,
                [RecProduct],
                RedisRecommendationProvider)
            super(RecommendsRedisStorageTestCase, self).setUp()

        def tearDown(self):
            super(RecommendsRedisStorageTestCase, self).tearDown()
            recommendation_registry.unregister(
                RecVote,
                [RecProduct],
                RedisRecommendationProvider)
            recommendation_registry.register(
                RecVote,
                [RecProduct],
                ProductRecommendationProvider)

if recommends_precompute is not None and MongoStorage is not None and getattr(settings, 'RECOMMENDS_TEST_MONGO', False):
    class MongoRecommendationProvider(GhettoRecommendationProvider):
        storage = MongoStorage(settings=settings)

    class RecommendsMongoStorageTestCase(RecommendsTestCase):

        def setUp(self):
            recommendation_registry.unregister(
                RecVote,
                [RecProduct],
                ProductRecommendationProvider)
            recommendation_registry.register(
                RecVote,
                [RecProduct],
                MongoRecommendationProvider)
            super(RecommendsMongoStorageTestCase, self).setUp()

        def tearDown(self):
            super(RecommendsMongoStorageTestCase, self).tearDown()
            recommendation_registry.unregister(
                RecVote,
                [RecProduct],
                MongoRecommendationProvider)
            recommendation_registry.register(
                RecVote,
                [RecProduct],
                ProductRecommendationProvider)
