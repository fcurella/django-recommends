from django.conf import settings
from django.utils import unittest
from django.contrib.auth.models import User
from example_project.example_app.models import Product, Vote, ProductRecommendationProvider
from recommends.providers import RecommendationProvider
from recommends.providers import recommendation_registry
from recommends.storages.mongodb.storage import MongoStorage
from recommends.storages.redis.storage import RedisStorage
from recommends.algorithms.pyrecsys import RecSysAlgorithm
from recommends.tests.tests import RecommendsTestCase


class GhettoRecommendationProvider(RecommendationProvider):
    def get_users(self):
        return User.objects.filter(is_active=True, votes__isnull=False).distinct()

    def get_items(self):
        return Product.objects.all()

    def get_ratings(self, obj):
        return Vote.objects.filter(product=obj)

    def get_rating_score(self, rating):
        return rating.score

    def get_rating_site(self, rating):
        return rating.site

    def get_rating_user(self, rating):
        return rating.user

    def get_rating_item(self, rating):
        return rating.product


class RecSysRecommendationProvider(GhettoRecommendationProvider):
    algorithm = RecSysAlgorithm(k=100)


class RedisRecommendationProvider(GhettoRecommendationProvider):
    storage = RedisStorage(settings=settings)


class MongoRecommendationProvider(GhettoRecommendationProvider):
    storage = MongoStorage(settings=settings)


if getattr(settings, 'RECOMMENDS_TEST_REDIS', False):
    class RecommendsRedisStorageTestCase(RecommendsTestCase):
        def setUp(self):
            recommendation_registry.unregister(Vote, [Product], ProductRecommendationProvider)
            recommendation_registry.register(Vote, [Product], RedisRecommendationProvider)
            super(RecommendsRedisStorageTestCase, self).setUp()


if getattr(settings, 'RECOMMENDS_TEST_MONGO', False):
    class RecommendsMongoStorageTestCase(RecommendsTestCase):
        def setUp(self):
            recommendation_registry.unregister(Vote, [Product], ProductRecommendationProvider)
            recommendation_registry.register(Vote, [Product], MongoRecommendationProvider)
            super(RecommendsMongoStorageTestCase, self).setUp()
