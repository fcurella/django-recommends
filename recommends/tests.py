import timeit
from django.utils import unittest
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import Client
from example_app.models import Product, Vote
from recommends.providers import recommendation_registry
from recommends.tasks import recommends_precompute


class RecommendsTestCase(unittest.TestCase):
    def setUp(self):
        self.client = Client()
        self.mug = Product.objects.get(name='Coffee Mug')
        self.orange_juice = Product.objects.get(name='Orange Juice')
        self.wine = Product.objects.get(name='Bottle of Red Wine')
        try:
            Product.objects.get(name='1lb Tenderloin Steak').delete()
        except Product.DoesNotExist:
            pass
        self.user1 = User.objects.get(username='user1')

        self.provider = recommendation_registry.get_provider_for_content(Product)

        recommends_precompute()

    def test_similarities(self):
        similarities = self.provider.storage.get_similarities()
        self.assertNotEquals(len(similarities), 0)

        # Make sure we didn't get all 0s
        zero_scores = filter(lambda x: x.score == 0, similarities)
        self.assertNotEquals(len(zero_scores), len(similarities))

        similar_to_mug = self.provider.storage.get_similarities_for_object(self.mug)
        self.assertEquals(len(similar_to_mug), 2)
        self.assertTrue(self.wine in [s.related_object for s in similar_to_mug])

    def test_recommendation(self):
        recommendations = self.provider.storage.get_recommendations()

        self.assertNotEquals(len(recommendations), 0)

        # Make sure we didn't get all 0s
        zero_scores = filter(lambda x: x.score == 0, recommendations)
        self.assertNotEquals(len(zero_scores), len(recommendations))

        recommended = self.provider.storage.get_recommendations_for_user(self.user1)
        self.assertEquals(len(recommended), 2)
        self.assertTrue(self.wine in [s.object for s in recommended])

        # Make sure we don't recommend item that the user already have
        self.assertFalse(self.mug in [v.product for v in Vote.objects.filter(user=self.user1)])

    def test_views(self):
        self.client.login(username='user1', password='user1')

        response = self.client.get(reverse('home'))
        self.assertTrue(self.mug.get_absolute_url() in response.content)

        response = self.client.get(self.mug.get_absolute_url())
        self.assertTrue(self.orange_juice.get_absolute_url() in response.content)

    def _test_performance(self):
        stmt = """recommends_precompute()"""
        setup = """from recommends.tasks import recommends_precompute"""
        print "timing..."
        times = timeit.repeat(stmt, setup, number=100)
        print times


class RecommendsListenersTestCase(unittest.TestCase):
    def setUp(self):
        self.client = Client()
        self.mug = Product.objects.get(name='Coffee Mug')
        self.orange_juice = Product.objects.get(name='Orange Juice')
        self.wine = Product.objects.get(name='Bottle of Red Wine')
        self.steak = Product.objects.get(name='1lb Tenderloin Steak')
        self.user1 = User.objects.get(username='user1')

        self.provider = recommendation_registry.get_provider_for_content(Product)

        recommends_precompute()

    def test_listeners(self):
        self.client.login(username='user1', password='user1')
        response = self.client.get(reverse('home'))

        self.vote = Vote.objects.create(
            user=self.user1,
            product=self.steak,
            site_id=1,
            score=1
        )

        response = self.client.get(reverse('home'))
        steak_url = self.steak.get_absolute_url()
        self.assertTrue(steak_url in response.content)
        recommendations = self.provider.storage.get_recommendations_for_user(self.user1)
        steak_recs = filter(lambda x: x.object_id == self.steak.id, recommendations)
        self.assertEqual(1L, len(steak_recs))
        self.steak.delete()

        response = self.client.get(reverse('home'))
        self.assertFalse(steak_url in response.content)
        recommendations = self.provider.storage.get_recommendations_for_user(self.user1)
        steak_recs = filter(lambda x: x.object_id == self.steak.id, recommendations)
        self.assertEqual(0L, len(steak_recs))

    def tearDown(self):
        self.vote.delete()
        recommends_precompute()
